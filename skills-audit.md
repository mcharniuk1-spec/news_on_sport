# Аудит відеоскілів і перевірка нових джерел

## Охоплення

Зіставлено сімейства відео та суміжних скілів у двох локальних roots `~/.codex/skills` і `~/.agents/skills`, попередній архів MAXITO, скіли плагінів fal, Remotion, CapCut та локального HyperFrames. Обсяг визначали назви й зміст релевантних груп, тому число не включає довільні навички, які можна опосередковано використати у відеопроєкті. Архів тепер має **68 SKILL.md**, з них 43 з першого аудиту, 24 раніше наявних суміжних і один новий із Hugging Face. [Додатковий реєстр із походженням](catalog/additional-installed-skills.json)

| Група | Що знайдено |
| --- | --- |
| Editing і production | RunComfy video-edit, video-extend, video-outpainting, image-to-video, ai-video-generation. CapCut rough cut, draft builder, upload, web editing, templates. |
| Motion design | 12 Remotion skills: Studio/render/markup/multimedia/captions/maps/create/docs/interactivity/upgrade/SaaS/best practices. Installed HyperFrames 0.9.2: hyperframes, hyperframes-cli, media-use. У новішому upstream є додаткові HyperFrames skills для registry, reverse і style sampling. |
| Аналіз і ASR | transcribe, NVIDIA VSS video Q&A, summarize, dense captions, embeddings, query, archive, report та deployment; calibration, video reasoning annotation; image-edit. VSS infrastructure потребує власного підтримуваного runtime, скіл сам не піднімає його. |
| Генерація і звук | 15 fal skills від prompt/model routing до cinematography, character, storytelling, commercial і UGC. Окремі локальні ACE-Step, AI music, ElevenLabs music. |
| Новий | Hugging Face Transformers.js, активовано для Codex після повторної перевірки exact tree. Скіл допомагає інтегрувати ASR та інші inference pipelines у JS; не є NLE або готовим генератором відео. |

## Паралельні скани NVIDIA SkillSpector 2.9.6

Шість кандидатів завантажено з upstream GitHub і перевірено одночасно в статичному режимі `--no-llm`. У звітах 100% заявленого покриття файлів, успішна робота аналізатора; LLM і meta аналіз не виконувалися. Окремо переглянуто інструкції, зовнішні передачі й ризикові залежності. Слово SAFE у сканері — статичний результат, фінальне рішення про активацію залежить від джерела, залежностей і поведінки. [Сканер](https://github.com/NVIDIA/SkillSpector) · [Звіти](verification/skill-scans/)

| Точне джерело | Бал | Рішення |
| --- | ---: | --- |
| [huggingface/skills • transformers-js](https://github.com/huggingface/skills/tree/5291c2b9365e06b175dc04817610c778623f4836/skills/transformers-js) | 0 | Встановлено підтримуваним safe installer. Копію звірено з upstream; інсталятор додав provenance та scan report. |
| [kajisho5/ffmpeg-skill • skills/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill/tree/216124e596b4c7e8ae8943f3a0046594708995cc/skills/ffmpeg-skill) | 0 | Один відсканований файл посилається на утиліти з ширшого repo. Для цього аудиту залишено штатний FFmpeg, без активації неповного skill tree. |
| [gitethanwoo/video-editing • analyze-video-editing](https://github.com/gitethanwoo/video-editing/tree/8b633c2d698410e523f95335aa6433766264cc7f/skills/analyze-video-editing) | 29 | CAUTION. Містить виконувані Python-скрипти, зокрема режим зовнішнього надсилання аудіо. Залишено для огляду без активації. |
| [HeyGen • hyperframes-registry](https://github.com/heygen-com/hyperframes/tree/01a5e948beb984e0ea19f8939d4a5ae2b242f117/skills/hyperframes-registry) | 12 | Потребує сумісного CLI й посилається на usage telemetry/feedback. Залишено для огляду без активації. |
| [HeyGen • style-sampling](https://github.com/heygen-com/hyperframes/tree/01a5e948beb984e0ea19f8939d4a5ae2b242f117/skills/style-sampling) | 7 | Сумісність із локальним 0.9.2 не перевірена. Наявні Pro/telemetry дії. |
| [HeyGen • reverse-any-video](https://github.com/heygen-com/hyperframes/tree/01a5e948beb984e0ea19f8939d4a5ae2b242f117/skills/reverse-any-video) | 16 | Є Pro та cloud rendering залежності. Публічний workflow корисний як довідка з покадрового аналізу. |

Додаткові Resolve-кандидати зі сторонніх GitHub репозиторіїв лишилися на етапі discovery. Для діагностики чинного Resolve MCP спершу потрібне підключення до SDK/bridge, а скіл робить цей API зручнішим після підключення.

## Hugging Face для моделей

- [Whisper large-v3-turbo](https://huggingface.co/openai/whisper-large-v3-turbo) — кандидат для ASR. Окремо щільний word alignment та діаризація.
- [Qwen3-VL-8B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct) — модель для мультимодального опису й кадрів. Для швидких рухів і переходів потрібен контроль інтервалів та перегляд.
- [Wan2.2 I2V A14B](https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B) — альтернатива для image-to-video. Перевіряти пам’ять, quantization, fps і підтримку конкретного runtime.
- [LTX-2.3](https://huggingface.co/Lightricks/LTX-2.3) — альтернатива для audio-video й control workflows. На цьому Mac ваги не запускалися, GPU throughput і якість не вимірювалися.
