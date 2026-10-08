# -*- coding: utf-8 -*-
"""葵小 2年 行事カレンダー（令和8年度 後期）を作る。

正本は下の EVENTS だけ。直したら `py -X utf8 build.py` → git push で、
購読している人のカレンダーにも数時間〜1日で反映される。
UID は「日付＋連番ではなく日付＋固定キー」にしてあるので、タイトルを直しても
相手側で予定が二重にならない（同じ日に予定を足すときはキーを新しく付ける）。
"""
import datetime as dt
import html
import pathlib

HERE = pathlib.Path(__file__).parent
CAL_NAME = "葵小 2年 行事予定"
BASE_URL = "https://ph2144tt0609-cmyk.github.io/aoi-2nen-calendar/"
ICS_NAME = "aoi-2nen.ics"
NOTE = "静岡市立葵小学校の年間予定表・月行事予定（配付物）から2年生に関係する行事を抜き出したものです。学校の予定は変更になる場合があります。"

# (開始日, 終了日(含む) or None, タイトル, 固定キー, 補足)
EVENTS = [
    ("2026-10-09", None, "前期修了・前期終業式／普通4（13:15下校）", "zenki-shuryo", ""),
    ("2026-10-13", None, "後期始業式・任命式", "koki-shigyo", ""),
    ("2026-10-14", None, "学年集会③", "gakunen-3", ""),
    ("2026-10-16", None, "あおいっ子教室⑫", "aoikko-12", ""),
    ("2026-10-21", None, "参観会・懇談会②（2・4年）・あおいっ子教室⑬", "sankan-2", ""),
    ("2026-10-22", None, "あおいっ子教室⑭", "aoikko-14", ""),
    ("2026-10-24", None, "ふたばあおい祭", "futaba-aoi", ""),
    ("2026-10-27", None, "午前3時間（11:15下校）・就学時健康診断", "shugakuji", ""),
    ("2026-10-28", None, "運動会全校練習①・鑑賞教室（大道芸ワールドカップ）", "undokai-renshu-1", "鑑賞教室＝大道芸ワールドカップ スクールツアー2026（3・4校時）"),
    ("2026-10-30", None, "あおいっ子教室⑮", "aoikko-15", ""),
    ("2026-11-04", None, "運動会全校練習②", "undokai-renshu-2", ""),
    ("2026-11-06", None, "普通4時間（13:15下校）", "futsu4-1106", ""),
    ("2026-11-11", None, "運動会全校練習③", "undokai-renshu-3", ""),
    ("2026-11-13", None, "特日4（13:10下校）・運動会前日", "undokai-zenjitsu", ""),
    ("2026-11-14", None, "葵大運動会", "undokai", ""),
    ("2026-11-15", None, "運動会予備日", "undokai-yobi", ""),
    ("2026-11-16", None, "休業日（運動会の振替）", "undokai-furikae", ""),
    ("2026-11-17", None, "読み聞かせ⑥", "yomikikase-6", ""),
    ("2026-11-20", None, "あおいっ子教室⑯", "aoikko-16", ""),
    ("2026-11-24", "2026-12-04", "読書旬間②（〜12/4）", "dokusho-2", ""),
    ("2026-11-26", None, "お話の会（1・2・3年）", "ohanashi", ""),
    ("2026-11-27", None, "あおいっ子教室⑰", "aoikko-17", ""),
    ("2026-12-02", None, "普通4時間（13:15下校）", "futsu4-1202", ""),
    ("2026-12-04", None, "普通4時間（13:15下校）", "futsu4-1204", ""),
    ("2026-12-08", None, "読み聞かせ⑦", "yomikikase-7", ""),
    ("2026-12-09", None, "あおい交流会③（2・4年）", "koryu-3", ""),
    ("2026-12-11", None, "あおいっ子教室", "aoikko-1211", "予定表の表記は「⑯」（11/20と同じ番号）"),
    ("2026-12-18", None, "あおいっ子教室⑲", "aoikko-19", ""),
    ("2026-12-22", None, "普通4（13:15下校）・給食終了・冬休み前集会", "fuyuyasumi-mae", ""),
    ("2026-12-23", "2027-01-05", "冬休み（〜1/5）", "fuyuyasumi", ""),
    ("2027-01-06", None, "特日4（12:05下校）・全校集会", "3gakki-hajime", ""),
    ("2027-01-07", None, "特日4（12:05下校）・書き初め会期間（〜1/15）", "kakizome", ""),
    ("2027-01-08", None, "給食開始・定着度調査・あおいっ子教室⑳", "kyushoku-kaishi", ""),
    ("2027-01-12", None, "【全員お弁当】新春のつどい（あおい交流会④）・普通5時間", "shinshun", "全員弁当の日"),
    ("2027-01-13", "2027-01-19", "パワーアップweek（〜1/19）", "powerup", ""),
    ("2027-01-14", None, "発育測定（1・2年）・朝ノート注文（希望）", "hatsuiku-12", ""),
    ("2027-01-15", None, "月曜日課・全校学活④（SEL）・あおいっ子教室㉑", "aoikko-21", ""),
    ("2027-01-19", None, "読み聞かせ⑧", "yomikikase-8", ""),
    ("2027-01-20", None, "学年集会④", "gakunen-4", ""),
    ("2027-01-22", None, "普通4時間（13:15下校）", "futsu4-0122", ""),
    ("2027-01-29", None, "あおいっ子教室㉒", "aoikko-22", ""),
    ("2027-02-02", None, "読み聞かせ⑨", "yomikikase-9", ""),
    ("2027-02-09", None, "あおいっ子教室㉓", "aoikko-23", ""),
    ("2027-02-10", None, "参観会・懇談会③（1・2年）・あおいっ子教室㉔", "sankan-3", ""),
    ("2027-02-12", None, "あおいっ子教室㉕", "aoikko-25", ""),
    ("2027-02-16", None, "読み聞かせ⑩（最終）", "yomikikase-10", ""),
    ("2027-02-17", None, "特日5（14:00下校）・あおい交流会⑤（2・4年 最終）", "koryu-5", ""),
    ("2027-02-19", None, "【全員お弁当】6年生を送る会・あおいっ子教室㉖", "okuru-kai", "全員弁当の日"),
    ("2027-02-25", None, "火曜日課・普通5時間", "kayo-nikka", ""),
    ("2027-02-26", None, "普通4（13:15下校）・あおいっ子教室㉗（最終）", "aoikko-27", ""),
    ("2027-03-01", None, "特日4（13:10下校）", "toku-0301", ""),
    ("2027-03-02", None, "特日5", "toku-0302", ""),
    ("2027-03-03", None, "特日5", "toku-0303", ""),
    ("2027-03-04", None, "特日5", "toku-0304", ""),
    ("2027-03-05", None, "特日5", "toku-0305", ""),
    ("2027-03-08", None, "特日4", "toku-0308", ""),
    ("2027-03-09", None, "特日4（13:10下校）", "toku-0309", ""),
    ("2027-03-10", None, "特日5", "toku-0310", ""),
    ("2027-03-11", None, "特日5", "toku-0311", ""),
    ("2027-03-12", None, "特日5・学校クリーン活動（大掃除）", "clean", ""),
    ("2027-03-15", None, "特日4", "toku-0315", ""),
    ("2027-03-16", None, "特日5・給食終了", "kyushoku-shuryo", ""),
    ("2027-03-17", None, "特日4（12:05下校）", "toku-0317", ""),
    ("2027-03-18", None, "卒業証書授与式", "sotsugyo", ""),
    ("2027-03-19", None, "修了式・特日4（12:05下校）", "shuryo", ""),
    ("2027-03-20", None, "春休みはじまり", "haruyasumi", ""),
    ("2027-03-26", None, "離任式", "rinin", ""),
]

WEEK = "月火水木金土日"


def d(s):
    return dt.date.fromisoformat(s)


def ics_escape(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line):
    """RFC 5545 の75オクテット折り返し（UTF-8の文字の途中で切らない）"""
    out, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > 74:
            out.append(cur)
            cur = b" "
        cur += b
    out.append(cur)
    return b"\r\n".join(out).decode("utf-8")


def build_ics():
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//aoi-2nen-calendar//JA", "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH", f"X-WR-CALNAME:{CAL_NAME}", "X-WR-TIMEZONE:Asia/Tokyo",
        f"X-WR-CALDESC:{ics_escape(NOTE)}", "REFRESH-INTERVAL;VALUE=DURATION:PT12H", "X-PUBLISHED-TTL:PT12H",
    ]
    for start, end, title, key, memo in EVENTS:
        s = d(start)
        e = (d(end) if end else s) + dt.timedelta(days=1)
        desc = (memo + "\n" if memo else "") + NOTE
        lines += [
            "BEGIN:VEVENT", f"UID:{start.replace('-', '')}-{key}@aoi-2nen-calendar", f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{s:%Y%m%d}", f"DTEND;VALUE=DATE:{e:%Y%m%d}",
            f"SUMMARY:{ics_escape('🏫 ' + title)}", f"DESCRIPTION:{ics_escape(desc)}",
            "TRANSP:TRANSPARENT", "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    (HERE / ICS_NAME).write_bytes(("\r\n".join(fold(l) for l in lines) + "\r\n").encode("utf-8"))


def build_html():
    ics_url = BASE_URL + ICS_NAME
    webcal = "webcal://" + ics_url.split("://", 1)[1]
    from urllib.parse import quote
    google = "https://calendar.google.com/calendar/r?cid=" + quote(webcal, safe="")
    rows, cur_month = [], None
    for start, end, title, key, memo in EVENTS:
        s = d(start)
        if s.month != cur_month:
            cur_month = s.month
            rows.append(f'<h3>{s.year}年{s.month}月</h3>')
        date = f"{s.month}/{s.day}（{WEEK[s.weekday()]}）"
        if end:
            e = d(end)
            date += f"〜{e.month}/{e.day}"
        m = f'<span class="memo">{html.escape(memo)}</span>' if memo else ""
        rows.append(f'<div class="ev"><span class="dt">{date}</span><span class="tt">{html.escape(title)}{m}</span></div>')
    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    out = (tpl.replace("{{CAL_NAME}}", html.escape(CAL_NAME)).replace("{{NOTE}}", html.escape(NOTE))
           .replace("{{WEBCAL}}", webcal).replace("{{GOOGLE}}", google).replace("{{ICS}}", ICS_NAME)
           .replace("{{ICS_URL}}", ics_url).replace("{{COUNT}}", str(len(EVENTS)))
           .replace("{{UPDATED}}", f"{dt.date.today():%Y/%m/%d}").replace("{{ROWS}}", "\n".join(rows)))
    (HERE / "index.html").write_text(out, encoding="utf-8")


if __name__ == "__main__":
    build_ics()
    build_html()
    print(f"OK: {len(EVENTS)}件 → {ICS_NAME} / index.html")
