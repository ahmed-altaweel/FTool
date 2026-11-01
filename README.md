# FTool

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

أداة **FTool** أداة سطر أوامر (CLI) لإدارة الملفات والمجلدات بلغة Python، تركّز على **الأمان** (سلة محذوفات خاصة، تأكيد قبل الحذف، وضع محاكاة) وعلى **سهولة الاستخدام**.

---

## الفهرس

1. [نظرة عامة](#نظرة-عامة)
2. [التثبيت](#التثبيت)
3. [البدء السريع](#البدء-السريع)
4. [مرجع الأوامر](#مرجع-الأوامر)
   - [`del` — الحذف](#del--الحذف)
   - [`restore` — الاستعادة](#restore--الاستعادة)
   - [`archive` — الضغط](#archive--الضغط)
   - [`extract` — فك الضغط](#extract--فك-الضغط)
   - [`copy` — النسخ](#copy--النسخ)
   - [`move` — النقل](#move--النقل)
   - [`create` — الإنشاء](#create--الإنشاء)
5. [الخيارات المشتركة](#الخيارات-المشتركة)
6. [رموز الخروج](#رموز-الخروج)
7. [سلة المحذوفات](#سلة-المحذوفات)
8. [بنية المشروع](#بنية-المشروع)
9. [إضافة أمر جديد](#إضافة-أمر-جديد)

---

## نظرة عامة

| الأمر | الوظيفة | يدعم `--dry-run` | يطلب تأكيدًا |
|---|---|:---:|:---:|
| `del` | حذف ملفات/مجلدات (إلى السلة افتراضيًا) | ✅ | ✅ |
| `restore` | استعادة عنصر محذوف من السلة | ✅ | ❌ |
| `archive` | ضغط إلى ZIP أو RAR | ✅ | ❌ |
| `extract` | فك ضغط أو عرض محتويات أرشيف | ✅ | عند تعارض الملفات |
| `copy` | نسخ ملف أو مجلد | ❌ | مع `-i` |
| `move` | نقل ملف أو مجلد | ✅ | ❌ |
| `create` | إنشاء ملف أو مجلد فارغ | ✅ | ❌ |

**المميزات العامة**

- سلة محذوفات خاصة بالأداة مع إمكانية الاستعادة.
- وضع المحاكاة `--dry-run` لمعرفة ما سيحدث دون تغيير أي شيء.
- دعم الأنماط (wildcards) مثل `*.txt`.
- حماية من **Path Traversal (zip-slip)** عند فك الضغط.
- كتابة آمنة عبر ملفات مؤقتة، فلا تبقى ملفات ناقصة عند الفشل.
- دعم أسماء الملفات العربية.
- رموز خروج واضحة تصلح للاستخدام داخل السكربتات.

---

## التثبيت

**المتطلبات:** Python 3.10 أو أحدث.

```bash
git clone https://github.com/<USERNAME>/FTool.git
cd FTool
pip install -e .
```

لقراءة ملفات **RAR**:

```bash
pip install -e ".[rar]"
```

| العملية | المتطلب الإضافي |
|---|---|
| إنشاء RAR | برنامج `rar` (يأتي مع WinRAR) |
| قراءة/فك RAR | حزمة `rarfile` + أحد: WinRAR أو `unrar` أو 7-Zip |
| ZIP | لا شيء (المكتبة القياسية) |

للتأكد من نجاح التثبيت:

```bash
ftool --help
```

> يجب تنفيذ أوامر `ftool` من الـ Terminal بعد التثبيت بـ `pip install -e .`

---

## البدء السريع

```bash
ftool create notes.txt --file          # إنشاء ملف
ftool copy notes.txt backup.txt        # نسخه
ftool archive notes.txt backup.txt     # ضغطهما في archive_<التاريخ>.zip
ftool del notes.txt                    # حذفه إلى السلة (مع تأكيد)
ftool restore notes.txt                # استعادته
```

الصيغة العامة:

```bash
ftool <command> [options] <arguments>
ftool <command> --help
```

---

## مرجع الأوامر

### `del` — الحذف

ينقل الملفات والمجلدات إلى **سلة FTool** افتراضيًا، ويمكن الحذف النهائي عند الطلب.

```bash
ftool del [-d] [-r] [-f] [-q] [--dry-run] [--final] <path>
```

| الخيار | المعنى |
|---|---|
| `path` | ملف أو مجلد أو نمط مثل `*.log` |
| `-d, --delete-folder` | السماح بحذف المجلدات (بدونه تُرفض المجلدات) |
| `-r, --recursive` | البحث عن النمط داخل المجلدات الفرعية أيضًا |
| `-f, --force` | حذف بدون رسالة تأكيد |
| `-q, --quiet` | إخفاء رسائل النجاح (تبقى الأخطاء) |
| `--dry-run` | عرض ما سيُحذف دون حذف |
| `--final` | حذف **نهائي** لا يمكن استعادته |

**أمثلة**

```bash
ftool del report.txt                 # إلى السلة مع تأكيد [Y/N]
ftool del -f report.txt              # بدون تأكيد
ftool del "*.tmp"                    # كل ملفات tmp في المجلد الحالي
ftool del -r "*.tmp"                 # ... وفي المجلدات الفرعية
ftool del -d old_folder              # حذف مجلد
ftool del --dry-run -d old_folder    # محاكاة فقط
ftool del --final report.txt         # حذف نهائي
```

**ملاحظات**

- المجلدات تتطلب `-d` وإلا ظهرت الحالة `REJECTED`.
- عند عدم وجود أي هدف مطابق تظهر الحالة `NotFound`.
- عند الإجابة بغير `Y` على سؤال التأكيد تُلغى العملية (`CANCELLED`).

---

### `restore` — الاستعادة

يعيد عنصرًا حُذف إلى السلة إلى مكانه الأصلي. إذا حُذف المسار نفسه أكثر من مرة تُستعاد **آخر نسخة** محذوفة.

```bash
ftool restore [-l] [--dry-run] [-q] [path]
```

| الخيار | المعنى |
|---|---|
| `path` | المسار الأصلي للعنصر المحذوف |
| `-l, --list` | عرض محتويات السلة (الأحدث أولًا) |
| `--dry-run` | عرض ما سيُستعاد دون تنفيذ |
| `-q, --quiet` | إخفاء رسائل النجاح |

**أمثلة**

```bash
ftool restore --list
ftool restore report.txt
ftool restore --dry-run report.txt
```

**حالات الرفض**

| السبب | المعنى |
|---|---|
| `MISSING_PATH` | لم تُحدَّد مسارًا ولا `--list` |
| `NO_TRASH_ENTRY` | لا يوجد سجل في السلة لهذا المسار |
| `TRASHED_ITEM_MISSING` | السجل موجود لكن الملف اختفى من السلة |
| `DESTINATION_EXISTS` | المكان الأصلي مشغول؛ انقل العنصر الموجود أو غيّر اسمه أولًا |

---

### `archive` — الضغط

يضغط ملفات ومجلدات إلى **ZIP** أو **RAR**.

```bash
ftool archive [-o OUTPUT] [-f {zip,rar}] [-l 0-9] [-e PATTERN]... [--force] [-d] [-q] <sources...>
```

| الخيار | المعنى |
|---|---|
| `sources` | ملف أو أكثر، مجلدات، أو أنماط مثل `*.txt` |
| `-o, --output` | مسار الأرشيف الناتج |
| `-f, --format` | `zip` أو `rar` |
| `-l, --level` | `0` بدون ضغط ... `9` أقصى ضغط (الافتراضي `6`) |
| `-e, --exclude` | نمط استبعاد، يمكن تكراره |
| `--force` | استبدال الأرشيف الناتج إن كان موجودًا |
| `-d, --dry-run` | عرض ما سيُضغط دون إنشاء أرشيف |
| `-q, --quiet` | إخفاء رسائل النجاح |

**تحديد الصيغة والاسم**

- الصيغة: `-f` ← امتداد `-o` ← `zip`.
- الاسم الافتراضي: `<name>.zip` لمصدر واحد، و`archive_YYYYMMDD_HHMMSS.zip` لعدة مصادر.
- إن لم يكن لـ `-o` امتداد يُضاف امتداد الصيغة تلقائيًا.

**أمثلة**

```bash
ftool archive proj                               # proj.zip
ftool archive a.txt b.txt -o backup.zip
ftool archive "*.txt" -o texts.zip
ftool archive proj -e node_modules -e "*.tmp" -o proj.zip
ftool archive proj -f rar -l 9 -o proj.rar
ftool archive proj --dry-run
ftool archive proj -o proj.zip --force
```

**أنماط الاستبعاد `-e`**

| النمط | يستبعد |
|---|---|
| `*.tmp` | أي عنصر اسمه ينتهي بـ `.tmp` في أي مستوى |
| `node_modules` | أي مجلد بهذا الاسم |
| `src/cache` | المسار المحدد (يحتوي `/`) |

**ملاحظات**

- لا يُضاف الأرشيف الناتج إلى نفسه.
- روابط المجلدات (symlinks) لا تُتَّبع وتظهر ضمن التحذيرات.
- الملفات غير المقروءة تُتخطى مع تحذير.
- RAR لا يخزّن مجلدات فارغة فقط دون ملفات.
- كتابة RAR تحتاج برنامج `rar`، وإلا استخدم `--format zip`.

---

### `extract` — فك الضغط

يفك أرشيف ZIP/RAR أو يعرض محتوياته. تُكتشف الصيغة من **محتوى الملف** (magic bytes) لا من امتداده.

```bash
ftool extract [-t TARGET] [-o | -s | -r] [-l] [-d] [-q] <archive>
```

| الخيار | المعنى |
|---|---|
| `archive` | ملف الأرشيف |
| `-t, --target` | مجلد الوجهة (الافتراضي: المجلد الحالي) |
| `-o, --overwrite` | استبدال الملفات الموجودة |
| `-s, --skip` | تخطي الملفات الموجودة |
| `-r, --rename` | الإبقاء على النسختين (`a.txt` و`a_1.txt`) |
| `-l, --list` | عرض المحتويات فقط |
| `-d, --dry-run` | محاكاة دون كتابة |
| `-q, --quiet` | إخفاء رسائل النجاح |

> الخيارات `-o` و`-s` و`-r` **لا تجتمع**؛ اختر واحدًا فقط.

**أمثلة**

```bash
ftool extract proj.zip --list
ftool extract proj.zip -t out
ftool extract proj.zip -t out -o
ftool extract proj.zip -t out -s
ftool extract proj.zip -t out -r
ftool extract proj.zip --dry-run
```

**سياسة التعارض**

بدون `-o/-s/-r` تسأل الأداة عند كل ملف موجود:

| الإدخال | الإجراء |
|---|---|
| `o` | استبدال |
| `s` | تخطي (الافتراضي) |
| `r` | إعادة تسمية |
| `q` | إيقاف العملية |

**الأمان**

تُرفض العناصر ذات المسارات الخطرة وتُسجَّل ضمن الأخطاء، مثل المسارات المطلقة، أو التي تحتوي `..`، أو التي تبدأ بحرف قرص مثل `C:`.

---

### `copy` — النسخ

ينسخ ملفًا أو مجلدًا مع الحفاظ على البيانات الوصفية (التواريخ وغيرها).

```bash
ftool copy [-r] [-f] [-i] [-q] <source> <destination>
```

| الخيار | المعنى |
|---|---|
| `source` | الملف أو المجلد المصدر |
| `destination` | المسار الهدف |
| `-r, --recursive` | نسخ المجلدات بمحتوياتها (مطلوب للمجلدات) |
| `-f, --force` | الكتابة فوق الموجود دون تأكيد (ودمج المجلدات الموجودة) |
| `-i, --interactive` | السؤال قبل الاستبدال `[y/N]` |
| `-q, --quiet` | إخفاء رسائل النجاح |

**أمثلة**

```bash
ftool copy a.txt b.txt
ftool copy a.txt ./backup/              # النسخ داخل مجلد موجود
ftool copy -r project project_copy
ftool copy -r -f project project_copy   # دمج/استبدال
ftool copy -i a.txt b.txt               # سؤال قبل الاستبدال
```

**قواعد وحماية**

- نسخ مجلد بدون `-r` يُرفض.
- لا يمكن نسخ مجلد إلى داخل نفسه.
- لا يمكن نسخ ملف فوق نفسه.
- إذا كانت الوجهة مجلدًا موجودًا يُنسخ العنصر بداخله بنفس اسمه.
- نسخ ملف إلى وجهة موجودة بدون `-i` يستبدلها مباشرة.

---

### `move` — النقل

ينقل ملفًا أو مجلدًا. التنفيذ: نسخ ← تحقق من الوجهة ← حذف المصدر.

```bash
ftool move [-d] [-f] [-q] <source> <destination>
```

| الخيار | المعنى |
|---|---|
| `source` | المصدر |
| `destination` | الوجهة |
| `-d, --dry-run` | محاكاة دون نقل فعلي |
| `-f, --force` | استبدال الوجهة إن وُجدت |
| `-q, --quiet` | إخفاء رسائل النجاح |

**أمثلة**

```bash
ftool move a.txt docs/a.txt
ftool move old_dir new_dir
ftool move -d a.txt docs/a.txt     # محاكاة
ftool move -f a.txt docs/a.txt     # استبدال الموجود
```

**حالات الرفض**

| الحالة | المعنى |
|---|---|
| `SOURCE_NOT_FOUND` | المصدر غير موجود |
| `SAME_PATH` | المصدر والوجهة نفس المسار، أو نقل مجلد إلى داخل نفسه |
| `DESTINATION_EXISTS` | الوجهة موجودة؛ استخدم `--force` |
| `PERMISSION_DENIED` | مشكلة صلاحيات |

---

### `create` — الإنشاء

ينشئ ملفًا فارغًا أو مجلدًا. يجب تحديد **أحد** الخيارين `--file` أو `--folder`.

```bash
ftool create (--file | --folder) [--parents] [--force] [--dry-run] [-q] <path>
```

| الخيار | المعنى |
|---|---|
| `path` | المسار المراد إنشاؤه |
| `--file` | إنشاء ملف فارغ |
| `--folder` | إنشاء مجلد |
| `--parents` | إنشاء المجلدات الوسيطة المفقودة (للمجلدات فقط) |
| `--force` | السماح بوجود عنصر بنفس الاسم |
| `--dry-run` | محاكاة دون إنشاء |
| `-q, --quiet` | إخفاء رسائل النجاح |

**أمثلة**

```bash
ftool create notes.txt --file
ftool create docs --folder
ftool create a/b/c --folder --parents
ftool create notes.txt --file --dry-run
```

**حالات الرفض**

| السبب | المعنى |
|---|---|
| `KIND_REQUIRED` | لم يُحدَّد نوع العنصر (أو حُدِّد الاثنان) |
| `PARENTS_FILE_NOT_ALLOWED` | `--parents` مع `--file` |
| `ALREADY_EXISTS` | العنصر موجود ولم يُستخدم `--force` |
| `PARENT_NOT_FOUND` | المجلد الأب غير موجود (استخدم `--parents`) |
| `PARENT_NOT_A_DIRECTORY` | المسار الأب ليس مجلدًا |

---

## الخيارات المشتركة

| الخيار | الأوامر | الوصف |
|---|---|---|
| `-q, --quiet` | الكل | يخفي رسائل النجاح؛ تبقى رسائل الأخطاء |
| `--dry-run` | `del`, `restore`, `create` | محاكاة بلا أي تغيير |
| `-d, --dry-run` | `archive`, `extract`, `move` | نفس المحاكاة باختصار `-d` |
| `-f, --force` | `del`, `copy`, `move` (و`--force` فقط في `archive`, `create`) | تجاوز التأكيد/الاستبدال |

> ⚠️ الاختصار `-d` يختلف حسب الأمر: في `del` يعني **حذف المجلدات**، وفي `archive` و`extract` و`move` يعني **المحاكاة**. راجع `ftool <command> --help` عند الشك.

---

## رموز الخروج

| الرمز | المعنى |
|:---:|---|
| `0` | نجاح |
| `1` | فشل أو رفض أو إلغاء (NotFound / Invalid / Failure / Cancelled) |
| `2` | خيارات أو استخدام خاطئ |

مثال داخل سكربت:

```bash
ftool archive project -o project.zip --force -q || echo "فشل الضغط"
```

---

## سلة المحذوفات

- المسار الافتراضي: `~/.local/share/ftool/trash`
  - `entries/<uuid>/<name>` — العناصر المحذوفة.
  - `trash_registry.json` — سجل المسارات الأصلية وأوقات الحذف.
- يُنقل كل عنصر إلى مجلد فريد (`uuid`) فلا تتعارض الأسماء المتشابهة.
- الحذف بـ `--final` يتجاوز السلة نهائيًا.
- `ftool restore --list` يعرض المحتويات.

---

## بنية المشروع

يتبع المشروع معمارية طبقات، والاعتماد يتجه دائمًا نحو الداخل:

```
FTool/
├── Presentation/        # واجهة CLI
│   └── CLI/
│       ├── Parsers/         # تعريف الأوامر والخيارات (argparse)
│       ├── Request/         # تحويل Namespace إلى Request
│       ├── Formatters/      # تحويل Result إلى نص للمستخدم
│       ├── Presenters/
│       └── main.py          # نقطة الدخول
├── Application/         # حالات الاستخدام (Use Cases)
│   ├── Delete/  Restore/  Archive/  Copy/  Move/  Create/
│   │   └── Request · Handler · Executor · Validator · Result
│   ├── Common/              # Dispatcher, CommandStatus, العقود المشتركة
│   ├── Confirmation/ Output/ Presenters/
├── Domain/              # الكيانات والعقود (Trash, TrashEntry, TargetDeleteHandler)
├── Infrastructure/      # التنفيذ الفعلي
│   ├── FileSystem/          # Inspector, Resolver, Scanner, TargetHandler
│   ├── Compression/         # ZipEngine, RarEngine, StreamWriter
│   ├── Trash/               # MoveToTrash, JsonTrashRegistry, RestoreFromTrash
│   └── Terminal/            # IOStream, Confirmation, Output
└── Bootstrap/           # التجميع (Composition Root)
    ├── ApplicationBuilder.py
    ├── ParserBuilder.py
    └── ModulesBuilder/      # Delete/Archive/Copy/Restore ModuleBuilder
```

**مسار تنفيذ أي أمر**

```
argv ─▶ Parser ─▶ RequestCreator ─▶ Dispatcher ─▶ Handler ─▶ Executor
                                                                  │
 الطباعة ◀─ OutputPolicy ◀─ Formatter ◀─ Result ◀─────────────────┘
```

**أنماط التصميم المستخدمة**

| النمط | أين |
|---|---|
| Strategy | تنفيذ حقيقي/محاكاة (`Real*Executor` / `DryRun*Executor`)، وأوضاع الحذف |
| Adapter | `ZipEngine` و`RarEngine` خلف `ArchiveEngine` |
| Registry / Factory | `Dispatcher`, `RequestFactory`, `ArchiveEngineRegistry` |
| Ports & Adapters | `FileSystemInspector`, `TargetResolverPort`, `SourceScannerPort` |

---

## إضافة أمر جديد

1. **Application/`<Cmd>`/**: أنشئ `Request` و`Result` و`Executor` و`Handler`.
2. **Presentation/CLI/Parsers/**: أنشئ `<Cmd>ParserBuilder` بالخيارات.
3. **Presentation/CLI/Request/RequestCreator/**: أنشئ `<Cmd>RequestCreator`.
4. **Presentation/CLI/Formatters/**: أنشئ `<Cmd>ResultFormatter`.
5. **Bootstrap/ModulesBuilder/**: أنشئ `<Cmd>ModuleBuilder` يسجّل الـ Handler والـ Creator والـ Formatter.
6. سجّل الـ Parser والـ Module في `Presentation/CLI/main.py`.

> يجب أن ترث `Result` من `CommandResult` وأن يكون `status` من نوع `CommandStatus`، ليعمل التحقق من الأخطاء ورمز الخروج في `Application.run`.