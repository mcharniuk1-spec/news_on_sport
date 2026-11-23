# Відеовиробництво на MAXITO

Аудит 19 листопада 2026, Europe/Sofia. [Реєстр проєктів](projects.json) · [Моделі fal](fal-routing.md) · [Монтаж, аналіз і motion design](workflow.md) · [Кадри Outspoken](reference/outspoken-contact.jpg) · [Архів скілів](skill-archive/) · [Запис перевірок](runs/2026111901_run_video_audit.md).

**Розширення аудиту.** [Editing, CapCut, Palmier Pro та motion design](editors-and-motion.md) · [Повні параметри 30 fal endpoints](fal-parameters.md) · [Аудит скілів і скани](skills-audit.md).

## Стек, який має сенс використовувати

- **FFmpeg + HyperFrames** — основний локальний маршрут для нарізок із готового MP4, брендованих титрів і HTML/CSS/GSAP-роликів. FFmpeg формує проксі й точні вирізки, HyperFrames рендерить графіку або цілу HTML-композицію. Перевірено локальне HTML → MP4.
- **Remotion** — для React/TypeScript-шаблонів, структурованих вхідних даних, кількох мов і форматів, компонентів графіків та інтерактивного preview. Виявив npm cache 4.0.520 та плагін зі скілами 4.0.534. Для рендерингу слід вибрати конкретний checkout із lockfile та узгодити версії пакетів. [Remotion CLI](https://www.remotion.dev/docs/cli)
- **CapCut** — швидка ручна доводка соцмережевих роликів. CapCut.app 9.7.4794 є на MAXITO. Офіційний HTTP MCP `capcut_creation` додано глобально й перевірено читанням конфігурації. OAuth завершився успішно в зовнішньому Chrome через офіційний helper. Desktop CLI показав OAuth. Захищений виклик у поточному чаті ще не підтверджено. [CapCut × Codex](https://www.capcut.com/tools/capcut-x-codex)
- **Palmier Pro** — локальний NLE із діалоговим монтажем, треками, captions, ефектами, snapshots та XML/FCPXML. Перевірено 58 схем і read-only список проєктів через уже зареєстрований stdio MCP.
- **DaVinci Resolve + Fusion + Fairlight** — основний кандидат для складного монтажу, проксі, мультикаму, трекінгу, кольору та звуку. Bundle 21.1.2 і виконуваний файл фізично присутні на диску. Після повторного нативного запуску відкрився Project Manager. MCP відповів `SCRIPTING_UNAVAILABLE`: процес запущено, bridge не активний. Python-файл bridge є у Fusion/Scripts/Utility, але в меню Workspace → Scripts відображався лише canary. Для Studio перевірити налаштування External scripting using → Local; для Free потрібен доступний in-app bridge і повторний `project_manager.list`. Ручний запуск Resolve підтверджено.
- **fal** — каталог і білінг відповіли через OAuth-конектор. Баланс вичерпано, завантаження та генерація заблоковані. Окремий API-ключ для CLI/CI не підтверджено. OAuth-конектор працює для планування, окремий ключ потрібен лише для прямого SDK. [Білінг fal](https://fal.ai/connect/credits)

## Проєкти й матеріали

Охоплення реєстру — 22 локальні та 12 ChatGPT-проєктів. Для локальних проєктів цільовий пошук був обмежений MAXITO та медіарелевантним деревом ArchFlow. ChatGPT-проєкти інвентаризовано за назвами; їхні матеріали не переглядалися.

| Джерело | Як використати |
| --- | --- |
| ArchFlow → Content Engine → LinkedIn → Outspoken | Найсильніший знайдений приклад для повторного використання. У пакеті v5 є `brand-library/packages/video` зі сценами, версіями та frame adapter. У r11/r12/r14 є різні формати та окремі голосові версії. Взяти параметри сцен, сітку, UI-рухи та критерії QA з актуальної версії. |
| have | Простір для hospitality/brand роликів. Перед монтажем зіставити оригінали з проєктною бібліотекою та правами на матеріал; повторно використати власні кадри для location b-roll і кліпів. |
| CapCut і DaVinci на MAXITO | Каталоги застосунків і runtime. Пошук у видимих каталогах CapCut Live і Resolve Project Libraries не підтвердив редагованих користувацьких проєктів; знайдений Fuse.drp належить SDK-прикладам. |
| Qollabe та вкладені дослідницькі проєкти, Thesis | У реєстрі є окремі проєкти; для відео придатні погоджені експлейнери, data motion і демонстрації за синтетичними чи публічними матеріалами. |
| Real Estate Bulg, Hotel Optimization, Croatia, Христя, Storyverse та інші | Є в реєстрі. Застосовувати маршрути за типом матеріалу: tour/demo/story/experiments. Прив’язку до конкретних оригіналів ще не встановлено. |
| Coffee items | Цільовий пошук імен coffee/cafe/кава на диску й у ArchFlow не дав погодженого відео чи брифу, який можна ідентифікувати як цей матеріал. Для тесту описано сценарій coffee product b-roll у [workflow](workflow.md). |

## Скіли на диску

Перший аудит зберіг 43 `SKILL.md` з локальних Remotion/fal/HyperFrames-пакетів, наявних монтажних скілів і офіційного CapCut bundle. Групи: `Editing` — універсальна генерація/редагування, `Remotion` — React motion, Studio, рендер і captions, `HyperFrames` — HTML, CLI і media, `fal` — каталог, маршрутизація й production, `CapCut` — rough cut, локальні drafts, шаблони, медіа й auth. Архів лежить поза шляхом автоматичного завантаження. Підтримуваний safe installer відхилив окремий каталог MAXITO як ціль активації. CapCut bundle збережено для читання, його скрипти в архіві не запускалися. Підключення MCP зроблено штатною CLI-командою окремо. Після розширення в архіві 68 entry points. Підтримуваний інсталятор активував Transformers.js після статичного сканування. [Результати аудиту](skills-audit.md)
