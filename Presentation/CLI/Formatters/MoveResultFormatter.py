from Application.Move.MoveResult import MoveResult
from Application.Presenters.ResultFormatter import ResultFormatter

class MoveResultFormatter(ResultFormatter):
    def format(self, result: MoveResult) -> str:
        # إذا كان الـ Quiet مفعلاً، نطبع فقط في حالة الخطأ
        # ولكن الـ Formatter لا يعرف الـ Quiet، الـ Presenter هو الذي يقرر.
        # هنا نجهز النص فقط.
        
        if result.status == "SUCCESS":
            if "[simulation]" in result.message:
                return f"🔍 {result.message}"
            return f"✅ {result.message}"
        
        elif result.status == "SOURCE_NOT_FOUND":
            return f"❌ Error: {result.message}"
        
        elif result.status == "DESTINATION_EXISTS":
            return f"⚠️ warning: {result.message}"
        
        elif result.status == "SAME_PATH":
            return f"⛔ forbidden: {result.message}"
        
        elif result.status == "PERMISSION_DENIED":
            return f"🔒 powers: {result.message}"
        
        else:
            return f"❌ to fail: {result.message}"

            