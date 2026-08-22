from Infrastructure.Terminal.Confirmation.base import ConfirmationPolicy
class SkippedConfirmationPolicy(ConfirmationPolicy):
    def confirm(self,text, paths):
        return True

