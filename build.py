"""試做版・漫畫櫃精選。資料在 data.json，封面在 img/（外部檔、lazy-load）。
只產生本資料夾的 index.html；不動 manga-radar / manga-radar-jp。"""
import html, json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
DATE = "2026-11-07"
N = len(DATA)
e = html.escape

for it in DATA:
    p = ROOT / "img" / f"{it['id']}.jpg"
    im = Image.open(p).convert("RGB")
    if im.width > 720:
        im = im.resize((720, round(im.height * 720 / im.width)), Image.Resampling.LANCZOS)
        im.save(p, "JPEG", quality=86, optimize=True)
    it["_wh"] = Image.open(p).size

LV = {"高": "hi", "中": "mid", "低": "lo"}
cards = []
for i, it in enumerate(DATA, 1):
    tags = ["#" + g for g in it["genres"]]
    tags += ["#" + it["status"], "#預測" + it["anime"], "#有台灣正版" if it["twok"] else "#沒台灣正版"]
    if float(it["score"]) >= 9.3:
        tags.append("#高分")
    hidden = " ".join(tags + ["#" + t for t in it["tags"]] + [it["jp"], it["author"], it["mag"]])
    w, h = it["_wh"]
    mhg = f"https://tw.manhuagui.com/comic/{it['mhg']}/"
    links = f'<a class="b r" href="{e(mhg)}" target="_blank" rel="noopener">漫畫櫃閱讀</a>'
    if it["read"]:
        links += f'<a class="b" href="{e(it["read"])}" target="_blank" rel="noopener">官方試閱・{e(it["read_label"])}</a>'
    links += f'<a class="b" href="{e(it["pub"])}" target="_blank" rel="noopener">官方頁面</a>'
    ev = "".join(f"<li>{e(x)}</li>" for x in it["evidence"])
    cards.append(
        f'<div class="c" data-ni="{e(it["zh"])}" data-g="{e("、".join(it["genres"]))}">'
        f'<img src="img/{it["id"]}.jpg" width="{w}" height="{h}" alt="{e(it["jp"])} 封面" loading="lazy">'
        f'<div class="t"><div class="n">{i}. {e(it["zh"])}<span class="tr">漫畫櫃譯名</span></div>'
        f'<div class="jp">{e(it["jp"])}</div>'
        f'<div class="m">{e(it["author"])}・{e(it["mag"])}</div>'
        f'<div class="m2">{e("、".join(it["genres"]))}・日本：{e(it["jpstat"])}</div>'
        f'<div class="mg"><span class="sc">★ {e(it["score"])}</span> 漫畫櫃評分（{e(it["votes"])} 票）・{e(it["status"])}・最新 {e(it["latest"])}</div>'
        f'<div class="an {LV[it["anime"]]}"><b>動畫化預測：{e(it["anime"])}</b>（我們的押注）｜{e(it["anime_why"])}</div>'
        f'<p>{e(it["pitch"])}</p>'
        f'<ul class="ev">{ev}</ul>'
        f'<div class="st"><b>從哪開始看</b>：{e(it["start"])}</div>'
        f'<div class="zh{"" if it["twok"] else " none"}">台灣正版：{e(it["tw"])}</div>'
        f'<div class="ls">{links}</div>'
        f'<span class="k">{e(hidden)}</span></div></div>'
    )

row1 = [("全部", ""), ("科幻奇幻", "#科幻奇幻"), ("懸疑恐怖", "#懸疑恐怖"), ("動作", "#動作"),
        ("喜劇日常", "#喜劇日常"), ("青春", "#青春"), ("社會人生", "#社會人生"), ("短篇連作", "#短篇連作")]
row2 = [("全部", ""), ("連載中", "#連載中"), ("已完結", "#已完結"), ("有台灣正版", "#有台灣正版"),
        ("沒台灣正版", "#沒台灣正版"), ("漫畫櫃 9.3 分以上", "#高分"), ("動畫化預測：高", "#預測高")]
cb = "".join(f'<button data-k="{e(k)}"{" class=on" if not k else ""}>{e(n)}</button>' for n, k in row1)
pb = "".join(f'<button data-p="{e(k)}"{" class=on" if not k else ""}>{e(n)}</button>' for n, k in row2)

CSS = '''body{margin:0;font-family:-apple-system,"PingFang TC","Noto Sans TC","Microsoft JhengHei",sans-serif;background:#111;color:#eee}
h1{font-size:22px;padding:20px 16px 4px;margin:0}h1 .tag{display:inline-block;font-size:13px;background:#2e7dbf;color:#fff;border-radius:6px;padding:2px 8px;margin-left:8px;vertical-align:middle}
.s{color:#aaa;padding:0 16px 4px;font-size:13px;line-height:1.6}.note{color:#888;padding:0 16px 12px;font-size:12px;line-height:1.6}
.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;padding:0 16px 24px}
.c{background:#1c1c1c;border-radius:12px;overflow:hidden;display:flex;flex-direction:column}
.c img{width:100%;height:340px;object-fit:cover;object-position:top;display:block;background:#000}
.t{padding:12px 14px 14px;display:flex;flex-direction:column;flex:1}.n{font-weight:700;font-size:17px}.tr{font-size:11px;font-weight:400;color:#999;border:1px solid #444;border-radius:4px;padding:0 4px;margin-left:6px;vertical-align:2px}
.jp{color:#bbb;font-size:13px;margin-top:2px}.m{color:#f5a623;font-size:12px;margin-top:6px}.m2{color:#9ab;font-size:12px;margin-top:2px;line-height:1.5}
.mg{font-size:12px;color:#bbb;margin-top:6px;line-height:1.5}.mg .sc{color:#111;background:#f5c542;border-radius:6px;padding:1px 6px;font-weight:700}
.an{font-size:13px;line-height:1.5;margin-top:8px;padding:6px 8px;border-radius:8px;background:#26221a}.an b{font-size:14px}.an.hi b{color:#ff6b5b}.an.mid b{color:#f5c542}.an.lo b{color:#7fbf8f}
p{margin:8px 0 0;font-size:14px;line-height:1.6;color:#ddd}.ev{margin:8px 0 0;padding-left:18px;font-size:12px;color:#aaa;line-height:1.6}
.st{margin-top:8px;font-size:13px;line-height:1.5;color:#cde;background:#1a2229;border-radius:8px;padding:6px 8px}.st b{color:#7fc4ff}
.zh{margin-top:8px;font-size:12px;color:#6fd3a0}.zh.none{color:#c9a}
.ls{margin-top:auto;padding-top:10px;display:flex;flex-wrap:wrap;gap:8px}.b{font-size:13px;text-decoration:none;color:#ddd;border:1px solid #444;border-radius:999px;padding:5px 12px}.b:hover{border-color:#888}.b.r{background:#f5a623;color:#111;border-color:#f5a623;font-weight:700}
.k{display:none}.c.h{display:none}
.f{position:sticky;top:0;z-index:5;background:#111;display:flex;flex-wrap:wrap;gap:8px;padding:10px 16px 12px;border-bottom:1px solid #222;margin-bottom:12px}
.f button{background:#1c1c1c;color:#ddd;border:1px solid #333;border-radius:999px;padding:6px 14px;font-size:14px;cursor:pointer;font-family:inherit}.f button:hover{border-color:#666}
.f button.on{background:#f5a623;color:#111;border-color:#f5a623;font-weight:700}.f .pr{flex-basis:100%;display:flex;flex-wrap:wrap;gap:8px}.f .pr button.on{background:#3a8f5c;border-color:#3a8f5c;color:#fff}
.f .cnt{color:#888;font-size:13px;align-self:center;margin-left:4px}.sb{flex-basis:100%;display:flex;gap:8px;margin-bottom:2px}
.sb input{flex:1;min-width:0;background:#1c1c1c;color:#eee;border:1px solid #333;border-radius:10px;padding:9px 12px;font-size:16px;font-family:inherit}.sb input:focus{outline:none;border-color:#f5a623}.sb button{flex:none}
#em{display:none;color:#888;text-align:center;padding:30px 16px}.ft{color:#777;font-size:12px;line-height:1.7;padding:8px 16px 30px;border-top:1px solid #222}'''

JS = r'''(function(){var bs=document.querySelectorAll('#f button[data-k]'),ps=document.querySelectorAll('#f button[data-p]'),cs=document.querySelectorAll('.c'),cnt=document.getElementById('cnt'),q=document.getElementById('q'),em=document.getElementById('em'),cat='',pri='';
function run(){var re=cat?new RegExp(cat,'i'):null,rp=pri?new RegExp(pri,'i'):null,ts=q.value.trim().toLowerCase().split(/\s+/).filter(Boolean),n=0;
cs.forEach(function(c){var tags=c.querySelector('.k').textContent;var all=c.querySelector('.t').textContent.toLowerCase();var ok=(!re||re.test(tags))&&(!rp||rp.test(tags))&&ts.every(function(w){return all.indexOf(w)>=0});c.classList.toggle('h',!ok);if(ok)n++});
cnt.textContent=n+' 部';em.style.display=n?'none':'block';}
bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){x.classList.remove('on')});b.classList.add('on');cat=b.dataset.k;run();});});
ps.forEach(function(b){b.addEventListener('click',function(){ps.forEach(function(x){x.classList.remove('on')});b.classList.add('on');pri=b.dataset.p;run();});});
q.addEventListener('input',run);document.getElementById('qc').addEventListener('click',function(){q.value='';run();q.focus();});})();'''

ntw = sum(1 for x in DATA if not x["twok"])
NI = (Path(__file__).parent / 'ni_snippet.html').read_text(encoding='utf-8')
H = f'''<!DOCTYPE html><html lang="zh-Hant-TW"><head><link rel="icon" href="favicon.svg" type="image/svg+xml"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>試做版・漫畫櫃精選｜漫畫雷達</title><style>
{CSS}</style></head>
<body><h1>漫畫櫃上還沒動畫化的好作品<span class="tag">試做版・漫畫櫃精選</span></h1>
<div class="s">共 {N} 部・資料日期 {DATE}・條件：漫畫櫃上看得到、到 2026 年 11 月都還沒宣布動畫化、不是大眾熱門作・從漫畫櫃高分榜挑候選，再用日本漫畫獎、MAL／AniList 一部部查證</div>
<div class="note">動畫化預測是漫畫雷達自己的押注，不是官方消息，之後會回來對答案。漫畫櫃是網路漢化站，{N - ntw} 部已經有台灣正版，喜歡的話請支持正版。漫畫櫃評分與最新話數是 {DATE} 的數字。</div>
<div class="f" id="f"><div class="sb"><input id="q" type="search" placeholder="搜尋作品、作者、關鍵字（例：末日、職人、Jump+）" autocomplete="off"><button id="qc" type="button">清除</button></div>{cb}<div class="pr">{pb}<span class="cnt" id="cnt">{N} 部</span></div></div>
<div id="em">找不到符合的項目</div><div class="g">{"".join(cards)}</div>
<div class="ft">查證方式（{DATE}）：漫畫櫃評分、狀態、最新話數直接讀漫畫櫃作品頁和搜尋頁；動畫化查日文新聞、出版社官方頁和 AniList 關聯作品；台灣正版用誠品線上、金石堂書目查作者和日文書名；MAL 評分讀 MyAnimeList 作品頁，評分人數太少的改列 AniList 平均分或不列。<br>
已排除：漫畫雷達原版 25 部、「還沒有中文版的日本好作品」14 部，以及已動畫化或已宣布動畫化的作品（例如《みいちゃんと山田さん》已宣布動畫化，所以沒放）。<br>
來源：マンガ大賞、このマンガがすごい！、手塚治虫文化賞、次にくるマンガ大賞、CREA夜ふかしマンガ大賞、艾斯納獎。封面來自各出版社與書店的公開書影。</div>
<script>
{JS}
</script>{NI}</body></html>'''
(ROOT / "index.html").write_text(H, encoding="utf-8")
print("bytes", len(H.encode()), "cards", N)
