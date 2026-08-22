from Application.Presenters.ResultPresenter import ResultPresenter

class CliResultPresenter(ResultPresenter):
    def __init__(self,formatters:dict):
        self.formatters=formatters
    def present(self,result)->str:
        formatter=self.formatters.get(type(result))
        if formatter is None:
            return f"...Unknown result type: {type(result).__name__}..."
        return formatter.format(result)