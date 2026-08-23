from Application.Common.CommandStatus import CommandStatus
from Application.Confirmation.ConfirmaitonPolicy import ConfirmationPolicy
from Application.Delete.DeleteExecutionStrategy.DryRunDeleteExecutor import DryRunDeleteExecutor
from Application.Delete.DeleteExecutionStrategy.RealDeleteExecutor import RealDeleteExecutor
from Application.Delete.DeleteExecutionStrategy.base import DeleteExecutorStrategy
from Application.Delete.DeleteModes.PermanentDeleteMode import PermanentDeleteMode
from Application.Delete.DeleteModes.TrashDeleteMode import TrashDeleteMode
from Application.Delete.DeleteModes.base import DeleteMode
from Application.Delete.DeleteResult import DeleteResult
from Application.Delete.DeleteRequest import DeleteOptions
from Application.Delete.DeleteValidator import DeleteValidator
from Application.Presenters.PreviewFormatter import PreviewFormatter
from Domain.Delete.TargetDeleteHandler import TargetDeleteHandler
from Infrastructure.Terminal.Confirmation.RequiredConfirmationPolicy import RequiredConfirmationPolicy
from Infrastructure.Terminal.Confirmation.SkippedConfirmationPolicy import SkippedConfirmationPolicy

# Architecture: Delete use-case coordinator.
# Layer: Application.Delete.
# Role: Performs validation, confirmation, strategy/mode selection, and result construction.
# Dependencies: Target handlers, validator, preview formatter, and trash mode.
class DeleteExecutor:
    def __init__(
        self,
        delete_handlers: list[TargetDeleteHandler],
        preview_formatter: PreviewFormatter,
        validator: DeleteValidator,
        trash_delete_mode: TrashDeleteMode,
       permananent_delete_mode:PermanentDeleteMode,
       required_confirmation_policy:RequiredConfirmationPolicy,
       skipped_confirmation_policy:SkippedConfirmationPolicy
    ) -> None:
        self.delete_handlers: list[TargetDeleteHandler] = delete_handlers
        self.preview_formatter: PreviewFormatter = preview_formatter
        self.validator: DeleteValidator = validator
        self.trash_delete_mode: TrashDeleteMode = trash_delete_mode
        self.permananent_delete_mode:PermanentDeleteMode=permananent_delete_mode
        self.required_confirmation_policy:RequiredConfirmationPolicy=required_confirmation_policy
        self.skipped_confirmation_policy:SkippedConfirmationPolicy=skipped_confirmation_policy
    
    def execute(self, path: str, paths: list[str], options: DeleteOptions) -> DeleteResult:

        if len(paths) <=0:
            return DeleteResult(CommandStatus.NOT_FOUND,paths=[],error_path=path)
        violations=self.validator.validate(paths,options)
        if violations:
            return DeleteResult(CommandStatus.INVALID,paths=paths,violations=violations)
        delete_executor: DeleteExecutorStrategy = self.select_delete_executor(options)
        delete_mode: DeleteMode = self.select_delete_mode(options)
        
        
        if(not self.confirm(options,paths)):
            return DeleteResult(CommandStatus.CANCELLED,paths=paths)


        delete_executor.execute(paths,delete_mode)
        return DeleteResult(CommandStatus.SUCCESS,paths=paths,is_dry_run=options.dry_run)

    def select_delete_executor(self, options: DeleteOptions) -> DeleteExecutorStrategy:
        delete_executor: DeleteExecutorStrategy = RealDeleteExecutor(
            self.delete_handlers
        )
        if options.dry_run:
            delete_executor = DryRunDeleteExecutor(self.delete_handlers)

        return delete_executor

    def select_delete_mode(self, options: DeleteOptions) -> DeleteMode:
        delete_mode: DeleteMode = self.permananent_delete_mode

        if not options.final_delete:
            delete_mode = self.trash_delete_mode

        return delete_mode
    
    def confirm(self, options: DeleteOptions, paths: list[str]) -> bool:
        confirm: ConfirmationPolicy =self.required_confirmation_policy
        if options.force:
            confirm=self.skipped_confirmation_policy
        return confirm.confirm(paths,options,self.preview_formatter)
