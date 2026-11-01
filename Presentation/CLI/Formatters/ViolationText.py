from Application.Archive.ArchiveResult import ArchiveViolation

_TEXT = {
    "SOURCE_UNREADABLE": "No read permission for:",
    "SOURCE_HAS_NO_NAME": "Cannot archive a path with no name (such as a drive root):",
    "DUPLICATE_NAME": "Two sources would be stored under the same name:",
    "NOTHING_TO_ARCHIVE": "Nothing to archive (everything was excluded or the sources are empty).",
    "OUTPUT_IS_DIRECTORY": "The output path is a folder:",
    "OUTPUT_EXISTS": "The output archive already exists (use --force to replace it, or choose another -o):",
    "OUTPUT_NOT_WRITABLE": "Cannot write to:",
    "UNSUPPORTED_FORMAT": "Unsupported or unrecognized archive format. Supported: zip, rar.",
    "FORMAT_MISMATCH": "Output extension does not match the chosen format.",
    "ARCHIVE_NOT_FOUND": "Archive not found:",
    "NOT_A_FILE": "Not a file:",
    "ARCHIVE_UNREADABLE": "No read permission for archive:",
    "TARGET_IS_FILE": "The target is a file, not a folder:",
    "TARGET_NOT_WRITABLE": "Cannot write to target:",
    "CORRUPTED_ARCHIVE": "The archive is damaged or cannot be read.",
}


def violation_lines(violation: ArchiveViolation) -> list[str]:
    lines = [f"Error : {_TEXT.get(violation.reason, violation.reason)}"]
    lines += [f" - {path}" for path in violation.paths]
    if violation.detail:
        lines.append(f"Detail: {violation.detail}")
    return lines
