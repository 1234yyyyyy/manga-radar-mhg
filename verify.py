from pathlib import Path
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parent
N=len(json.loads((ROOT/"data.json").read_text(encoding="utf-8")))
url=(ROOT/"index.html").as_uri()
errors=[];issues=[]
JSV="""() => [...document.querySelectorAll('.c')].filter(c=>!c.classList.contains('h')).length"""
BAD="""([k,p]) => {const a=k?new RegExp(k,'i'):null,b=p?new RegExp(p,'i'):null,bad=[];
document.querySelectorAll('.c').forEach(c=>{const t=c.querySelector('.k').textContent,on=!c.classList.contains('h'),hit=(!a||a.test(t))&&(!b||b.test(t));if(on!==hit)bad.push(c.querySelector('.n').textContent)});return bad;}"""
with sync_playwright() as p:
    br=p.chromium.launch(executable_path="/opt/google/chrome/chrome",args=["--no-sandbox","--disable-dev-shm-usage"])
    pg=br.new_page(viewport={"width":1280,"height":900})
    pg.on("pageerror",lambda e:errors.append(str(e)))
    pg.on("console",lambda m:errors.append("console:"+m.text) if m.type=="error" else None)
    pg.on("requestfailed",lambda r:errors.append("reqfail:"+r.url))
    pg.goto(url); pg.wait_for_load_state("load")
    n=pg.locator(".c").count(); print("cards",n)
    if n!=N: issues.append("count")
    print("title",pg.title()); print("sub",pg.locator(".s").inner_text())
    # load all lazy images
    pg.evaluate("document.querySelectorAll('img').forEach(i=>i.loading='eager')")
    for y in range(0,20000,600): pg.mouse.wheel(0,600); pg.wait_for_timeout(60)
    pg.wait_for_timeout(1500)
    imgs=pg.evaluate("[...document.querySelectorAll('img')].map(i=>[i.alt,i.complete,i.naturalWidth])")
    broken=[x for x in imgs if not x[1] or x[2]<500]
    print("images",len(imgs),"broken/small",broken)
    if broken: issues.append("images")
    pg.evaluate("window.scrollTo(0,0)")
    ks=pg.locator("#f button[data-k]"); ps=pg.locator("#f button[data-p]")
    for i in range(ks.count()):
        b=ks.nth(i); b.click(); k=b.get_attribute("data-k") or ""
        v=pg.evaluate(JSV); bad=pg.evaluate(BAD,[k,""]); cnt=pg.locator("#cnt").inner_text()
        print(f"genre {b.inner_text()!r} visible={v} cnt={cnt} bad={bad}")
        if bad or str(v) not in cnt or (k and v==0): issues.append("genre "+b.inner_text())
    ks.nth(0).click()
    for i in range(ps.count()):
        b=ps.nth(i); b.click(); k=b.get_attribute("data-p") or ""
        v=pg.evaluate(JSV); bad=pg.evaluate(BAD,["",k])
        print(f"cond {b.inner_text()!r} visible={v} bad={bad}")
        if bad or (k and v==0): issues.append("cond "+b.inner_text())
    # combo
    ks.nth(1).click(); ps.nth(1).click()
    v=pg.evaluate(JSV); bad=pg.evaluate(BAD,[ks.nth(1).get_attribute("data-k"),ps.nth(1).get_attribute("data-p")]); print("combo 科幻奇幻+連載中",v,bad)
    if bad: issues.append("combo")
    ks.nth(0).click(); ps.nth(0).click()
    for term,exp in [("末日",None),("jump+",None),("松本大洋",2),("zzzz不存在",0)]:
        pg.fill("#q",term); v=pg.evaluate(JSV); em=pg.locator("#em").is_visible(); print("search",term,v,"empty-msg",em)
        if exp is not None and v!=exp: issues.append("search "+term)
        if exp==0 and not em: issues.append("empty msg")
        if exp is None and v==0: issues.append("search "+term)
    pg.click("#qc"); v=pg.evaluate(JSV); print("after clear",v)
    if v!=N: issues.append("clear")
    pg.wait_for_timeout(500)
    pg.screenshot(path=str(ROOT/"preview.png"),full_page=True)
    m=br.new_page(viewport={"width":390,"height":844}); m.goto(url); m.wait_for_timeout(1500); m.screenshot(path=str(ROOT/"research/mobile.png"))
    br.close()
print("errors",errors); print("ISSUES",issues or "none")
