from Infrastructure.Terminal.Output.base import OutputPolicy
class NormalOutputPolicy(OutputPolicy):
    def print_result(self, text):
        print(text)
    def print_error(self, text: str) -> None:
        print(text)