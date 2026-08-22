
from Application.Common.Handler import CommandHandler
class DeleteHandler(CommandHandler):
    def __init__(self,target_resolver,executor):
        self.target_resolver=target_resolver
        self.executor=executor
    def execute(self,request):
        request=request.request
        target_solver=self.target_resolver.resolve(request.path,request.options.recursive_search)
        return self.executor.execute(request.path,target_solver,request.options)

