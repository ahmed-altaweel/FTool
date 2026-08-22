from Application.Common.Dispatcher import Dispatcher
class ApplicationBuilder:
    def __init__(self):
        self.dispatcher=Dispatcher()
    def add_command(self,module):
        request_type,handler=module.build()
        self.dispatcher.register(request_type,handler)
        return self
    def build(self):
        return self.dispatcher