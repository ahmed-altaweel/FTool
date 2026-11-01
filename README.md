# FTool

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Tests](https://img.shields.io/badge/tests-20%20passing-brightgreen)

أداة سطر أوامر (CLI) لإدارة الملفات بلغة Python:

- **`del`** حذف آمن: ينقل الملفات إلى سلة خاصة بالأداة بدل الحذف النهائي.
- **`archive`** ضغط الملفات والمجلدات إلى **ZIP** أو **RAR**.
- **`extract`** فك الضغط أو عرض محتويات الأرشيف مع حماية من الملفات الخبيثة.

مبنية بمعمارية طبقات (Presentation / Application / Domain / Infrastructure / Bootstrap).

## المميزات
- استبعاد ملفات بأنماط (`-e "*.tmp"`) ودعم wildcard مثل `*.txt`
- وضع المحاكاة `--dry-run` قبل أي عملية
- حماية من Path Traversal (zip-slip) عند فك الضغط
- سياسات تعارض عند الفك: استبدال / تخطي / إعادة تسمية / سؤال
- دعم أسماء الملفات العربية
- رموز خروج واضحة (0 نجاح، 1 فشل، 2 خيارات خاطئة)

## التثبيت

```bash
git clone https://github.com/<USERNAME>/FTool.git
cd FTool
pip install -e .
```

لقراءة ملفات RAR أيضًا:

```bash
pip install -e ".[rar]"
```

> إنشاء RAR يحتاج برنامج `rar` (من WinRAR). قراءة RAR تحتاج WinRAR أو unrar أو 7-Zip.

## الاستخدام

### ضغط
```bash
ftool archive proj                                      # proj.zip
ftool archive a.txt b.txt -o backup.zip
ftool archive "*.txt" -o texts.zip
ftool archive proj -e node_modules -e "*.tmp" -o proj.zip
ftool archive proj -f rar -l 9 -o proj.rar
ftool archive proj --dry-run
ftool archive proj -o proj.zip --force                  # استبدال أرشيف موجود
```

| الخيار | المعنى |
|---|---|
| `-o, --output` | مسار الأرشيف (الصيغة تُؤخذ من الامتداد إن لم تُحدَّد) |
| `-f, --format` | `zip` أو `rar` (الافتراضي zip) |
| `-l, --level` | 0 (بلا ضغط) إلى 9 (أقصى ضغط)، الافتراضي 6 |
| `-e, --exclude` | نمط استبعاد، يمكن تكراره |
| `--force` | استبدال الأرشيف الناتج إن وُجد |
| `-d, --dry-run` | محاكاة بلا تنفيذ |
| `-q, --quiet` | إخفاء رسائل النجاح |

### فك الضغط
```bash
ftool extract proj.zip --list         # عرض المحتويات
ftool extract proj.zip -t out         # فك إلى مجلد out
ftool extract proj.zip -t out -o      # استبدال الموجود
ftool extract proj.zip -t out -s      # تخطي الموجود
ftool extract proj.zip -t out -r      # إبقاء النسختين (a.txt و a_1.txt)
ftool extract proj.zip --dry-run
```

بدون `-o/-s/-r` تسأل الأداة عند كل ملف موجود: `o` استبدال، `s` تخطي، `r` إعادة تسمية، `q` إيقاف.

### حذف
```bash
ftool del f.txt            # نقل إلى سلة الأداة (مع تأكيد)
ftool del -f f.txt         # بدون تأكيد
ftool del -d -r my_folder  # حذف مجلد
ftool del --final f.txt    # حذف نهائي
```

لأي أمر: `ftool <command> --help`

## الاختبارات
```bash
ftool del -r my_folder
```

> **ملاحظة:** يجب تنفيذ أوامر `ftool` من Terminal بعد تثبيت المشروع باستخدام `pip install -e .`.
