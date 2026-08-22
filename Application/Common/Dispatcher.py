class Dispatcher:
    def __init__(self):
        self.handlers={}
    def register(self,request_type,handler):
        self.handlers[request_type]=handler
    def dispatch(self,request):
        handler=self.handlers[type(request)]
        return handler.execute(request)

