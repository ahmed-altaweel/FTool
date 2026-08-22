from Infrastructure.Terminal.Confirmation.base import ConfirmationPolicy
class RequiredConfirmationPolicy(ConfirmationPolicy):
    def confirm(self, paths,options,preview_formatter):
        preview = preview_formatter.format(paths, options)
        print(preview)
        return input("Are you sure?[Y/N]").strip().upper()=='Y'