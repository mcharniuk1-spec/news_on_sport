# Video Operations — інструкція для Claude

Корінь робочих матеріалів: `<PROJECT_ROOT>`. Якщо Claude відкрито з `<DRIVE>`, явно завантаж цей файл. Почни з [інвентарю](README.md), [реєстру проєктів](projects.json) і лише потрібного розділу [монтажу та motion design](editors-and-motion.md).

## 1. Підготуй локальний стек

- Перевір `ffmpeg -version`, `ffprobe -version`, `node -v` і наявність вихідних медіа. FFmpeg — для проксі, нарізок, звуку, компіляції та QC.
- **HyperFrames:** якщо CLI не в PATH, попередньо перевірений кеш — `~/.npm/_npx/0865b412d54fa5ea/node_modules/.bin/hyperframes`. Запусти `--version` і `doctor`. Для HTML motion використовуй seekable timeline. Локальний HTML → MP4 пройшов тест.
- **Remotion:** для React/TypeScript, даних, captions і серій. Працюй у checkout з lockfile, узгодь версії пакетів, запусти Studio й короткий рендер. Наявність npm cache не підтверджує готовий checkout.
- **Скіли:** `<PROJECT_ROOT>/skill-archive/{Editing,Analysis,Audio,HyperFrames,Remotion,CapCut,fal,Upstream}/`. Відкривай лише відповідний `SKILL.md` та потрібні references. Архів не є шляхом автозавантаження. Перш ніж активувати новий скіл у Claude, користуйся чинним safe installer і NVIDIA SkillSpector. [Інвентар і результати сканування](skills-audit.md).

## 2. Підключи лише потрібні MCP

У **Claude Code** спочатку виконай `claude mcp list` у цьому проєкті. У **Claude Desktop** перевір Settings → Extensions/Connectors. Реєстрація та OAuth Codex не переносяться автоматично. Після кожного підключення виконай read-only перевірку.

| Інструмент | Підключення та перевірка |
| --- | --- |
| **Palmier Pro** | Відкрий `/Applications/PalmierPro.app`. У Claude Desktop використовуй вбудований bundle `/Applications/PalmierPro.app/Contents/Resources/palmier-pro.mcpb`. У Claude Code, якщо запису ще немає, запусти `claude mcp add --scope local --transport http palmier-pro http://127.0.0.1:19789/mcp`. Далі `tools/list` і `manage_project(action="list")`. Локальний HTTP-каталог і чинний Codex stdio bridge перевірено окремо. [Документація](https://www.palmier.io/docs/agent-and-mcp.md) |
| **CapCut** | Desktop app у `<DRIVE>/CapCut/Applications/CapCut.app`. Для Claude з підтримкою remote MCP перевір сумісність офіційного endpoint `https://www.capcut.com/api/external_mcp` і OAuth resource з тим самим URL. Якщо клієнт підтримує цей потік, зареєструй `capcut_creation`, запусти OAuth у клієнті й передай підтвердження користувачу у зовнішньому Chrome. Перевір read-only profile або шаблони. OAuth успішний у Codex, сумісність із Claude окремо не перевірено. Якщо OAuth не проходить, використовуй CapCut Desktop і локальний MP4/SRT handoff. [Офіційне підключення CapCut × Codex](https://www.capcut.com/tools/capcut-x-codex) |
| **DaVinci Resolve** | Відкрий `<DRIVE>/DaVinci Resolve/Applications/DaVinci Resolve/DaVinci Resolve.app`. Чинний stdio server: `~/Library/Application Support/davinci-resolve-mcp/venv/bin/python` запускає `~/Library/Application Support/davinci-resolve-mcp/src/server.py`. Перед реєстрацією звір шляхи й тільки потрібні `PYTHONPATH`, `RESOLVE_SCRIPT_API`, `RESOLVE_SCRIPT_LIB` з локальним `codex mcp get davinci-resolve --json`. Перевір `project_manager.list`. Стан попереднього тесту — `SCRIPTING_UNAVAILABLE`. Для Studio перевір локальний external scripting, для Free — доступність і запуск in-app bridge. |
| **fal.ai** | Якщо в Claude є нативний конектор, перевір каталог і білінг. Інакше використовуй офіційний SDK із server-side `FAL_KEY` з наявного захищеного сховища, якщо ключ там підтверджено. Codex OAuth працював для каталогу, окремий ключ не знайдено, останній billing check показав вичерпаний баланс. Для планування бери [CSV каталогу](catalog/fal-endpoints.csv), [схеми 30 endpoints](fal-parameters.md) і [мапу моделей](fal-routing.md). |

FFmpeg, HyperFrames і Remotion можна запускати локально через CLI. NVIDIA VSS і Hugging Face використовуй лише для конкретного завдання після перевірки runtime. Новий сервіс заради інвентаризації не потрібен.

## 3. Виконай монтаж

1. Звір джерела, таймкоди й формат. Зроби ASR і покадрову вибірку, познач уривки.
2. Вибери **Palmier або CapCut** для редагованого монтажу, **Resolve** для складного finishing, **HyperFrames або Remotion** для motion та **fal** для погоджених генеративних шотів, дубляжу чи Foley.
3. Почни з короткого уривка й окремої версії таймлайна. Перевір результат зі звуком, субтитри, межі склейок та вертикальне кадрування перед масштабуванням. Збережи версію, MP4 і SRT/VTT за вимогами завдання.
