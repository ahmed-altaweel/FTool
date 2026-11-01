from Application.Archive.ArchiveEngine import ArchiveEngineRegistry
from Application.Archive.ArchiveExecutionStrategy.DryRunArchiveExecutor import DryRunArchiveExecutor
from Application.Archive.ArchiveExecutionStrategy.DryRunExtractExecutor import DryRunExtractExecutor
from Application.Archive.ArchiveExecutionStrategy.RealArchiveExecutor import RealArchiveExecutor
from Application.Archive.ArchiveExecutionStrategy.RealExtractExecutor import RealExtractExecutor
from Application.Archive.ArchiveExecutor import ArchiveExecutor
from Application.Archive.ArchiveHandler import ArchiveHandler
from Application.Archive.ArchivePlanner import ArchivePlanner
from Application.Archive.ArchiveRequest import ArchiveRequest, ExtractRequest
from Application.Archive.ArchiveResult import ArchiveResult, ExtractResult
from Application.Archive.ArchiveValidator import ArchiveValidator
from Application.Archive.ExtractExecutor import ExtractExecutor
from Application.Archive.ExtractHandler import ExtractHandler
from Application.Common.Dispatcher import Dispatcher
from Application.Common.ModuleBuilder import ModuleBuilder
from Application.Common.Result import CommandResult
from Application.Presenters.ResultFormatter import ResultFormatter
from Infrastructure.Compression.RarEngine import RarEngine
from Infrastructure.Compression.ZipEngine import ZipEngine
from Infrastructure.FileSystem.FileInspector.OsFileSystemInspector import OsFileSystemInspector
from Infrastructure.FileSystem.Resolver.PatternResolver import PatternResolver
from Infrastructure.FileSystem.Resolver.TargetResolver import TargetResolver
from Infrastructure.FileSystem.Scanner.OsSourceScanner import OsSourceScanner
from Infrastructure.Terminal.Confirmation.PromptConflictPolicy import PromptConflictPolicy
from Infrastructure.Terminal.IOStream import IOStream
from Presentation.CLI.Formatters.ArchiveResultFormatter import ArchiveResultFormatter
from Presentation.CLI.Formatters.ExtractResultFormatter import ExtractResultFormatter
from Presentation.CLI.Request.RequestCreator.ArchiveRequestCreator import ArchiveRequestCreator
from Presentation.CLI.Request.RequestCreator.ExtractRequestCreator import ExtractRequestCreator
from Presentation.CLI.Request.RequestFactory import RequestFactory


# Architecture: Archive-module composition root.
# Layer: Bootstrap.
# Role: Wires engines, planner, validator, strategies and handlers, then registers `archive` and `extract`.
class ArchiveModuleBuilder(ModuleBuilder):
    def build(
        self,
        dispatcher: Dispatcher,
        request_factory: RequestFactory,
        formatters: dict[type[CommandResult], ResultFormatter],
    ) -> None:
        fs_inspector = OsFileSystemInspector()
        registry = ArchiveEngineRegistry([ZipEngine(), RarEngine()])
        validator = ArchiveValidator(fs_inspector)

        archive_executor = ArchiveExecutor(
            registry,
            ArchivePlanner(OsSourceScanner()),
            validator,
            RealArchiveExecutor(),
            DryRunArchiveExecutor(),
        )
        extract_executor = ExtractExecutor(
            registry,
            validator,
            RealExtractExecutor(fs_inspector),
            DryRunExtractExecutor(fs_inspector),
            PromptConflictPolicy(IOStream()),
        )

        target_resolver = TargetResolver(PatternResolver())
        dispatcher.register(
            ArchiveRequest, ArchiveHandler(target_resolver, fs_inspector, validator, archive_executor)
        )
        dispatcher.register(ExtractRequest, ExtractHandler(extract_executor))

        request_factory.register("archive", ArchiveRequestCreator())
        request_factory.register("extract", ExtractRequestCreator())

        formatters[ArchiveResult] = ArchiveResultFormatter()
        formatters[ExtractResult] = ExtractResultFormatter()
