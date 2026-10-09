# -*- coding: utf-8 -*-
"""葵小 学年別 行事カレンダー（令和8年度 後期）を作る。

正本は下の EVENTS だけ。1行＝(日付, 終了日 or None, 対象学年, タイトル, 固定キー, 補足)。
学年で中身が違う日（特日4/特日5 など）は、学年ごとに別の行にする。
直したら `py -X utf8 build.py` → git push。購読している人のカレンダーにも半日〜1日で反映される。
UID は「日付＋固定キー＋学年」なので、タイトルを直しても相手側で予定が二重にならない。

出典：静岡市立葵小学校「令和8年度 年間予定表」（配付用・紙）＋学校HPの月行事予定。
学年の割り振りは表の書き方（「1・2年」「5年以外」など）に従い、書いていない行事は全学年に入れる。
委員会・代表委員会は5・6年、クラブは4〜6年として扱う（表に学年の記載がないため）。
"""
import datetime as dt
import html
import json
import pathlib
from urllib.parse import quote

HERE = pathlib.Path(__file__).parent
BASE_URL = "https://ph2144tt0609-cmyk.github.io/aoi-2nen-calendar/"
SCHOOL = "葵小"
NOTE = "静岡市立葵小学校の年間予定表・月行事予定（配付物）から学年ごとに抜き出したものです。学校の予定は変更になる場合があります。最終確認は学校のお手紙でお願いします。"

ALL = (1, 2, 3, 4, 5, 6)
G = lambda *g: tuple(g)

EVENTS = [
    # ---- 10月 ----
    ("2026-10-09", None, ALL, "前期修了・前期終業式（8:25〜8:40）／普通4（13:15下校）", "zenki-shuryo", ""),
    ("2026-10-13", None, ALL, "後期始業式・任命式", "koki-shigyo", ""),
    ("2026-10-14", None, ALL, "学年集会③", "gakunen-3", ""),
    ("2026-10-14", None, G(6), "6年 普通4時間", "6-futsu4-1014", ""),
    ("2026-10-15", None, G(6), "修学旅行①", "shugaku-1", ""),
    ("2026-10-16", None, G(6), "修学旅行②", "shugaku-2", ""),
    ("2026-10-16", None, G(1, 5), "参観会・懇談会②", "sankan-2-15", ""),
    ("2026-10-16", None, ALL, "あおいっ子教室⑫", "aoikko-12", ""),
    ("2026-10-19", None, G(6), "6年 普通4時間", "6-futsu4-1019", ""),
    ("2026-10-21", None, G(1), "音楽集会④（1年の発表）", "ongaku-4", ""),
    ("2026-10-21", None, G(2, 4), "参観会・懇談会②", "sankan-2-24", ""),
    ("2026-10-21", None, ALL, "あおいっ子教室⑬", "aoikko-13", ""),
    ("2026-10-22", None, G(3, 6), "参観会・懇談会②", "sankan-2-36", "3年・6年・5組"),
    ("2026-10-22", None, ALL, "あおいっ子教室⑭", "aoikko-14", ""),
    ("2026-10-23", None, G(5), "就学時健診の児童打合せ（15:00〜・6校時あり）", "shugakuji-uchiawase", ""),
    ("2026-10-24", None, ALL, "ふたばあおい祭り", "futaba-aoi", ""),
    ("2026-10-27", None, G(1, 2, 3, 4, 6), "午前3時間（11:15下校）・就学時健康診断", "shugakuji", ""),
    ("2026-10-27", None, G(5), "【5年お弁当】就学時健康診断", "shugakuji-5", "5年以外は11:15下校"),
    ("2026-10-28", None, ALL, "運動会全校練習①・鑑賞教室（大道芸ワールドカップ）", "undokai-renshu-1", "鑑賞教室＝大道芸ワールドカップ スクールツアー2026（3・4校時）"),
    ("2026-10-30", None, ALL, "あおいっ子教室⑮", "aoikko-15", ""),
    ("2026-10-30", None, G(5, 6), "代表委員会⑤", "daihyo-5", ""),
    # ---- 11月 ----
    ("2026-11-02", None, G(5, 6), "委員会（11月）", "iinkai-11", ""),
    ("2026-11-04", None, ALL, "運動会全校練習②", "undokai-renshu-2", ""),
    ("2026-11-06", None, ALL, "普通4時間（13:15下校）", "futsu4-1106", ""),
    ("2026-11-09", None, G(4, 5, 6), "クラブ④", "club-4", ""),
    ("2026-11-11", None, ALL, "運動会全校練習③", "undokai-renshu-3", ""),
    ("2026-11-13", None, G(1, 2, 3, 4), "特日4（13:10下校）・運動会前日", "undokai-zenjitsu", ""),
    ("2026-11-13", None, G(5, 6), "運動会前日準備（15:00頃下校）", "undokai-junbi", ""),
    ("2026-11-14", None, ALL, "葵大運動会", "undokai", ""),
    ("2026-11-15", None, ALL, "運動会予備日", "undokai-yobi", ""),
    ("2026-11-16", None, ALL, "休業日（運動会の振替）", "undokai-furikae", ""),
    ("2026-11-17", None, ALL, "読み聞かせ⑥", "yomikikase-6", ""),
    ("2026-11-20", None, G(1), "校外学習 秋見つけ（駿府城公園）", "akimitsuke", ""),
    ("2026-11-20", None, ALL, "あおいっ子教室⑯", "aoikko-16", ""),
    ("2026-11-24", "2026-12-04", ALL, "読書旬間②（〜12/4）", "dokusho-2", ""),
    ("2026-11-25", None, ALL, "児童会活動（朝）", "jidokai", ""),
    ("2026-11-25", None, G(1, 6), "あおい交流会③", "koryu-3-16", ""),
    ("2026-11-26", None, G(1, 2, 3), "お話の会", "ohanashi", ""),
    ("2026-11-27", None, ALL, "あおいっ子教室⑰", "aoikko-17", ""),
    ("2026-11-30", None, G(4, 5, 6), "クラブ⑤（最終）", "club-5", ""),
    # ---- 12月 ----
    ("2026-12-02", None, ALL, "普通4時間（13:15下校）", "futsu4-1202", ""),
    ("2026-12-02", None, G(5), "音楽集会⑤（5年の発表）", "ongaku-5", ""),
    ("2026-12-04", None, ALL, "普通4時間（13:15下校）", "futsu4-1204", ""),
    ("2026-12-07", None, G(5, 6), "委員会（12月）", "iinkai-12", ""),
    ("2026-12-08", None, ALL, "読み聞かせ⑦", "yomikikase-7", ""),
    ("2026-12-09", None, G(2, 4), "あおい交流会③", "koryu-3-24", ""),
    ("2026-12-11", None, ALL, "あおいっ子教室", "aoikko-1211", "予定表の表記は「⑯」（11/20と同じ番号）"),
    ("2026-12-11", None, G(5, 6), "学校保健委員会", "hoken-iinkai", ""),
    ("2026-12-16", None, G(6), "音楽集会⑥（6年の発表 8:25〜8:40）", "ongaku-6", ""),
    ("2026-12-16", None, G(3, 5), "あおい交流会③", "koryu-3-35", ""),
    ("2026-12-18", None, ALL, "あおいっ子教室⑲", "aoikko-19", ""),
    ("2026-12-22", None, ALL, "普通4（13:15下校）・給食終了・冬休み前集会", "fuyuyasumi-mae", ""),
    ("2026-12-23", "2027-01-05", ALL, "冬休み（〜1/5）", "fuyuyasumi", ""),
    # ---- 1月 ----
    ("2027-01-06", None, ALL, "特日4（12:05下校）・全校集会", "3gakki-hajime", ""),
    ("2027-01-07", None, ALL, "特日4（12:05下校）・書き初め会期間（〜1/15）", "kakizome", ""),
    ("2027-01-08", None, ALL, "給食開始・定着度調査・あおいっ子教室⑳", "kyushoku-kaishi", ""),
    ("2027-01-12", None, ALL, "【全員お弁当】新春のつどい（あおい交流会④）・普通5時間", "shinshun", ""),
    ("2027-01-12", None, G(5, 6), "委員会（1月）", "iinkai-1", ""),
    ("2027-01-13", "2027-01-19", ALL, "パワーアップweek（〜1/19）", "powerup", ""),
    ("2027-01-13", None, G(5, 6), "発育測定", "hatsuiku-56", ""),
    ("2027-01-14", None, ALL, "朝ノート注文（希望）", "asa-note", ""),
    ("2027-01-14", None, G(1, 2), "発育測定", "hatsuiku-12", ""),
    ("2027-01-15", None, ALL, "月曜日課・全校学活④（SEL）・あおいっ子教室㉑", "aoikko-21", ""),
    ("2027-01-15", None, G(3, 4), "発育測定", "hatsuiku-34", ""),
    ("2027-01-18", None, G(5, 6), "代表委員会⑥", "daihyo-6", ""),
    ("2027-01-19", None, ALL, "読み聞かせ⑧", "yomikikase-8", ""),
    ("2027-01-20", None, ALL, "学年集会④", "gakunen-4", ""),
    ("2027-01-22", None, ALL, "普通4時間（13:15下校）", "futsu4-0122", ""),
    ("2027-01-28", None, G(6), "城内中 新入生説明会・体験授業（14:00予定・城内中）", "jonai-chu", ""),
    ("2027-01-29", None, ALL, "あおいっ子教室㉒", "aoikko-22", ""),
    # ---- 2月 ----
    ("2027-02-02", None, ALL, "読み聞かせ⑨", "yomikikase-9", ""),
    ("2027-02-05", None, G(1), "1年 13:00下校（新1年生保護者説明会）", "shin1nen-setsumei", ""),
    ("2027-02-09", None, G(5, 6), "参観会・懇談会③", "sankan-3-56", "5年・6年・5組"),
    ("2027-02-09", None, ALL, "あおいっ子教室㉓", "aoikko-23", ""),
    ("2027-02-10", None, G(1, 2), "参観会・懇談会③", "sankan-3-12", ""),
    ("2027-02-10", None, ALL, "あおいっ子教室㉔", "aoikko-24", ""),
    ("2027-02-12", None, G(3, 4), "参観会・懇談会③", "sankan-3-34", ""),
    ("2027-02-12", None, ALL, "あおいっ子教室㉕", "aoikko-25", ""),
    ("2027-02-16", None, ALL, "読み聞かせ⑩（最終）", "yomikikase-10", ""),
    ("2027-02-17", None, ALL, "特日5（14:00下校）", "toku-0217", ""),
    ("2027-02-17", None, G(2, 4), "あおい交流会⑤（最終）", "koryu-5-24", ""),
    ("2027-02-19", None, ALL, "【全員お弁当】6年生を送る会・あおいっ子教室㉖", "okuru-kai", ""),
    ("2027-02-19", None, G(1, 6), "あおい交流会⑤（最終）", "koryu-5-16", ""),
    ("2027-02-24", None, G(3, 5), "あおい交流会⑤（最終）", "koryu-5-35", ""),
    ("2027-02-24", None, G(5, 6), "代表委員会⑦（最終）", "daihyo-7", ""),
    ("2027-02-25", None, ALL, "火曜日課・普通5時間", "kayo-nikka", ""),
    ("2027-02-25", None, G(5, 6), "委員会（2月・最終）", "iinkai-2", ""),
    ("2027-02-26", None, ALL, "普通4（13:15下校）・あおいっ子教室㉗（最終）", "aoikko-27", ""),
    # ---- 3月 ----
    ("2027-03-01", None, G(1, 2), "特日4（13:10下校）", "toku-0301", ""),
    ("2027-03-01", None, G(3, 4, 5, 6), "特日5（14:00下校）", "toku-0301", ""),
    ("2027-03-02", None, G(1), "特日4", "toku-0302", ""),
    ("2027-03-02", None, G(2, 3, 4, 5, 6), "特日5", "toku-0302", ""),
    ("2027-03-03", None, ALL, "特日5", "toku-0303", ""),
    ("2027-03-04", None, G(1), "特日4", "toku-0304", ""),
    ("2027-03-04", None, G(2, 3, 4, 5, 6), "特日5", "toku-0304", ""),
    ("2027-03-05", None, ALL, "特日5", "toku-0305", ""),
    ("2027-03-08", None, G(1, 2), "特日4", "toku-0308", ""),
    ("2027-03-08", None, G(3, 4, 5, 6), "特日5", "toku-0308", ""),
    ("2027-03-09", None, G(1, 2, 3, 4, 5), "特日4（13:10下校）", "toku-0309", ""),
    ("2027-03-09", None, G(6), "卒業式総練習（14:45頃下校）", "toku-0309", ""),
    ("2027-03-10", None, ALL, "特日5", "toku-0310", ""),
    ("2027-03-11", None, G(1), "特日4", "toku-0311", ""),
    ("2027-03-11", None, G(2, 3, 4, 5, 6), "特日5", "toku-0311", ""),
    ("2027-03-12", None, ALL, "特日5・学校クリーン活動（大掃除）", "clean", ""),
    ("2027-03-15", None, G(1, 2), "特日4", "toku-0315", ""),
    ("2027-03-15", None, G(3, 4, 5, 6), "特日5", "toku-0315", ""),
    ("2027-03-16", None, G(1), "特日4・給食終了", "kyushoku-shuryo", ""),
    ("2027-03-16", None, G(2, 3, 4, 5, 6), "特日5・給食終了", "kyushoku-shuryo", ""),
    ("2027-03-17", None, G(1, 2, 3, 4, 6), "特日4（12:05下校）", "toku-0317", ""),
    ("2027-03-17", None, G(5), "【5年お弁当】卒業式準備（15:00頃下校）", "toku-0317", ""),
    ("2027-03-18", None, ALL, "卒業証書授与式", "sotsugyo", ""),
    ("2027-03-19", None, ALL, "修了式・特日4（12:05下校）", "shuryo", ""),
    ("2027-03-20", None, ALL, "春休みはじまり", "haruyasumi", ""),
    ("2027-03-26", None, ALL, "離任式", "rinin", ""),
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


def events_for(g):
    return [e for e in EVENTS if g in e[2]]


def build_ics(g, filename):
    name = f"{SCHOOL} {g}年 行事予定"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//aoi-gyoji-calendar//JA", "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH", f"X-WR-CALNAME:{name}", "X-WR-TIMEZONE:Asia/Tokyo",
        f"X-WR-CALDESC:{ics_escape(NOTE)}", "REFRESH-INTERVAL;VALUE=DURATION:PT12H", "X-PUBLISHED-TTL:PT12H",
    ]
    for start, end, grades, title, key, memo in events_for(g):
        s = d(start)
        e = (d(end) if end else s) + dt.timedelta(days=1)
        desc = (memo + "\n" if memo else "") + NOTE
        lines += [
            "BEGIN:VEVENT", f"UID:{start.replace('-', '')}-{key}-g{g}@aoi-gyoji-calendar", f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{s:%Y%m%d}", f"DTEND;VALUE=DATE:{e:%Y%m%d}",
            f"SUMMARY:{ics_escape('🏫 ' + title)}", f"DESCRIPTION:{ics_escape(desc)}",
            "TRANSP:TRANSPARENT", "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    (HERE / filename).write_bytes(("\r\n".join(fold(l) for l in lines) + "\r\n").encode("utf-8"))


def page_data():
    data = {}
    for g in ALL:
        ics_url = f"{BASE_URL}grade{g}.ics"
        webcal = "webcal://" + ics_url.split("://", 1)[1]
        rows = []
        for start, end, grades, title, key, memo in events_for(g):
            s = d(start)
            date = f"{s.month}/{s.day}（{WEEK[s.weekday()]}）"
            if end:
                e = d(end)
                date += f"〜{e.month}/{e.day}"
            rows.append({"ym": f"{s.year}年{s.month}月", "date": date, "title": title, "memo": memo})
        data[g] = {
            "ics": f"grade{g}.ics", "icsUrl": ics_url, "webcal": webcal,
            "google": "https://calendar.google.com/calendar/r?cid=" + quote(webcal, safe=""),
            "rows": rows,
        }
    return data


def build_html():
    tpl = (HERE / "template.html").read_text(encoding="utf-8")
    out = (tpl.replace("{{NOTE}}", html.escape(NOTE)).replace("{{UPDATED}}", f"{dt.date.today():%Y/%m/%d}")
           .replace("{{DATA}}", json.dumps(page_data(), ensure_ascii=False)))
    (HERE / "index.html").write_text(out, encoding="utf-8")


if __name__ == "__main__":
    for g in ALL:
        build_ics(g, f"grade{g}.ics")
    build_ics(2, "aoi-2nen.ics")  # 初版で配ったURLを生かしておく（中身は2年と同じ）
    build_html()
    print("OK:", " / ".join(f"{g}年 {len(events_for(g))}件" for g in ALL))
