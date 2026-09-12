from dataclasses import dataclass
from pathlib import Path
from Application.Common.BaseCommandOptions import BaseCommandOptions

# 1. خيارات الأمر (تشبه DeleteOptions لكن خاصة بالنقل)
@dataclass
class MoveOptions(BaseCommandOptions):
    dry_run: bool = False
    force: bool = False      # لتجاوز التأكيد واستبدال الملفات الموجودة
    quiet: bool = False

# 2. وسائط الأمر (المصدر والوجهة)
@dataclass
class MoveRequestArgs:
    source: Path
    destination: Path
    options: MoveOptions

# 3. الطلب النهائي الذي ستمرره للتطبيق
@dataclass
class MoveRequest:
    request: MoveRequestArgs
