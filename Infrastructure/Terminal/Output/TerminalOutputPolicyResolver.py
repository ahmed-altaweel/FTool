from Application.Output.OutputPolicyResolver import OutputPolicyResolver


class TerminalOutputPolicyResolver(OutputPolicyResolver):
    def __init__(self, normal, quiet):
        self._normal = normal
        self._quiet = quiet

    def resolve(self, quiet: bool):
        return self._quiet if quiet else self._normal
