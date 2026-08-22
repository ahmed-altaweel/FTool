import argparse
class ParserBuilder:
    def __init__(self):
        self.parser=argparse.ArgumentParser(
            prog='ftool'
        )
        self.commands=self.parser.add_subparsers(
            dest='command',
            required=True
        )
    def add(self,command_builder):
        command_builder.build(self.commands)
        return self
    def build(self):
        return self.parser