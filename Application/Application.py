from Application.Common.CommandStatus import CommandStatus


class Application:
    def __init__(self,dispatcher,request_factory,presenter,output_policy_resolver):
        self.dispatcher=dispatcher
        self.request_factory=request_factory
        self.presenter=presenter
        self.output_policy_resolver=output_policy_resolver
    def run(self,args):
        request=self.request_factory.create(args)
        result =self.dispatcher.dispatch(request)
        text=self.presenter.present(result)
        quiet=getattr(request.request.options,'quiet',False)
        output_policy=self.output_policy_resolver.resolve(quiet)
        if result.status==CommandStatus.INVALID:
            output_policy.print_error(text)
        else:
            output_policy.print_result(text)