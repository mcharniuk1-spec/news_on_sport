# Editing, motion design та рев’ю

## 1. Монтаж — вибір інструмента за операцією

| Завдання | CapCut Desktop | Palmier Pro MCP | Коли взяти інший інструмент |
| --- | --- | --- | --- |
| Розібрати long-form і зробити selects | Імпорт на timeline, playback, маркери, split, trim, видалення. Автоматичну нарізку перевіряти за сенсом, першою/останньою репліками та паузами. | `inspect_media`, `search_media`, `get_transcript`, `detect_scenes`; `remove_words`, `remove_silence` або `ripple_delete_ranges` після відбору. Після ripple перечитати слова й таймлайн. | FFmpeg/ffprobe + локальний ASR для batch. Resolve для мультикаму й складного звуку. |
| Точні J/L cuts, діалоги, реакції | Відокремити аудіо, вести його окремим треком; накласти реакцію як overlay, зробити PIP, split screen або freeze. Вирівняти за хвилею й реплікою. | `sync_clips`, `manage_multicam`, `change_cam`, `apply_layout`, `manage_clip_links`, `set_clip_properties`. Координати джерела в секундах, на таймлайні в кадрах. | Resolve/Fairlight для монтажу багатодоріжкового звуку; FFmpeg для серійного PIP. |
| Вертикальні кліпи | Дублювати проєкт/версію, виставити 9:16, reframe, перевірити обличчя й safe zones після кожної зміни плану. Для двох людей — квадратний inset або stacked split. | Окремий timeline від master, canvas settings, `apply_layout` та keyframes. Зміна canvas може перекадрувати кліпи. | Remotion/HyperFrames для різних layout за одним manifest. H3 Max reframe — якщо потрібен синтетичний результат за межами простого crop і його можна перевірити. |
| Субтитри | Auto Captions → виправити слова, імена та розриви рядків → загальний стиль → ручні акценти. Доступність функцій залежить від версії, платформ і регіону. | `get_transcript` → `add_captions` → caption group style; окремий authored text через `add_texts`. | Локальний ASR/Scribe плюс SRT/VTT/ASS як джерело часу, Remotion для word-highlight і RTL/багатомовного layout. |
| B-roll / stock / вставки | На верхній доріжці або replace clip, із source-audio mute за потреби. Зберегти початковий діалог і вирівняти зміст репліки з появою кадру. | `get_assets`, `search_media`, `import_media`, `insert_clips`, `swap_clip_media`; asset library для погоджених повторюваних вставок. `list_models` перед генерацією, dry run для оцінки credits. | fal для короткого синтетичного шота, Blender для точного 3D packshot, реальна зйомка для документальних деталей. |
| Crop, маска, видалення фону | Mask, feather, keyframes, auto cutout за наявності. Контроль країв, волосся, рук і перекриттів. | `manage_masks` для базових форм чи prompt-based tracking, `set_keyframes` для підтриманих параметрів. Prompt-based tracking може потребувати credits. | Fusion для track, clean plate, rotoscope. Bria/Pixelcut для окремого шота. |
| Заміна тексту / графіка в кадрі | Якщо текст є окремим шаром, змінити сам шар. У сплющеному відео накрити чистою ділянкою або маскою, прив’язати новий текст до руху й перспективи кадру. | `update_text` для authored text; `add_texts`, маски, keyframes, імпорт зовнішнього композиту. | Fusion/After Effects для perspective tracking. HTML/Remotion для точного тексту й повторних версій. |
| Speed, transitions, ритм | Speed curves, freeze, clip transitions, beat markers. Залишати handles і перевіряти рух після інтерполяції. | `edit_speed` для uniform/curve, `detect_beats`, `split_clips`; ефекти та layout motion за живими схемами. | FFmpeg для простих переходів і точних повторів; Topaz для тесту інтерполяції. |
| Color, audio, export | HSL, curves/filters, гучність, fade, музика та voice-over. Перевірити весь експорт, настроїти resolution/frame rate/codec на цільову платформу. | `apply_color`, `inspect_color`, `denoise_audio`, `export_project`, `manage_exports`. Задокументовані video/XML/FCPXML/package routes. | Resolve Color/Fairlight для складного finishing, FFmpeg для QC/перекодування та профілів доставки. |
| Передача й рев’ю | Для власного монтажера передати editable draft, вихідні файли та окремий MP4. Для зовнішнього review достатньо MP4 з таймкодом. | `manage_markers`, `manage_snapshots`, `inspect_timeline`; snapshot для версій, XML/FCPXML після перевірки round-trip. | MP4 + SRT/VTT + edit manifest — стабільний мінімум між різними середовищами. Контрольовані обміни XML/AAF/EDL тестувати на одному уривку. |

Джерела. [CapCut Desktop](https://www.capcut.com/resource/how-to-use-capcut) · [CapCut на ПК](https://www.capcut.com/resource/how-to-use-capcut-on-pc) · [CapCut captions](https://www.capcut.com/help/how-to-recognise-subtitles) · [Palmier Pro](https://www.palmier.io/) · [Palmier Pro GitHub](https://github.com/palmier-io/palmier-pro).

### CapCut Desktop, Codex і локальні drafts

Desktop — ручний монтаж. CapCut × Codex за документацією організовує надані матеріали та створює редагований rough cut, який можна довести в CapCut. Конкретні команди підключення й покриття Desktop-функцій треба перевіряти в актуальному каталозі MCP. OAuth у зовнішньому Chrome завершився `success=true`, а desktop CLI показав `OAuth`. У вже відкритому чаті CapCut tools не з’явилися, а окремий runtime helper дав `connection_not_confirmed`. Перша перевірка в сесії із завантаженими інструментами — read-only profile або шаблони. Платні та завантажувальні операції для цієї перевірки зайві. [CapCut × Codex](https://www.capcut.com/tools/capcut-x-codex)

### Palmier Pro як локальний NLE для агента

На Mac є Palmier Pro 0.12.1 build 91 і вбудований MCP bundle 0.2.0. Застосунок запускається, а локальний HTTP MCP повернув 58 схем. У Codex уже був зареєстрований stdio bridge. Окремо через його штатну команду пройшли initialize, tools/list і read-only manage_project.list. Apple Silicon і macOS 26+ — вимоги виробника. [Доступні схеми](catalog/palmier-tools.json) · [Релізи](https://github.com/palmier-io/palmier-pro/releases)

Практичний сценарій. Створити окремий alternate timeline із погодженого master, інвентаризувати медіа, прочитати діалог на рівні слів. Для змістовних скорочень позначити репліки й таймкоди, для монтажу реакцій окремо синхронізувати аудіо/відео. Зробити snapshot перед серією правок, потім читати результати через timeline, transcript, composited frames і color scopes. Перевірити версію офлайн зі звуком. CapCut корисний, коли монтажер доводить social effects і шаблони вручну. Palmier має явні інструменти для таймкодів, діалогу, медіа й версій. Resolve доречний для складного tracking, finishing і зведення звуку.

## 2. Motion design — проєктування окремо від нарізки

- **HTML/CSS/SVG + HyperFrames.** Готові сайти, UI-демо, типографіка, брендовані transitions, charts і HTML subtitles. Для покадрового рендеру задавати seekable GSAP/WAAPI timeline і локальні шрифти. Важкі blur, тіні, багато відеошарів та 3D підвищують витрати пам’яті.
- **Remotion React/TypeScript.** Для серій, словників перекладів, даних та автоматичних 16:9/9:16/4:5 версій. Контролювати fps, props, shared assets і час рендеру. Різні формати мають власні композиційні правила.
- **CapCut/Palmier keyframes.** Вручну або через підтверджені інструменти задавати появу, масштаб, позицію, opacity, crop та PIP. Доречно для окремого ролика. Для десятків повторів краще параметризована композиція.
- **Fusion або After Effects.** Tracking, rotoscope, clean plate, depth layers, професійна анімація й композитинг. Потрібні окремі шаблони й переносимі рендери. Складні ефекти треба перевіряти після NLE handoff.
- **Blender / Three.js.** 3D камера, матеріали, світло, предметна зйомка, частинки. Blender дає контроль над 3D-пайплайном і проходами рендеру, Three.js дозволяє перевикористовувати вебсцену. Фіксувати asset versions, камеру й seed.
- **Motion Canvas / Manim / Rive / Lottie.** Motion Canvas і Manim для пояснень і діаграм. Rive/Lottie для компактних багаторазових векторних елементів. Під час відеоекспорту стан і час стають визначеними кадрами, а інтерактивність не переноситься.
- **FFmpeg, ASS, PNG/ProRes alpha.** Для швидких lower thirds, зміни layout, burn-in та фінального зведення відрендерених шарів. У складній сцені підтримувати графіку зручніше у вихідному редакторі, а FFmpeg лишити для компіляції.

[Детальна матриця технологій, HTML-пайплайн і перевірки](workflow.md)

## 3. Підготовка промптів з готових відео

Визначити режим аналізу за запитом: `summary` для короткої суті, `shot_log` для кадрів і монтажних меж, `selects` для нарізки, `style_map` для повторення руху й верстки, `audio_event_log` для Foley. Спочатку FFmpeg metadata і scene candidates, ASR зі словами та мовцями, потім візуальні кадри і точна перевірка навколо обраних місць. Для кожного запису зберігати `asset_id, source_in_ms, source_out_ms, evidence_frames, visible_action, transcript_quote, confidence`. Після model pass переглянути важливі місця зі звуком і кадри по обидва боки склейок.

Генеративний запит для B-roll задає **завдання, тривалість, предмет і дію, плани, рух камери, світло, стабільні деталі й потрібний звук**. Для video-to-video описати тільки потрібну зміну, потім окремо перелічити речі, які мають збігтися з оригіналом. Для Foley задати фізичне джерело, акустику, акценти, місця тиші та пріоритет голосу. Coffee приклад: звук струменя під час наливання, два тихі удари кераміки, суха акустика, без музики. Картинку тестувати окремо на логотипі, формі чашки й фізиці струменя.

Найменший корисний пілот — один погоджений вихідний кліп, три нарізки з однаковим source timecode, один титр, окреме Foley, два aspect ratios. Порівняти час ручної правки, повторний рендер, якість синхронізації, мобільну читабельність і портативність timeline.
