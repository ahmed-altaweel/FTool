import contextlib
import io
import os
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from Infrastructure.Compression.RarEngine import RarEngine  # noqa: E402
from Infrastructure.Compression.ZipEngine import ZipEngine  # noqa: E402
from Presentation.CLI.main import main  # noqa: E402


class CliTestCase(unittest.TestCase):
    """Runs the real CLI (parser -> handler -> engine -> formatter) inside a temp folder."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)
        self._old_cwd = os.getcwd()
        os.chdir(self.dir)
        self.addCleanup(os.chdir, self._old_cwd)
        env = mock.patch.dict(os.environ, {"XDG_DATA_HOME": str(self.dir / "_data")})
        env.start()
        self.addCleanup(env.stop)

    def ftool(self, *argv: str, stdin: str = "") -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), mock.patch("sys.stdin", io.StringIO(stdin)):
            code = main(list(argv))
        return code, out.getvalue()

    def make_tree(self) -> None:
        (self.dir / "proj/src").mkdir(parents=True)
        (self.dir / "proj/node_modules/x").mkdir(parents=True)
        (self.dir / "proj/empty").mkdir()
        (self.dir / "proj/a.txt").write_text("hello", encoding="utf-8")
        (self.dir / "proj/src/m.py").write_text("print(1)", encoding="utf-8")
        (self.dir / "proj/node_modules/x/j.js").write_text("junk", encoding="utf-8")
        (self.dir / "proj/b.tmp").write_text("tmp", encoding="utf-8")
        (self.dir / "proj/ملف.txt").write_text("عربي", encoding="utf-8")

    @staticmethod
    def names(path: Path) -> set[str]:
        with zipfile.ZipFile(path) as z:
            return set(z.namelist())


class ArchiveTests(CliTestCase):
    def test_roundtrip_with_exclude_and_unicode(self) -> None:
        self.make_tree()
        code, _ = self.ftool("archive", "proj", "-e", "node_modules", "-e", "*.tmp", "-o", "out.zip")
        self.assertEqual(code, 0)
        names = self.names(self.dir / "out.zip")
        self.assertIn("proj/a.txt", names)
        self.assertIn("proj/ملف.txt", names)
        self.assertIn("proj/empty/", names)
        self.assertFalse(any("node_modules" in n or n.endswith(".tmp") for n in names))

        code, _ = self.ftool("extract", "out.zip", "-t", "restored")
        self.assertEqual(code, 0)
        self.assertEqual((self.dir / "restored/proj/ملف.txt").read_text(encoding="utf-8"), "عربي")
        self.assertTrue((self.dir / "restored/proj/empty").is_dir())

    def test_default_name_and_format_from_extension(self) -> None:
        self.make_tree()
        self.assertEqual(self.ftool("archive", "proj/a.txt")[0], 0)
        self.assertTrue((self.dir / "a.txt.zip").exists())
        code, _ = self.ftool("archive", "proj/a.txt", "-o", "x.rar", "-f", "zip")
        self.assertEqual(code, 1)  # explicit zip + .rar name is rejected, not silently wrong

    def test_dry_run_creates_nothing(self) -> None:
        self.make_tree()
        code, out = self.ftool("archive", "proj", "-o", "out.zip", "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("SIMULATION", out)
        self.assertFalse((self.dir / "out.zip").exists())

    def test_output_inside_source_is_not_archived_into_itself(self) -> None:
        self.make_tree()
        self.assertEqual(self.ftool("archive", "proj", "-o", "proj/self.zip")[0], 0)
        self.assertNotIn("proj/self.zip", self.names(self.dir / "proj/self.zip"))

    def test_existing_output_needs_force(self) -> None:
        self.make_tree()
        self.assertEqual(self.ftool("archive", "proj", "-o", "o.zip")[0], 0)
        code, out = self.ftool("archive", "proj", "-o", "o.zip")
        self.assertEqual(code, 1)
        self.assertIn("--force", out)
        self.assertEqual(self.ftool("archive", "proj", "-o", "o.zip", "--force")[0], 0)

    def test_wildcards_and_missing_sources(self) -> None:
        self.make_tree()
        self.assertEqual(self.ftool("archive", "proj/*.txt", "-o", "w.zip")[0], 0)
        self.assertEqual(self.names(self.dir / "w.zip"), {"a.txt", "ملف.txt"})
        code, out = self.ftool("archive", "nope.txt", "-o", "n.zip")
        self.assertEqual(code, 1)
        self.assertIn("nope.txt", out)
        self.assertFalse((self.dir / "n.zip").exists())

    def test_everything_excluded_is_rejected(self) -> None:
        self.make_tree()
        code, out = self.ftool("archive", "proj/b.tmp", "-e", "*.tmp", "-o", "z.zip")
        self.assertEqual(code, 1)
        self.assertIn("Nothing to archive", out)

    def test_level_zero_stores(self) -> None:
        self.make_tree()
        self.assertEqual(self.ftool("archive", "proj", "-l", "0", "-o", "s.zip")[0], 0)
        with zipfile.ZipFile(self.dir / "s.zip") as z:
            self.assertTrue(all(i.compress_type == zipfile.ZIP_STORED for i in z.infolist()))


class ExtractTests(CliTestCase):
    def build_zip(self) -> None:
        self.make_tree()
        self.ftool("archive", "proj", "-o", "p.zip", "-q")

    def test_list_only_writes_nothing(self) -> None:
        self.build_zip()
        code, out = self.ftool("extract", "p.zip", "--list")
        self.assertEqual(code, 0)
        self.assertIn("proj/a.txt", out)
        self.assertFalse((self.dir / "proj_extracted").exists())

    def test_conflict_options(self) -> None:
        self.build_zip()
        self.ftool("extract", "p.zip", "-t", "r", "-q")
        (self.dir / "r/proj/a.txt").write_text("CHANGED", encoding="utf-8")

        self.ftool("extract", "p.zip", "-t", "r", "-s")
        self.assertEqual((self.dir / "r/proj/a.txt").read_text(encoding="utf-8"), "CHANGED")

        self.ftool("extract", "p.zip", "-t", "r", "-r")
        self.assertEqual((self.dir / "r/proj/a_1.txt").read_text(encoding="utf-8"), "hello")
        self.assertEqual((self.dir / "r/proj/a.txt").read_text(encoding="utf-8"), "CHANGED")

        self.ftool("extract", "p.zip", "-t", "r", "-o")
        self.assertEqual((self.dir / "r/proj/a.txt").read_text(encoding="utf-8"), "hello")

    def test_default_conflict_prompts_the_user(self) -> None:
        self.build_zip()
        self.ftool("extract", "p.zip", "-t", "r", "-q")
        (self.dir / "r/proj/a.txt").write_text("CHANGED", encoding="utf-8")
        # a.txt -> overwrite; remaining files -> default (skip) because stdin ends
        code, _ = self.ftool("extract", "p.zip", "-t", "r", stdin="o\n")
        self.assertEqual(code, 0)
        self.assertEqual((self.dir / "r/proj/a.txt").read_text(encoding="utf-8"), "hello")

    def test_quit_at_prompt_cancels(self) -> None:
        self.build_zip()
        self.ftool("extract", "p.zip", "-t", "r", "-q")
        code, out = self.ftool("extract", "p.zip", "-t", "r", stdin="q\n")
        self.assertEqual(code, 1)
        self.assertIn("CANCELLED", out)

    def test_dry_run_writes_nothing(self) -> None:
        self.build_zip()
        code, out = self.ftool("extract", "p.zip", "-t", "r", "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("SIMULATION", out)
        self.assertFalse((self.dir / "r").exists())

    def test_path_traversal_is_blocked(self) -> None:
        with zipfile.ZipFile(self.dir / "evil.zip", "w") as z:
            z.writestr("../evil.txt", "x")
            z.writestr("/abs.txt", "x")
            z.writestr("..\\win.txt", "x")
            z.writestr("ok.txt", "fine")
        code, out = self.ftool("extract", "evil.zip", "-t", "sandbox")
        self.assertEqual(code, 1)
        self.assertTrue((self.dir / "sandbox/ok.txt").exists())
        for bad in ("evil.txt", "abs.txt", "win.txt"):
            self.assertFalse((self.dir / bad).exists())
            self.assertFalse((self.dir / "sandbox" / bad).exists())
        self.assertIn("Blocked unsafe entry", out)

    def test_bad_inputs(self) -> None:
        (self.dir / "fake.zip").write_text("not a zip", encoding="utf-8")
        code, out = self.ftool("extract", "fake.zip")
        self.assertEqual(code, 1)
        self.assertIn("Unsupported", out)

        (self.dir / "broken.zip").write_bytes(b"PK\x03\x04" + b"\x00" * 30)
        code, out = self.ftool("extract", "broken.zip")
        self.assertEqual(code, 1)
        self.assertIn("damaged", out)

        code, out = self.ftool("extract", "missing.zip")
        self.assertEqual(code, 1)
        self.assertIn("not found", out.lower())

    def test_conflicting_flags_exit_code_2(self) -> None:
        code, out = self.ftool("extract", "x.zip", "-o", "-s")
        self.assertEqual(code, 2)
        self.assertIn("only one", out)

    def test_quiet_hides_success_but_not_errors(self) -> None:
        self.make_tree()
        code, out = self.ftool("archive", "proj", "-o", "q.zip", "-q")
        self.assertEqual((code, out), (0, ""))
        code, out = self.ftool("archive", "nope", "-q")
        self.assertEqual(code, 1)
        self.assertIn("not found", out.lower())


@unittest.skipIf(os.name == "nt", "uses a fake POSIX 'rar' script")
class RarEngineTests(CliTestCase):
    def fake_rar(self) -> Path:
        bin_dir = self.dir / "bin"
        bin_dir.mkdir()
        script = bin_dir / "rar"
        script.write_text(
            '#!/bin/sh\n'
            'echo "ARGS $*" >> "$FAKE_RAR_LOG"\n'
            'echo "CWD $(pwd)" >> "$FAKE_RAR_LOG"\n'
            'printf "Rar!\\032\\007\\000" > "$5"\n'
        )
        script.chmod(script.stat().st_mode | stat.S_IEXEC)
        return bin_dir

    def test_rar_is_unavailable_without_program(self) -> None:
        with mock.patch.dict(os.environ, {"PATH": str(self.dir)}):
            self.assertIn("rar", (RarEngine().write_unavailable_reason() or "").lower())
            self.make_tree()
            code, out = self.ftool("archive", "proj", "-f", "rar")
        self.assertEqual(code, 1)
        self.assertIn("WinRAR", out)

    def test_rar_command_line(self) -> None:
        self.make_tree()
        log = self.dir / "rar.log"
        env = {"PATH": f"{self.fake_rar()}{os.pathsep}{os.environ['PATH']}", "FAKE_RAR_LOG": str(log)}
        with mock.patch.dict(os.environ, env):
            code, _ = self.ftool("archive", "proj", "-e", "node_modules", "-l", "9", "-o", "o.rar")
        self.assertEqual(code, 0)
        text = log.read_text(encoding="utf-8")
        self.assertIn("-m5", text)
        self.assertIn("proj/a.txt", text)
        self.assertIn("proj/ملف.txt", text)
        self.assertNotIn("node_modules", text)
        self.assertIn(f"CWD {self.dir}", text)  # names are stored relative to the source's parent
        self.assertTrue((self.dir / "o.rar").exists())
        self.assertFalse(list(self.dir.glob("*.ftool-tmp*")))

    def test_rar_signature_detection(self) -> None:
        (self.dir / "a.rar").write_bytes(b"Rar!\x1a\x07\x00rest")
        (self.dir / "b.rar").write_bytes(b"nope")
        self.assertTrue(RarEngine().matches(self.dir / "a.rar"))
        self.assertFalse(RarEngine().matches(self.dir / "b.rar"))
        self.assertTrue(ZipEngine().matches(self.dir / "a.rar") is False)


if __name__ == "__main__":
    unittest.main()
