class RequestFactory:
    def __init__(self):
        self.factories={}
    def register(self,command_name,creator):
        self.factories[command_name]=creator
    def create(self,argv):
        creator=self.factories.get(argv.command)
        if creator is None:
            raise ValueError(
                f"Unknown command:{argv.command}"
            )
        return creator(argv)