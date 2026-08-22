from Application.Common.CommandStatus import CommandStatus
from Application.Delete.DeleteExecutionStrategy.DryRunDeleteExecutor import DryRunDeleteExecutor
from Application.Delete.DeleteExecutionStrategy.RealDeleteExecutor import RealDeleteExecutor
from Application.Delete.DeleteModes.PermanentDeleteMode import PermanentDeleteMode
from Application.Delete.DeleteModes.TrashDeleteMode import TrashDeleteMode
from Application.Delete.DeleteResult import DeleteResult
from Infrastructure.Terminal.Confirmation.RequiredConfirmationPolicy import RequiredConfirmationPolicy
from Infrastructure.Terminal.Confirmation.SkippedConfirmationPolicy import SkippedConfirmationPolicy
class DeleteExecutor:
    def __init__(self,delete_handlers,preview_formatter,validator,trash_delete_mode):
        self.delete_handlers=delete_handlers
        self.preview_formatter=preview_formatter
        self.validator=validator
        self.trash_delete_mode=trash_delete_mode
    def execute(self,path,paths,options):

        if len(paths) <=0:
            return DeleteResult(CommandStatus.NOT_FOUND,paths=[],error_path=path)
        violations=self.validator.validate(paths,options)
        if violations:
            return DeleteResult(CommandStatus.INVALID,paths=paths,violations=violations)
        delete_executor=self.select_delete_executor(options)
        delete_mode=self.select_delete_mode(options)
        
        
        if(not self.confirm(options,paths)):
            return DeleteResult(CommandStatus.CANCELLED,paths=paths)


        delete_executor.execute(paths,delete_mode)
        return DeleteResult(CommandStatus.SUCCESS,paths=paths,is_dry_run=options.dry_run)

    def select_delete_executor(self,options):
        delete_executor=RealDeleteExecutor(self.delete_handlers)   
        if options.dry_run:
           delete_executor=DryRunDeleteExecutor(self.delete_handlers)
       
        return delete_executor
    
    def select_delete_mode(self,options):
        delete_mode=PermanentDeleteMode()
      
        if not options.final_delete:
            delete_mode=self.trash_delete_mode

        return delete_mode
    
    def confirm(self,options,paths):
        confirm=RequiredConfirmationPolicy()
        if options.force:
            confirm=SkippedConfirmationPolicy()
        return confirm.confirm(paths,options,self.preview_formatter)
