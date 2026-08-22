from Infrastructure.Terminal.Output.base import OutputPolicy
class QuietOutputPolicy(OutputPolicy):
    def print_result(self,text):
        return
    def print_error(self, text: str) -> None:
        print(text)