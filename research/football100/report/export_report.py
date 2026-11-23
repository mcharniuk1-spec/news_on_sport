#!/usr/bin/env python3
"""Build the analytics workbook (xlsx + csv + json) from features.json + final/NN.json (+ CORRECTIONS.json).
Run: python3 report/export_report.py     Output: FINAL_100/football100_report.xlsx, .csv, report/final_all.json"""
import csv, glob, json, os, subprocess, sys
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XImage
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); H = os.path.dirname(D)
sys.path.insert(0, D)
import taxonomy as T

# ---------- data ----------
feats = {f["no"]: f for f in json.load(open(f"{D}/features.json"))}
labels = {}
for p in sorted(glob.glob(f"{D}/final/[0-9][0-9].json")):
    for r in json.load(open(p)): labels[r["no"]] = r
corr_p = f"{D}/final/CORRECTIONS.json"; n_corr = 0
if os.path.exists(corr_p):
    for no, fix in json.load(open(corr_p)).items():
        if int(no) in labels: labels[int(no)].update(fix); n_corr += 1
errs = []
for r in labels.values(): T.validate_record(r, errs, "final ")
assert not errs, errs[:10]
missing = [n for n in feats if n not in labels]
assert not missing, f"unlabelled: {missing}"
json.dump([labels[n] for n in sorted(labels)], open(f"{D}/final_all.json", "w"), ensure_ascii=False, indent=1)
agree = {}
for p in glob.glob(f"{D}/final/agreement_*.json"):
    for k, v in json.load(open(p)).items(): agree.setdefault(k, []).append(v)

def final_video(no):
    f = feats[no]; name = f["video_file"]
    return (f"FINAL_100/pilot_extra/{name}" if no > 900 else f"FINAL_100/videos/{name.replace('_small', '')}")

def first_frame_ok(no):
    f = feats[no]; v = f"{H}/{final_video(no)}"
    if not os.path.exists(v): return "no file"
    try:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", v, "-frames:v", "1", "/tmp/_ff0.png"], check=True)
        a = Image.open("/tmp/_ff0.png").convert("RGB").resize((108, 192)); b = Image.open(f["cover_src"]).convert("RGB").resize((108, 192))
        import numpy as np
        d = float(np.abs(np.asarray(a, dtype=int) - np.asarray(b, dtype=int)).mean())
        return "yes, frames 1-3" if d < 12 else f"NO (diff {d:.0f})"
    except Exception as e: return f"check failed: {e}"

def bucket(d):
    return "n/a" if not d else ("<=35 s" if d <= 35 else "36-45 s" if d <= 45 else "46-60 s" if d <= 60 else ">60 s")

# thumbnails
os.makedirs(f"{D}/thumbs", exist_ok=True)
for no, f in feats.items():
    im = Image.open(f["cover_src"]).convert("RGB")
    im.resize((81, 144), Image.LANCZOS).save(f"{D}/thumbs/{no:03d}_s.jpg", quality=82)
    im.resize((135, 240), Image.LANCZOS).save(f"{D}/thumbs/{no:03d}_m.jpg", quality=84)

rows = []
for no in sorted(feats):
    r = dict(feats[no]); r.update({k: v for k, v in labels[no].items() if k != "no"})
    r["final_file"] = final_video(no); r["first_frame_cover"] = first_frame_ok(no); r["duration_bucket"] = bucket(r.get("duration_s"))
    r["risk_flags_txt"] = ", ".join(r["risk_flags"])
    r["p1_changes"] = "; ".join(f"{c['category']}: {c['action']}" for c in r["changes"] if c["priority"] == "P1")
    r["n_p1"] = sum(c["priority"] == "P1" for c in r["changes"])
    r["all_changes"] = "\n".join(f"[{c['priority']}] {c['category']}: {c['action']}" for c in r["changes"])
    r["source_label"] = (r.get("news_domain") or "Ballon d'Or pack") if r["source_kind"] != "split" else "split of a pilot video"
    r["comic_txt"] = "yes" if r["comic"] else "no"; r["hook_num_txt"] = "yes" if r["hook_has_number"] else "no"; r["hook_q_txt"] = "yes" if r["hook_has_question"] else "no"
    rows.append(r)
json.dump(rows, open(f"{D}/report_rows.json", "w"), ensure_ascii=False, indent=1, default=str)

# ---------- column registry ----------
# (key, English header, Ukrainian header, width, group)
COLS = [
 ("no", "No", "№", 6, "ID"), ("group", "Set", "Набір", 11, "ID"), ("title", "On-screen title", "Заголовок", 30, "ID"), ("subject", "Subject (news / player)", "Тема / герой", 34, "ID"),
 ("source_kind", "Source type", "Тип джерела", 10, "ID"), ("source_label", "Source", "Джерело", 16, "ID"), ("news_date", "News date", "Дата новини", 11, "ID"), ("news_n_sources", "Sources (n)", "Джерел", 8, "ID"),
 ("voice_engine", "Voice engine", "Рушій голосу", 11, "Voice"), ("voice_name", "Voice", "Голос", 16, "Voice"), ("voice_label", "Voice slot", "Слот", 8, "Voice"), ("voice_model", "Model", "Модель", 22, "Voice"),
 ("hook_text", "Hook (first line)", "Хук (перший рядок)", 44, "Hook"), ("hook_type", "Hook type", "Тип хука", 16, "Hook"), ("hook_type_alt", "2nd hook device", "Другий прийом", 14, "Hook"),
 ("hook_basis", "Hook built on", "Хук побудований на", 20, "Hook"), ("hook_basis_detail", "Basis detail (the concrete fact)", "Конкретика (факт)", 40, "Hook"),
 ("hook_words", "Hook words", "Слів у хуку", 7, "Hook"), ("hook_num_txt", "Number in hook", "Число в хуку", 8, "Hook"), ("hook_q_txt", "Question in hook", "Питання в хуку", 8, "Hook"), ("hook_strength", "Hook strength (1-5, predicted)", "Сила хука (1-5, прогноз)", 10, "Hook"),
 ("story_summary", "Story in one line", "Історія одним рядком", 44, "Story"), ("topic_primary", "Topic", "Тематика", 20, "Story"), ("scope", "Scope", "Змагання / охоплення", 16, "Story"),
 ("subject_type", "Subject type", "Тип героя", 12, "Story"), ("timeliness", "Timeliness", "Актуальність", 14, "Story"), ("uk_relevance", "UK relevance", "Близькість до UK", 10, "Story"),
 ("story_structure", "Story structure", "Структура історії", 18, "Story"), ("twist_position", "Twist position", "Де поворот", 10, "Story"), ("payoff_type", "Payoff type", "Тип розв'язки", 15, "Story"),
 ("humour_type", "Humour type", "Тип гумору", 16, "Humour & emotion"), ("humour_target", "Humour target", "Ціль жарту", 12, "Humour & emotion"), ("humour_intensity", "Humour intensity (0-3)", "Інтенсивність гумору (0-3)", 9, "Humour & emotion"), ("dominant_emotion", "Dominant emotion", "Емоція", 13, "Humour & emotion"),
 ("comment_bait", "Comment trigger", "Тригер коментарів", 15, "Engagement design"), ("cta_opener_type", "CTA opener type", "Тип початку CTA", 14, "Engagement design"), ("cta_opener", "CTA opener text", "Початок CTA", 34, "Engagement design"), ("cta_opener_repeat", "CTA opener used in N videos", "Скільки відео з таким CTA", 9, "Engagement design"),
 ("story_clarity", "Story clarity (1-5)", "Ясність історії", 8, "Predicted scores"), ("humour_quality", "Humour quality (1-5)", "Якість гумору", 8, "Predicted scores"), ("shareability", "Shareability (1-5)", "Поширюваність", 8, "Predicted scores"),
 ("comment_potential", "Comment potential (1-5)", "Потенціал коментарів", 9, "Predicted scores"), ("uk_fit", "UK fit (1-5)", "Підходить UK", 8, "Predicted scores"), ("novelty", "Novelty (1-5)", "Новизна", 8, "Predicted scores"),
 ("virality_pred", "Virality (1-10, predicted)", "Вірусність (1-10, прогноз)", 10, "Predicted scores"), ("annotator_agreement", "Annotator agreement", "Узгодженість анотаторів", 10, "Predicted scores"),
 ("duration_s", "Duration (s)", "Тривалість (с)", 9, "Production"), ("duration_bucket", "Duration bucket", "Діапазон тривалості", 10, "Production"), ("words", "Words", "Слів", 7, "Production"), ("chars", "Chars", "Символів", 8, "Production"),
 ("limit_chars", "Char limit", "Ліміт символів", 8, "Production"), ("words_per_second", "Words / s", "Слів/с", 8, "Production"), ("loudness_lufs", "Loudness (LUFS)", "Гучність (LUFS)", 9, "Production"),
 ("comic_txt", "Comic inserts", "Комікс-вставки", 8, "Production"), ("comic_style", "Comic style", "Стиль коміксу", 14, "Production"), ("n_inserts", "Inserts planned", "Вставок заплановано", 8, "Production"), ("flip_clips_ready", "Flip clips ready", "Вставок готово", 8, "Production"),
 ("footage_clips", "Footage clips", "Футаж-кліпів", 8, "Production"), ("final_file", "Final file", "Фінальний файл", 38, "Production"),
 ("thumb", "Poster preview", "Прев'ю постера", 12, "Poster"), ("first_frame_cover", "Cover as first frame", "Обкладинка першим кадром", 14, "Poster"), ("cover_title", "Poster headline", "Заголовок постера", 34, "Poster"),
 ("cover_joke", "Poster bubble joke", "Жарт у бульбашці", 34, "Poster"), ("cover_burst", "Burst word", "Слово-вибух", 13, "Poster"), ("cover_emoji", "Emoji set", "Емодзі", 10, "Poster"), ("cover_sunburst", "Sunburst colour", "Колір променів", 9, "Poster"),
 ("cover_tilt_deg", "Panel tilt (deg)", "Нахил панелі", 8, "Poster"), ("cover_hero_source", "Hero source", "Джерело героя", 20, "Poster"), ("poster_title_sells_hook", "Poster sells the reactions (1-5)", "Постер продає реакції (1-5)", 11, "Poster"),
 ("poster_joke_quality", "Poster joke quality (1-5)", "Якість жарту на постері (1-5)", 10, "Poster"), ("poster_issue", "Poster issue", "Проблема постера", 32, "Poster"), ("poster_change", "Poster change", "Що змінити в постері", 32, "Poster"),
 ("risk_flags_txt", "Risk flags", "Ризики", 26, "Risks & changes"), ("n_p1", "P1 changes (n)", "P1 змін", 7, "Risks & changes"), ("p1_changes", "P1 changes", "P1 зміни", 44, "Risks & changes"), ("all_changes", "All recommended changes", "Усі рекомендовані зміни", 60, "Risks & changes"),
]
PERF = [("platform", "Platform", "Платформа", 14), ("publish_date", "Publish date", "Дата публікації", 12), ("url", "URL", "Посилання", 22), ("views", "Views", "Перегляди", 10), ("likes", "Likes", "Лайки", 8),
        ("comments", "Comments", "Коментарі", 9), ("shares", "Shares", "Поширення", 9), ("saves", "Saves", "Збереження", 9), ("avg_view_s", "Avg view duration (s)", "Сер. час перегляду (с)", 11),
        ("avg_pct", "Avg % viewed", "Сер. % перегляду", 10), ("swipe_away", "Swiped away %", "Свайп-аут %", 9), ("subs", "Subs gained", "Нових підписників", 9), ("clicks", "Site clicks", "Кліки на сайт", 9), ("pnotes", "Notes", "Нотатки", 24)]
CALC = [("like_rate", "Like rate", "Частка лайків"), ("comment_rate", "Comment rate", "Частка коментарів"), ("share_rate", "Share rate", "Частка поширень"), ("eng_rate", "Engagement rate", "Залученість"), ("click_rate", "Click rate", "CTR на сайт"), ("rank_views", "Rank by views", "Місце за переглядами")]
GROUPCOL = {"ID": "44546A", "Voice": "7B4FA3", "Hook": "D9731A", "Story": "3A8F5C", "Humour & emotion": "C0508B", "Engagement design": "1E8C93", "Predicted scores": "B8962E",
            "Production": "6E6E6E", "Poster": "C23B3B", "Risks & changes": "A34A1B", "Performance (fill in)": "2F6EBA", "Calculated": "1F4E8C"}
HR, R0 = 4, 5  # header row, first data row
N = len(rows); RN = R0 + N - 1
allkeys = [c[0] for c in COLS] + [p[0] for p in PERF] + [c[0] for c in CALC]
col = {k: i + 1 for i, k in enumerate(allkeys)}
def rng(k): return f"Videos!${L(col[k])}${R0}:${L(col[k])}${RN}"

wb = Workbook(); ws = wb.active; ws.title = "Videos"
thin = Side(style="thin", color="D0D0D0"); border = Border(left=thin, right=thin, top=thin, bottom=thin)
ws["A1"] = "Football Shorts: 100 videos + 4 pilot splits. Report for performance analytics"; ws["A1"].font = Font(size=15, bold=True)
ws["A2"] = ("Predicted columns (scores, virality, strengths) are annotator HYPOTHESES from the script text; compare them with the measured performance columns (blue, fill in) "
            "and the Analytics sheet recalculates. Labels come from two independent blind annotators plus an adjudicator and a cross-corpus QA pass.")
ws["A2"].alignment = Alignment(wrap_text=True, vertical="top"); ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=14); ws.row_dimensions[2].height = 32
# group band + headers
def put_headers(sheet, items, startcol, group, color):
    for i, (k, en, uk, w) in enumerate(items):
        c = startcol + i; cell = sheet.cell(HR, c, f"{en}\n{uk}")
        cell.font = Font(bold=True, color="FFFFFF", size=9); cell.fill = PatternFill("solid", fgColor=color); cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); cell.border = border
        sheet.column_dimensions[L(c)].width = w
    sheet.cell(3, startcol, group).font = Font(bold=True, color="FFFFFF");
    for c in range(startcol, startcol + len(items)): sheet.cell(3, c).fill = PatternFill("solid", fgColor=color)
    sheet.merge_cells(start_row=3, start_column=startcol, end_row=3, end_column=startcol + len(items) - 1)
    sheet.cell(3, startcol).alignment = Alignment(horizontal="center")
i = 0
while i < len(COLS):
    g = COLS[i][4]; j = i
    while j < len(COLS) and COLS[j][4] == g: j += 1
    put_headers(ws, [(k, en, uk, w) for k, en, uk, w, _ in COLS[i:j]], i + 1, g, GROUPCOL[g]); i = j
put_headers(ws, PERF, len(COLS) + 1, "Performance (fill in)", GROUPCOL["Performance (fill in)"])
put_headers(ws, [(k, en, uk, 11) for k, en, uk in CALC], len(COLS) + len(PERF) + 1, "Calculated", GROUPCOL["Calculated"])
ws.row_dimensions[HR].height = 52
wrapkeys = {"title", "subject", "hook_text", "hook_basis_detail", "story_summary", "cta_opener", "cover_title", "cover_joke", "poster_issue", "poster_change", "p1_changes", "all_changes", "risk_flags_txt", "final_file", "voice_model"}
INPUT_FILL = PatternFill("solid", fgColor="EAF2FF"); CALC_FILL = PatternFill("solid", fgColor="F2F2F2")
for ri, r in enumerate(rows):
    rr = R0 + ri; ws.row_dimensions[rr].height = 112
    for k, *_ in COLS:
        c = col[k]
        if k == "thumb":
            img = XImage(f"{D}/thumbs/{r['no']:03d}_s.jpg"); img.width, img.height = 81, 144; ws.add_image(img, f"{L(c)}{rr}"); continue
        v = r.get(k); cell = ws.cell(rr, c, v if not isinstance(v, (list, dict)) else json.dumps(v)); cell.border = border
        cell.alignment = Alignment(wrap_text=k in wrapkeys, vertical="top")
        if isinstance(v, float): cell.number_format = "0.0" if k not in ("annotator_agreement",) else "0%"
    for k, *_ in PERF:
        cell = ws.cell(rr, col[k]); cell.fill = INPUT_FILL; cell.border = border; cell.alignment = Alignment(vertical="top")
        if k == "publish_date": cell.number_format = "yyyy-mm-dd"
        if k in ("avg_pct", "swipe_away"): cell.number_format = "0.0%"
    V, Lk, Cm, Sh, Sv, Av = (f"{L(col[x])}{rr}" for x in ("views", "likes", "comments", "shares", "saves", "avg_view_s"))
    Ck = f"{L(col['clicks'])}{rr}"
    f = {"like_rate": f'=IFERROR({Lk}/{V},"")', "comment_rate": f'=IFERROR({Cm}/{V},"")', "share_rate": f'=IFERROR({Sh}/{V},"")',
         "eng_rate": f'=IFERROR(({Lk}+{Cm}+{Sh}+{Sv})/{V},"")', "click_rate": f'=IFERROR({Ck}/{V},"")',
         "rank_views": f'=IF(ISNUMBER({V}),RANK({V},${L(col["views"])}${R0}:${L(col["views"])}${RN}),"")'}
    for k, *_ in CALC:
        cell = ws.cell(rr, col[k], f[k]); cell.fill = CALC_FILL; cell.border = border; cell.alignment = Alignment(vertical="top")
        cell.number_format = "0.0%" if k != "rank_views" else "0"
ws.freeze_panes = ws.cell(R0, 3); ws.auto_filter.ref = f"A{HR}:{L(len(allkeys))}{RN}"
dv = DataValidation(type="list", formula1='"YouTube Shorts,TikTok,Instagram Reels,Facebook Reels,X"', allow_blank=True); ws.add_data_validation(dv); dv.add(f"{L(col['platform'])}{R0}:{L(col['platform'])}{RN}")
for k in ("hook_strength", "virality_pred", "shareability", "humour_quality", "comment_potential", "poster_title_sells_hook"):
    ws.conditional_formatting.add(f"{L(col[k])}{R0}:{L(col[k])}{RN}", ColorScaleRule(start_type="min", start_color="F8CBAD", mid_type="percentile", mid_value=50, mid_color="FFF2CC", end_type="max", end_color="A9D18E"))
ws.conditional_formatting.add(f"{L(col['n_p1'])}{R0}:{L(col['n_p1'])}{RN}", CellIsRule(operator="greaterThan", formula=["0"], fill=PatternFill("solid", bgColor="F4B084")))
ws.conditional_formatting.add(f"{L(col['first_frame_cover'])}{R0}:{L(col['first_frame_cover'])}{RN}", FormulaRule(formula=[f'LEFT({L(col["first_frame_cover"])}{R0},3)<>"yes"'], fill=PatternFill("solid", bgColor="F4B084")))

# ---------- Analytics ----------
an = wb.create_sheet("Analytics"); an.column_dimensions["A"].width = 30
an["A1"] = "Analytics: every table recalculates from the Videos sheet. Measured columns stay empty until you enter performance."; an["A1"].font = Font(size=13, bold=True)
an["A2"] = "N = videos with that label. Predicted = annotator estimate. Measured averages ignore videos with no data. Compare the two to see which labels really win."
HDR = ["Value", "N videos", "Avg predicted virality", "Avg hook strength", "Avg shareability", "Avg humour quality", "N with data", "Avg views", "Avg like rate", "Avg comment rate", "Avg share rate", "Avg engagement rate", "Avg % viewed", "Avg view time (s)"]
for i in range(2, len(HDR) + 1): an.column_dimensions[L(i)].width = 14
DIMS = [("hook_type", "Hook type"), ("hook_basis", "Hook built on"), ("topic_primary", "Topic"), ("story_structure", "Story structure"), ("humour_type", "Humour type"), ("humour_target", "Humour target"),
        ("dominant_emotion", "Dominant emotion"), ("comment_bait", "Comment trigger"), ("cta_opener_type", "CTA opener type"), ("payoff_type", "Payoff type"), ("twist_position", "Twist position"),
        ("scope", "Scope"), ("uk_relevance", "UK relevance"), ("timeliness", "Timeliness"), ("subject_type", "Subject type")]
row = 4
def table(title, key, values):
    global row
    an.cell(row, 1, title).font = Font(bold=True, size=12, color="FFFFFF");
    for c in range(1, len(HDR) + 1): an.cell(row, c).fill = PatternFill("solid", fgColor="1F4E8C")
    row += 1
    for i, h in enumerate(HDR, 1):
        c = an.cell(row, i, h); c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="DDEBF7"); c.alignment = Alignment(wrap_text=True, horizontal="center"); c.border = border
    row += 1
    for v in values:
        a = f"$A{row}"; kr = rng(key)
        vcrit = a
        an.cell(row, 1, v)
        def avg(k): return f'=IFERROR(AVERAGEIFS({rng(k)},{kr},{vcrit}),"")'
        vals = [f'=COUNTIF({kr},{vcrit})', avg("virality_pred"), avg("hook_strength"), avg("shareability"), avg("humour_quality"),
                f'=COUNTIFS({kr},{vcrit},{rng("views")},">0")', avg("views"), avg("like_rate"), avg("comment_rate"), avg("share_rate"), avg("eng_rate"), avg("avg_pct"), avg("avg_view_s")]
        for i, f in enumerate(vals, 2):
            c = an.cell(row, i, f); c.border = border
            c.number_format = "0" if i in (2, 7) else ("0.0" if i in (3, 4, 5, 6, 14) else ("#,##0" if i == 8 else "0.0%"))
        an.cell(row, 1).border = border; row += 1
    row += 1
for key, title in DIMS:
    table(title, key, list(T.ENUMS[key if key in T.ENUMS else key]))
table("Voice engine", "voice_engine", ["Kokoro", "ElevenLabs"]); table("Voice (name)", "voice_name", sorted({r["voice_name"] for r in rows}))
table("Comic inserts", "comic_txt", ["yes", "no"]); table("Number in hook", "hook_num_txt", ["yes", "no"]); table("Question in hook", "hook_q_txt", ["yes", "no"])
table("Duration bucket", "duration_bucket", ["<=35 s", "36-45 s", "46-60 s", ">60 s"]); table("Poster hero source", "cover_hero_source", sorted({r["cover_hero_source"] for r in rows}))
table("CTA opener repeated in N videos", "cta_opener_repeat", sorted({r["cta_opener_repeat"] for r in rows}))
# matrix hook_type x topic
an.cell(row, 1, "Matrix: hook type (rows) x topic (columns), N videos").font = Font(bold=True, size=12); row += 1
tops = list(T.ENUMS["topic_primary"]);
for i, t in enumerate(tops, 2): c = an.cell(row, i, t); c.font = Font(bold=True, size=9); c.alignment = Alignment(wrap_text=True, horizontal="center")
row += 1
for h in T.ENUMS["hook_type"]:
    an.cell(row, 1, h)
    for i, t in enumerate(tops, 2): an.cell(row, i, f"=COUNTIFS({rng('hook_type')},$A{row},{rng('topic_primary')},{L(i)}${row - 1 - list(T.ENUMS['hook_type']).index(h)})").border = border
    row += 1
row += 1
an.cell(row, 1, "Prediction calibration (needs measured data): correlation of predicted vs measured").font = Font(bold=True, size=12); row += 1
for lab, a_, b_ in [("virality_pred vs views", "virality_pred", "views"), ("hook_strength vs avg % viewed", "hook_strength", "avg_pct"), ("shareability vs share rate", "shareability", "share_rate"),
                    ("comment_potential vs comment rate", "comment_potential", "comment_rate"), ("humour_quality vs like rate", "humour_quality", "like_rate"), ("poster_title_sells_hook vs views", "poster_title_sells_hook", "views")]:
    an.cell(row, 1, lab); c = an.cell(row, 2, f'=IFERROR(CORREL({rng(a_)},{rng(b_)}),"needs data")'); c.number_format = "0.00"; c.border = border; row += 1
an.freeze_panes = "B4"

# ---------- Posters ----------
ps = wb.create_sheet("Posters")
pcols = [("no", "No / №", 6), ("thumb", "Poster preview / Прев'ю", 20), ("title", "Video title / Назва", 28), ("hook_type", "Hook type / Тип хука", 15), ("cover_title", "Poster headline / Заголовок", 34), ("cover_joke", "Bubble joke / Жарт", 32),
         ("cover_burst", "Burst word", 12), ("cover_emoji", "Emoji", 9), ("cover_sunburst", "Sunburst", 9), ("cover_hero_source", "Hero source", 20), ("first_frame_cover", "First frame = cover", 14),
         ("poster_title_sells_hook", "Sells the reactions (1-5)", 11), ("poster_joke_quality", "Joke quality (1-5)", 10), ("poster_issue", "Issue / Проблема", 34), ("poster_change", "Change / Що змінити", 34), ("views", "Views (copy from Videos)", 12)]
ps["A1"] = "Poster review: which headline/joke/colour/emoji combinations sell the video (compare with views)"; ps["A1"].font = Font(size=13, bold=True)
for i, (k, h, w) in enumerate(pcols, 1):
    c = ps.cell(3, i, h); c.font = Font(bold=True, color="FFFFFF", size=9); c.fill = PatternFill("solid", fgColor="C23B3B"); c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center"); ps.column_dimensions[L(i)].width = w
ps.row_dimensions[3].height = 40
for ri, r in enumerate(rows):
    rr = 4 + ri; ps.row_dimensions[rr].height = 184
    for i, (k, h, w) in enumerate(pcols, 1):
        if k == "thumb":
            img = XImage(f"{D}/thumbs/{r['no']:03d}_m.jpg"); img.width, img.height = 135, 240; ps.add_image(img, f"{L(i)}{rr}"); continue
        if k == "views": ps.cell(rr, i, f"=Videos!{L(col['views'])}{R0 + ri}").alignment = Alignment(vertical="top"); continue
        c = ps.cell(rr, i, r.get(k)); c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = border
ps.freeze_panes = "C4"; ps.auto_filter.ref = f"A3:{L(len(pcols))}{3 + N}"

# ---------- Changes ----------
cs = wb.create_sheet("Changes backlog")
cs["A1"] = "Recommended changes: one row per change (filter by priority / category; set Status as you go)"; cs["A1"].font = Font(size=13, bold=True)
ch_cols = [("No", 6), ("Video", 34), ("Priority", 8), ("Category", 20), ("Action", 70), ("Status", 12), ("Owner / note", 24)]
for i, (h, w) in enumerate(ch_cols, 1):
    c = cs.cell(3, i, h); c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="A34A1B"); cs.column_dimensions[L(i)].width = w
rr = 4
for r in rows:
    for c in r["changes"]:
        if c["category"] == "none": continue
        for i, v in enumerate([r["no"], r["title"], c["priority"], c["category"], c["action"], "todo", ""], 1):
            cell = cs.cell(rr, i, v); cell.alignment = Alignment(wrap_text=True, vertical="top"); cell.border = border
        if c["priority"] == "P1": cs.cell(rr, 3).fill = PatternFill("solid", fgColor="F4B084")
        rr += 1
dv2 = DataValidation(type="list", formula1='"todo,doing,done,skip"', allow_blank=True); cs.add_data_validation(dv2); dv2.add(f"F4:F{rr}")
cs.freeze_panes = "A4"; cs.auto_filter.ref = f"A3:G{rr - 1}"
cs["I3"] = "Summary by category"; cs["I3"].font = Font(bold=True)
for i, cat in enumerate([c for c in T.ENUMS["change_category"] if c != "none"], 4):
    cs.cell(i, 9, cat); cs.cell(i, 10, f'=COUNTIF($D$4:$D${rr},I{i})'); cs.cell(i, 11, f'=COUNTIFS($D$4:$D${rr},I{i},$C$4:$C${rr},"P1")')
cs["J3"] = "All"; cs["K3"] = "P1"; cs.column_dimensions["I"].width = 22

# ---------- Taxonomy ----------
tx = wb.create_sheet("Taxonomy"); tx.column_dimensions["A"].width = 22; tx.column_dimensions["B"].width = 28; tx.column_dimensions["C"].width = 110
tx["A1"] = "Taxonomy used for the labels (exact values, with definitions)"; tx["A1"].font = Font(size=13, bold=True); r_ = 3
for k, vals in T.ENUMS.items():
    for i, (a, b) in enumerate(vals.items()):
        tx.cell(r_, 1, k if i == 0 else "").font = Font(bold=True); tx.cell(r_, 2, a); tx.cell(r_, 3, b).alignment = Alignment(wrap_text=True); r_ += 1
    r_ += 1
tx.cell(r_, 1, "Scores").font = Font(bold=True); tx.cell(r_, 2, "1-5: " + ", ".join(T.SCORES_15) + " | humour_intensity 0-3 | virality_pred 1-10")

# ---------- Method & agreement ----------
mt = wb.create_sheet("Method & reliability"); mt.column_dimensions["A"].width = 34; mt.column_dimensions["B"].width = 14; mt.column_dimensions["C"].width = 90
mt["A1"] = "How the labels were made and how reliable they are"; mt["A1"].font = Font(size=13, bold=True)
txt = [("Code-computed (exact)", "duration, loudness, words/chars, hook length, number/question in hook, CTA repeat count, poster text, voice, inserts, files. These are facts about the files."),
       ("Annotator-labelled", "hook type, basis, topic, structure, humour, emotion, comment trigger, scores, risks, changes. Two blind annotators (editorial analyst; growth analyst) per script batch, then an adjudicator resolved each disagreement against the taxonomy, then a cross-corpus QA critic fixed drift."),
       ("Predicted scores", "Hypotheses from the script text, not measurements. Use the Analytics calibration block once views exist and re-tune the taxonomy and weights."),
       ("Not covered", "Footage quality, on-screen caption timing and the actual video pictures were not scored (annotators read text, not video). Add a visual-review column after a screening."),
       ("QA corrections applied", str(n_corr) + " records changed by the QA critic")]
for i, (a, b) in enumerate(txt, 3): mt.cell(i, 1, a).font = Font(bold=True); mt.cell(i, 3, b).alignment = Alignment(wrap_text=True, vertical="top"); mt.row_dimensions[i].height = 48
mt.cell(10, 1, "Inter-annotator agreement before adjudication (labels: exact match; 1-5 scores: within 1 point; virality: within 2; risk flags: identical sets). Scores look high because of the tolerance; the lowest-agreement fields are risk flags, 2nd hook device, twist position and humour type: treat those labels as softer.").font = Font(bold=True)
mt.cell(10, 1).alignment = Alignment(wrap_text=True); mt.row_dimensions[10].height = 62
for i, (k, v) in enumerate(sorted(agree.items(), key=lambda kv: sum(kv[1]) / len(kv[1])), 11):
    mt.cell(i, 1, k); c = mt.cell(i, 2, round(sum(v) / len(v), 3)); c.number_format = "0%"

# ---------- README ----------
rd = wb.create_sheet("README", 0); rd.column_dimensions["A"].width = 120
lines = ["Football Shorts report: how to use", "",
 "1. Videos: one row per video (100 + 4 pilot splits). Colour bands: ID, Voice, Hook, Story, Humour & emotion, Engagement design, Predicted scores, Production, Poster, Risks & changes, then blue Performance cells to fill in.",
 "2. Fill the blue columns after publishing (platform, date, views, likes, comments, shares, saves, average view duration, % viewed, swipe-away, subscribers, site clicks). Rates and rank calculate by themselves.",
 "3. Analytics: tables by every label (hook type, hook basis, topic, structure, humour, comment trigger, CTA, voice, duration, poster hero) with predicted and measured averages. They update from the Videos sheet.",
 "4. Posters: larger poster previews with headline, joke, colour, emoji, hero source, score, issue and change.",
 "5. Changes backlog: every recommended change, filterable by priority P1 (before publishing) / P2 / P3 and by category.",
 "6. Taxonomy: exact label values with definitions. Method & reliability: what is code-computed, what is labelled, and annotator agreement.",
 "7. Cover as first frame: the poster is embedded as frames 1-3 (0.1 s at 30 fps) of every final video, so players and apps that take the first frame as the preview show it. Audio is untouched (checked bit-for-bit).",
 "8. Predicted values are hypotheses. After 15-20 videos have data, check Analytics > Prediction calibration, then rewrite the weak labels' rules in the method skill.",
 "9. When Codex frames and hero art arrive: rebuild the videos, run cover_frame.py, then report/build_features.py and report/export_report.py to refresh this file (labels stay; code-computed fields update)."]
for i, t in enumerate(lines, 1):
    c = rd.cell(i, 1, t); c.alignment = Alignment(wrap_text=True, vertical="top")
    if i == 1: c.font = Font(size=15, bold=True)
wb.save(f"{H}/FINAL_100/football100_report.xlsx")
# csv (flat, no images): all Videos columns
flat = [k for k, *_ in COLS if k != "thumb"]
with open(f"{H}/FINAL_100/football100_report.csv", "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(flat + [p[0] for p in PERF])
    for r in rows: w.writerow([("" if r.get(k) is None else (r[k].replace("\n", " | ") if isinstance(r.get(k), str) else r.get(k))) for k in flat] + [""] * len(PERF))
print("saved", f"{H}/FINAL_100/football100_report.xlsx", "rows", N, "cols", len(allkeys), "qa corrections", n_corr)
print("first-frame check:", {r["first_frame_cover"] for r in rows})
