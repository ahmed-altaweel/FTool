from pathlib import Path

from Application.Common.CommandStatus import CommandStatus
from Application.Create.CreateRequest import CreateOptions
from Application.Create.CreateResult import CreateResult
from Application.Create.CreateValidator import CreateValidator
from Domain.Create.TargetCreateHandler import TargetCreateHandler


# Architecture: Create use-case executor.
# Layer: Application.Create.
# Role: Validates, selects the target handler, and performs or simulates creation.
class CreateExecutor:
    def __init__(
        self,
        file_handler: TargetCreateHandler,
        folder_handler: TargetCreateHandler,
        validator: CreateValidator,
    ) -> None:
        self._file_handler = file_handler
        self._folder_handler = folder_handler
        self._validator = validator

    def execute(self, path: Path, options: CreateOptions) -> CreateResult:
        errors = self._validator.validate(path, options)
        if errors:
            return CreateResult(
                status=CommandStatus.INVALID,
                paths=[str(path)],
                violations=errors,
            )

        handler = self._file_handler if options.create_file else self._folder_handler

        if options.dry_run:
            return CreateResult(
                status=CommandStatus.SUCCESS,
                paths=[str(path)],
                is_dry_run=True,
            )

        try:
            handler.create(path, parents=options.parents)
        except FileExistsError:
            return CreateResult(
                status=CommandStatus.INVALID,
                paths=[str(path)],
                error_path=str(path),
            )
        except FileNotFoundError:
            return CreateResult(
                status=CommandStatus.NOT_FOUND,
                paths=[str(path)],
                error_path=str(path),
            )
        except PermissionError:
            return CreateResult(
                status=CommandStatus.INVALID,
                paths=[str(path)],
                error_path=str(path),
            )

        return CreateResult(
            status=CommandStatus.SUCCESS,
            paths=[str(path)],
        )