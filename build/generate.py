#!/usr/bin/env python3
"""AlHafeez site generator. Optional: edit CONFIG and re-run to rebuild all pages."""
import os, random, math, shutil

OUT = os.environ.get("OUT", "alhafeez-website")
CONFIG = {
    "brand": "AlHafeez",
    "tagline": "Residences in the canopy",
    "email": "visits@aaranyaresidences.com",
    "phone": "+92 21 3587 4920",
    "address": "42 Canopy Grove, Clifton Block 4, Karachi",
    "cta": "Book a private visit",
}
B = CONFIG["brand"]

PAGES = [
    ("index", "Home"), ("architecture", "Architecture"), ("residences", "Residences"),
    ("terrace-residence", "Terrace Residence"), ("garden-residence", "Garden Residence"),
    ("sky-penthouse", "Sky Penthouse"), ("amenities", "Amenities"), ("materials", "Materials"),
    ("sustainability", "Sustainability"), ("gallery", "Gallery"), ("location", "Location"),
    ("visit", "Contact"),
]
NAV = [("architecture", "Architecture"), ("residences", "Residences"), ("amenities", "Amenities"),
       ("location", "Location"), ("visit", "Contact")]

# ---------------------------------------------------------------- SVG art
def svg_wrap(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice">'
            f'<defs>{defs}</defs>{body}</svg>')

def palm(x, y, s, rnd):
    out = f'<path d="M{x} {y} q{rnd.randint(-8,8)*s} {-60*s} {rnd.randint(-10,10)*s} {-120*s}" stroke="#2b2118" stroke-width="{3*s}" fill="none"/>'
    tx, ty = x, y - 120 * s
    for a in range(-80, 100, 28):
        r = math.radians(a - 90)
        ex, ey = tx + math.cos(r) * 70 * s, ty + math.sin(r) * 40 * s + 18 * s
        out += f'<path d="M{tx} {ty} Q{(tx+ex)/2} {ty-26*s} {ex} {ey}" stroke="#2f5a3a" stroke-width="{4*s}" fill="none" stroke-linecap="round"/>'
    return out

def building(w=1600, h=900, seed=1, zoom=1.0, cx=None, floors=8):
    rnd = random.Random(seed)
    cx = cx or w * 0.58
    defs = ('<linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3a3a"/>'
            '<stop offset=".55" stop-color="#8d8a78"/><stop offset="1" stop-color="#d9b98a"/></linearGradient>'
            '<linearGradient id="gl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#27383a"/><stop offset="1" stop-color="#0f1b1a"/></linearGradient>'
            '<linearGradient id="gr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1d3a2b"/><stop offset="1" stop-color="#0c1a12"/></linearGradient>')
    b = f'<rect width="{w}" height="{h}" fill="url(#sk)"/>'
    for i in range(5):  # soft clouds
        b += f'<ellipse cx="{rnd.randint(0,w)}" cy="{rnd.randint(40,260)}" rx="{rnd.randint(200,420)}" ry="{rnd.randint(18,40)}" fill="#e8dcc4" opacity=".12"/>'
    b += f'<path d="M0 {h*.62} Q{w*.25} {h*.48} {w*.5} {h*.6} T{w} {h*.56} V{h} H0Z" fill="#35493c" opacity=".7"/>'
    bw, fh = 560 * zoom, 70 * zoom
    top = h * .78 - fh * floors
    for i in range(floors):
        off = (24 * zoom if i % 2 else 0) + (14 * zoom if i % 3 == 0 else 0)
        x = cx - bw / 2 + off
        y = top + i * fh
        bwi = bw - off * 1.4
        b += f'<rect x="{x}" y="{y}" width="{bwi}" height="{fh}" fill="url(#gl)"/>'
        # timber fins
        n = int(bwi / (14 * zoom))
        fins = "".join(f'<rect x="{x+k*14*zoom+3}" y="{y}" width="{4*zoom}" height="{fh-10*zoom}" fill="#a9753f" opacity=".92"/>' for k in range(n))
        b += fins
        # slab + terrace overhang
        b += f'<rect x="{x-26*zoom}" y="{y+fh-12*zoom}" width="{bwi+52*zoom}" height="{12*zoom}" fill="#d8ceb8"/>'
        # planters
        for k in range(int(bwi / (60 * zoom))):
            px = x - 14 * zoom + k * 60 * zoom + rnd.randint(0, 20)
            b += f'<ellipse cx="{px}" cy="{y+fh-14*zoom}" rx="{26*zoom}" ry="{10*zoom}" fill="#3d7a4c" opacity=".9"/>'
            b += f'<ellipse cx="{px+10}" cy="{y+fh-8*zoom}" rx="{16*zoom}" ry="{16*zoom}" fill="#2b5c3a" opacity=".85"/>'
    b += f'<rect x="0" y="{h*.78}" width="{w}" height="{h*.22}" fill="url(#gr)"/>'
    for i in range(7):
        b += palm(rnd.randint(40, w - 40), h * .8 + rnd.randint(0, 80), rnd.choice([1, 1.2, 1.6]), rnd)
    for i in range(40):
        b += f'<ellipse cx="{rnd.randint(0,w)}" cy="{h*.86+rnd.randint(0,90)}" rx="{rnd.randint(30,90)}" ry="{rnd.randint(12,30)}" fill="#2f6a42" opacity=".75"/>'
    b += f'<rect width="{w}" height="{h}" fill="#0b1510" opacity=".12"/>'
    # warm windows
    return svg_wrap(w, h, b, defs)

def interior(seed=2, tone="#cdbfa3"):
    rnd = random.Random(seed)
    w, h = 1200, 800
    defs = ('<linearGradient id="v" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fb2a4"/><stop offset="1" stop-color="#e5d6b4"/></linearGradient>')
    b = f'<rect width="{w}" height="{h}" fill="{tone}"/>'
    b += f'<rect x="120" y="90" width="620" height="420" fill="url(#v)"/>'
    for k in range(10):
        b += f'<rect x="{120+k*62}" y="90" width="7" height="420" fill="#a9753f"/>'
    b += f'<ellipse cx="260" cy="420" rx="120" ry="60" fill="#2f6a42" opacity=".8"/>'
    b += f'<rect x="0" y="520" width="{w}" height="280" fill="#8a6a45"/>'
    for k in range(14):
        b += f'<rect x="{k*90}" y="520" width="3" height="280" fill="#5e4527" opacity=".5"/>'
    b += '<rect x="780" y="300" width="340" height="230" rx="10" fill="#26231f"/><rect x="800" y="270" width="300" height="60" rx="20" fill="#34302a"/>'
    b += '<rect x="330" y="560" width="300" height="120" rx="14" fill="#efe8d8"/><rect x="330" y="540" width="300" height="40" rx="14" fill="#e0d5bd"/>'
    b += f'<circle cx="980" cy="160" r="46" fill="#efe8d8" opacity=".85"/>'
    return svg_wrap(w, h, b, defs)

def pool(seed=3):
    w, h = 1200, 800
    defs = '<linearGradient id="p" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5f9a93"/><stop offset="1" stop-color="#1f4f52"/></linearGradient>'
    b = f'<rect width="{w}" height="{h}" fill="#e2d6bb"/><rect x="140" y="240" width="920" height="380" rx="26" fill="url(#p)"/>'
    for k in range(9):
        b += f'<path d="M160 {270+k*38} q120 -20 240 0 t240 0 t240 0 t200 0" stroke="#cfe6df" stroke-width="2" fill="none" opacity=".4"/>'
    b += '<rect x="0" y="640" width="1200" height="160" fill="#a9753f"/>'
    rnd = random.Random(seed)
    for s in (1.4, 1.1, 1.6):
        b += palm(rnd.randint(80, 1100), 700, s, rnd)
    return svg_wrap(w, h, b, defs)

def materials(seed=4):
    sw = [("#a9753f", "timber"), ("#d8ceb8", "limestone"), ("#26231f", "charcoal"), ("#1d3a2b", "forest"), ("#cdbfa3", "beige"), ("#3d7a4c", "planting")]
    w, h = 1200, 800
    b = f'<rect width="{w}" height="{h}" fill="#efe8d8"/>'
    for i, (c, _) in enumerate(sw):
        x, y = 60 + (i % 3) * 380, 60 + (i // 3) * 370
        b += f'<rect x="{x}" y="{y}" width="340" height="330" rx="6" fill="{c}"/>'
        if c == "#a9753f":
            b += "".join(f'<rect x="{x+k*22+8}" y="{y}" width="6" height="330" fill="#7a5128" opacity=".6"/>' for k in range(15))
        if c == "#d8ceb8":
            b += "".join(f'<path d="M{x} {y+k*40} h340" stroke="#bdb198" stroke-width="2"/>' for k in range(1, 8))
    return svg_wrap(w, h, b)

def mapsvg():
    w, h = 1200, 800
    b = f'<rect width="{w}" height="{h}" fill="#dfd6c0"/>'
    rnd = random.Random(7)
    for i in range(14):
        b += f'<path d="M{rnd.randint(0,w)} 0 Q{rnd.randint(0,w)} {h/2} {rnd.randint(0,w)} {h}" stroke="#f4eddb" stroke-width="{rnd.choice([8,14,22])}" fill="none"/>'
    b += '<path d="M0 560 Q300 440 600 560 T1200 500 V800 H0Z" fill="#9db7a0" opacity=".75"/>'
    b += '<circle cx="600" cy="380" r="90" fill="#a9753f" opacity=".18"/><circle cx="600" cy="380" r="26" fill="#14261d"/><circle cx="600" cy="380" r="9" fill="#efe8d8"/>'
    for i, (x, y) in enumerate([(300, 230), (880, 260), (940, 560), (260, 560), (720, 640)]):
        b += f'<circle cx="{x}" cy="{y}" r="12" fill="#26231f"/><circle cx="{x}" cy="{y}" r="4" fill="#efe8d8"/>'
    return svg_wrap(w, h, b)

def logo():
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 270 60"><g fill="none" stroke="#efe8d8" stroke-width="2">'
            '<path d="M8 50 V14 L26 4 L44 14 V50"/><path d="M17 50 V24 M26 50 V18 M35 50 V24"/></g>'
            '<text x="62" y="40" font-family="Georgia,serif" font-size="30" letter-spacing="6" fill="#efe8d8">AlHafeez</text></svg>')

def write(path, data):
    p = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(data)

# ---------------------------------------------------------------- CSS
CSS = r"""
/* AlHafeez — shared responsive styles. */
:root{--forest:#14261d;--forest2:#1d3a2b;--char:#26231f;--cream:#efe8d8;--lime:#e6dcc5;--beige:#cdbfa3;--timber:#a9753f;--ink:#1a1814;
--serif:"Cormorant Garamond",Georgia,"Times New Roman",serif;--sans:"Inter",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--gut:clamp(20px,5vw,72px)}
*{box-sizing:border-box;margin:0}
html{scroll-behavior:smooth;scroll-padding-top:80px}
body{background:var(--cream);color:var(--ink);font-family:var(--sans);font-size:16px;line-height:1.7;-webkit-font-smoothing:antialiased}
html,body{overflow-x:clip}
img{max-width:100%;display:block}
a{color:inherit}
:focus-visible{outline:2px solid var(--timber);outline-offset:3px;border-radius:2px}
.skip{position:absolute;left:-999px;top:8px;background:var(--cream);color:var(--ink);padding:10px 16px;z-index:100}.skip:focus{left:8px}
h1,h2,h3{font-family:var(--serif);font-weight:400;line-height:1.15;letter-spacing:-.01em}
h1{font-size:clamp(2.8rem,8vw,7rem)}h2{font-size:clamp(2.1rem,5vw,4.2rem)}h3{font-size:clamp(1.5rem,2.6vw,2.1rem)}
.eyebrow{font-size:.72rem;letter-spacing:.28em;text-transform:uppercase;color:var(--timber);font-weight:500;display:block;margin-bottom:1.1rem}
.dark .eyebrow{color:var(--beige)}
.lead{font-size:clamp(1.05rem,1.5vw,1.3rem);max-width:56ch;opacity:.85}
.wrap{padding:clamp(72px,11vw,160px) var(--gut)}
.dark{background:var(--forest);color:var(--cream)}.char{background:var(--char);color:var(--cream)}.lime{background:var(--lime)}
/* progress bar (scroll-linked) */
.progress{position:fixed;inset:0 0 auto 0;height:3px;background:var(--timber);transform-origin:0 50%;transform:scaleX(0);z-index:60}
@supports (animation-timeline:scroll()){.progress{animation:prog linear both;animation-timeline:scroll(root)}}
@keyframes prog{to{transform:scaleX(1)}}
/* header */
.nav{position:fixed;inset:0 0 auto 0;z-index:50;display:flex;align-items:center;justify-content:space-between;padding:18px var(--gut);color:var(--cream);background:linear-gradient(rgba(10,18,13,.55),transparent);backdrop-filter:blur(2px)}
.nav .logo{width:150px;display:block}.nav .logo img{width:100%}
.nav ul{display:flex;gap:clamp(16px,2.6vw,38px);list-style:none;padding:0;align-items:center}
.nav a{text-decoration:none;font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;position:relative;padding:6px 0}
.nav ul a:not(.btn)::after{content:"";position:absolute;left:0;bottom:0;height:1px;width:100%;background:currentColor;transform:scaleX(0);transform-origin:left;transition:transform .4s}
.nav ul a:hover::after,.nav a[aria-current]::after{transform:scaleX(1)}
.btn{display:inline-block;border:1px solid currentColor;padding:14px 26px!important;letter-spacing:.2em;font-size:.72rem;text-transform:uppercase;text-decoration:none;transition:.4s;background:transparent;color:inherit;cursor:pointer;font-family:var(--sans)}
.btn:hover{background:var(--cream);color:var(--forest)}
.btn.solid{background:var(--timber);border-color:var(--timber);color:#fff}.btn.solid:hover{background:var(--cream);color:var(--forest);border-color:var(--cream)}
.light .btn:hover,.lime .btn:hover{background:var(--forest);color:var(--cream)}
#menu,.burger{display:none}
@media(max-width:860px){
 .nav{z-index:70;backdrop-filter:none}
 .burger{display:block;font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;cursor:pointer;padding:8px}
 #menu:focus-visible+.burger{outline:2px solid var(--timber)}
 .nav ul{position:fixed;inset:0;z-index:1;width:100%;background:var(--forest);flex-direction:column;justify-content:flex-start;gap:28px;overflow-y:auto;overscroll-behavior:contain;padding:calc(104px + env(safe-area-inset-top)) var(--gut) calc(32px + env(safe-area-inset-bottom));transform:translateY(-100%);transition:transform .5s;visibility:hidden}
 .nav ul a{font-size:1.1rem}
 #menu:checked~ul{transform:none;visibility:visible}
 .nav .burger{position:relative;z-index:2}
 #menu{display:block;position:absolute;opacity:0;right:var(--gut);width:60px;height:30px}
}
/* hero */
.hero{position:relative;min-height:100svh;display:grid;align-items:end;color:var(--cream);overflow:hidden;background:var(--forest)}
.hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:62% 50%}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,18,13,.45),rgba(10,18,13,0) 35%,rgba(10,18,13,.75));pointer-events:none}
.hero .in{position:relative;z-index:2;padding:0 var(--gut) clamp(48px,8vw,96px);max-width:1200px}
.hero h1{max-width:12ch;margin-bottom:1.4rem}.hero .lead{margin-bottom:2rem}
.hero.small{min-height:62svh}.hero.small h1{font-size:clamp(2.4rem,6vw,5rem);max-width:18ch}
.scrollcue{position:absolute;right:var(--gut);bottom:40px;z-index:2;writing-mode:vertical-rl;font-size:.68rem;letter-spacing:.3em;text-transform:uppercase;color:var(--beige)}
.scrollcue::after{content:"";display:block;width:1px;height:60px;background:var(--beige);margin:14px auto 0;animation:cue 2.4s infinite}
@keyframes cue{0%{transform:scaleY(0);transform-origin:top}50%{transform:scaleY(1);transform-origin:top}51%{transform-origin:bottom}100%{transform:scaleY(0);transform-origin:bottom}}
@supports (animation-timeline:scroll()){
 .hero>img{animation:herozoom linear both;animation-timeline:scroll(root);animation-range:0 100vh}
 .hero .in{animation:herofade linear both;animation-timeline:scroll(root);animation-range:0 70vh}
}
@keyframes herozoom{to{transform:scale(1.22) translateY(6%);filter:brightness(.7)}}
@keyframes herofade{to{opacity:0;transform:translateY(-40px)}}
/* rotating statement */
.statement{position:relative;min-height:46vh;display:grid;place-items:center;text-align:center}
.statement p{grid-area:1/1;font-family:var(--serif);font-size:clamp(1.7rem,4.2vw,3.6rem);line-height:1.18;max-width:22ch;opacity:0;animation:rot 21s infinite}
.statement p:nth-child(2){animation-delay:7s}.statement p:nth-child(3){animation-delay:14s}
@keyframes rot{0%{opacity:0;transform:translateY(20px);filter:blur(6px)}5%,28%{opacity:1;transform:none;filter:none}33%,100%{opacity:0;transform:translateY(-20px);filter:blur(6px)}}
/* reveal */
@supports (animation-timeline:view()){
 .rv{animation:rv linear both;animation-timeline:view();animation-range:entry 0% cover 28%}
 @keyframes rv{from{opacity:0;transform:translateY(46px)}to{opacity:1;transform:none}}
 .imgreveal img{animation:imgr linear both;animation-timeline:view();animation-range:entry 0% cover 60%}
 @keyframes imgr{from{transform:scale(1.25)}to{transform:scale(1)}}
}
.imgreveal{overflow:hidden}
/* layout */
.split{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(32px,6vw,100px);align-items:center}
.split.rev>:first-child{order:2}
.split img{width:100%;aspect-ratio:4/3;object-fit:cover}
.split h2{margin-bottom:1.4rem}.split p+p{margin-top:1rem}
@media(max-width:860px){.split{grid-template-columns:minmax(0,1fr)}.split.rev>:first-child{order:0}}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:30px;margin-top:3rem;border-top:1px solid rgba(239,232,216,.25);padding-top:2rem}
.stats b{display:block;font-family:var(--serif);font-weight:400;font-size:2.6rem}.stats span{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--beige)}
/* Scroll-linked tower gallery */
.tower-track{height:240vh;position:relative;background:radial-gradient(ellipse at 50% 80%,#2f5a3f,var(--forest) 68%);color:var(--cream)}
.tower-sticky{position:sticky;top:0;height:100svh;display:grid;grid-template-rows:auto minmax(0,1fr) auto;padding:clamp(104px,14vh,136px) var(--gut) 28px}
.tower-heading{position:relative;z-index:1}
.tower-heading .eyebrow{color:var(--beige)}
.tower-heading h2{max-width:24ch;font-size:clamp(1.8rem,4vw,3.2rem)}
.tower-stage{position:relative;min-height:0;display:grid;place-items:center}
.tower-image{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:0;pointer-events:none}
.tower-caption{position:relative;z-index:1;color:var(--beige);font-size:.78rem;letter-spacing:.12em}
@media(max-width:700px){.tower-track{height:220vh}.tower-sticky{padding:104px var(--gut) 22px}.tower-heading h2{max-width:18ch}.tower-caption{font-size:.7rem}}
/* cards */
.rail{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:3rem}
@media(max-width:860px){.rail{grid-template-columns:minmax(0,1fr)}}
.card{background:#fff;color:var(--ink);text-decoration:none;display:flex;flex-direction:column;transition:transform .5s,box-shadow .5s;box-shadow:0 1px 0 rgba(0,0,0,.06)}
.card:hover{transform:translateY(-8px);box-shadow:0 30px 50px -28px rgba(0,0,0,.45)}
.card .imgreveal img{aspect-ratio:4/3;object-fit:cover;width:100%;transition:transform 1.2s}
.card:hover img{transform:scale(1.06)}
.card .b{padding:26px 26px 30px;display:flex;flex-direction:column;gap:.7rem;flex:1}
.card .meta{display:flex;gap:18px;flex-wrap:wrap;font-size:.72rem;letter-spacing:.18em;text-transform:uppercase;color:#6d6455}
.card .go{margin-top:auto;font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;color:var(--timber)}
.dark .card,.char .card{background:var(--forest2);color:var(--cream)}.dark .card .meta{color:var(--beige)}
/* filter (CSS only) */
.filters{display:flex;gap:10px;flex-wrap:wrap;margin:2rem 0 0}
.filters input{position:absolute;opacity:0;pointer-events:none}
.filters label{border:1px solid currentColor;padding:10px 20px;font-size:.72rem;letter-spacing:.2em;text-transform:uppercase;cursor:pointer;transition:.3s}
.filters input:checked+label{background:var(--forest);color:var(--cream)}
.filters input:focus-visible+label{outline:2px solid var(--timber);outline-offset:3px}
.fwrap:has(#f-g:checked) .card:not([data-t=g]),.fwrap:has(#f-t:checked) .card:not([data-t=t]),.fwrap:has(#f-s:checked) .card:not([data-t=s]){display:none}
/* amenities grid */
.grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1px;background:rgba(239,232,216,.2);margin-top:3rem}
.grid3>div{background:var(--forest);padding:38px 30px}.grid3 h3{margin-bottom:.6rem}.grid3 p{opacity:.78;font-size:.95rem}
.grid3 i{display:block;font-style:normal;font-family:var(--serif);font-size:2.2rem;color:var(--timber);margin-bottom:1rem}
/* swatch */
.swatches{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-top:2.5rem}
.sw{aspect-ratio:1;display:flex;align-items:flex-end;padding:14px;font-size:.7rem;letter-spacing:.2em;text-transform:uppercase}
/* marquee */
.marq{overflow:hidden;white-space:nowrap;padding:clamp(18px,3vw,28px) 0;background:var(--timber);color:#fff}
.marq div{display:inline-block;animation:mq 38s linear infinite;font-family:var(--serif);font-size:clamp(1.4rem,3vw,2.4rem);letter-spacing:.04em}
.marq span{margin:0 clamp(1rem,3vw,2.2rem)}
@keyframes mq{to{transform:translateX(-50%)}}
/* map */
.mapbox{position:relative;overflow:hidden}.mapbox img{width:100%;aspect-ratio:16/10;object-fit:cover}
.pin{position:absolute;background:var(--cream);color:var(--ink);padding:6px 12px;font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;box-shadow:0 8px 20px -8px rgba(0,0,0,.4)}
.pin.me{background:var(--forest);color:var(--cream)}
.list{list-style:none;padding:0;margin-top:2rem}
.list li{display:flex;justify-content:space-between;gap:20px;padding:16px 0;border-bottom:1px solid rgba(26,24,20,.18)}
.dark .list li{border-color:rgba(239,232,216,.22)}
.list li span:last-child{color:var(--timber);white-space:normal;overflow-wrap:anywhere;text-align:right}
.location-address{margin-top:1.5rem;color:var(--beige)}
/* gallery + lightbox (CSS only) */
.gal{columns:3 280px;column-gap:16px;margin-top:3rem}.gal a{display:block;margin-bottom:16px;overflow:hidden}.gal img{width:100%;transition:transform 1s}.gal a:hover img{transform:scale(1.05)}
.lb{position:fixed;inset:0;background:rgba(8,14,10,.94);display:none;place-items:center;z-index:90;padding:4vw}
.lb:target{display:grid}.lb img{max-height:84vh;width:auto;max-width:100%;object-fit:contain}
.lb .x{position:absolute;top:22px;right:28px;color:var(--cream);font-size:.75rem;letter-spacing:.25em;text-transform:uppercase;text-decoration:none}
/* form */
form{display:grid;gap:18px;max-width:640px;min-width:0}
label.f{display:grid;gap:6px;min-width:0;font-size:.72rem;letter-spacing:.2em;text-transform:uppercase}
input[type=text],input[type=email],input[type=tel],select,textarea{font:inherit;font-size:1rem;letter-spacing:0;text-transform:none;padding:14px;border:1px solid rgba(26,24,20,.35);background:#fff;color:var(--ink);width:100%;min-width:0}
textarea{min-height:130px}
.dark input,.dark select,.dark textarea{background:rgba(239,232,216,.08);color:var(--cream);border-color:rgba(239,232,216,.35)}
.crumb{font-size:.72rem;letter-spacing:.22em;text-transform:uppercase;margin-bottom:1.4rem;opacity:.8}
.specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:rgba(26,24,20,.18);margin:2.5rem 0}
.specs div{background:var(--cream);padding:22px}.specs b{display:block;font-family:var(--serif);font-weight:400;font-size:1.8rem}.specs span{font-size:.7rem;letter-spacing:.2em;text-transform:uppercase;color:#6d6455}
/* footer */
footer{background:var(--char);color:var(--cream);padding:clamp(60px,8vw,110px) var(--gut) 34px}
.fgrid{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr) minmax(0,1fr);gap:48px}
@media(max-width:860px){.fgrid{grid-template-columns:minmax(0,1fr)}}
footer h4{font-size:.72rem;letter-spacing:.26em;text-transform:uppercase;color:var(--beige);font-weight:500;margin-bottom:1rem}
footer ul{list-style:none;padding:0;display:grid;gap:8px;min-width:0}footer a{text-decoration:none;opacity:.85;overflow-wrap:anywhere}footer a:hover{opacity:1;text-decoration:underline}
.fine{margin-top:56px;padding-top:24px;border-top:1px solid rgba(239,232,216,.18);font-size:.78rem;opacity:.6}
.creator{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-top:1rem;font-size:.78rem;opacity:.8}
.creator p{margin:0}
.social-links{display:flex;gap:10px}
.social-links a{display:grid;place-items:center;width:38px;height:38px;border:1px solid rgba(239,232,216,.3);border-radius:50%;transition:background .3s}
.social-links a:hover{background:var(--forest2);text-decoration:none}
.social-links svg{width:18px;height:18px}
.big{font-family:var(--serif);font-size:clamp(2.6rem,9vw,8rem);line-height:.95;margin-bottom:1.2rem}
/* motion safety */
@media(prefers-reduced-motion:reduce){
 *,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}
 .statement{display:block;text-align:left;padding:0}.statement p{opacity:1;margin-bottom:1rem;max-width:none}
 .rv{opacity:1;transform:none}
}
@media print{.nav,.progress,.tower-track,.marq{display:none}}
"""

# ---------------------------------------------------------------- HTML helpers
def head(title, desc, fname):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — {B}</title><meta name="description" content="{desc}">
<meta name="theme-color" content="#14261d"><link rel="icon" href="images/aaranya-logo.svg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css"><script src="js/site.js" defer></script></head><body class="light">
<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"></div>
<header class="nav"><a class="logo" href="index.html" aria-label="{B} home"><img src="images/aaranya-logo.svg" alt="{B}" width="150" height="41"></a>
<nav aria-label="Primary"><input type="checkbox" id="menu" aria-label="Toggle menu"><label class="burger" for="menu">Menu</label><ul>
''' + "".join('<li><a href="{}.html"{}>{}</a></li>'.format(h, ' aria-current="page"' if h == fname else "", t) for h, t in NAV) + \
f'<li><a class="btn" href="visit.html#book">{CONFIG["cta"].split()[0]} visit</a></li></ul></nav></header><main id="main">'

def foot():
    links = "".join(f'<li><a href="{h}.html">{t}</a></li>' for h, t in PAGES)
    return f'''</main><footer><div class="fgrid"><div><img src="images/aaranya-logo.svg" alt="{B}" width="190" height="52">
<p style="margin-top:1.2rem;max-width:36ch;opacity:.8">Thoughtfully designed residences in Clifton, Karachi, with gardens, terraces and a calm connection to the outdoors.</p></div>
<div><h4>Explore</h4><ul>{links}</ul></div>
<div><h4>Contact</h4><ul><li>{CONFIG["address"]}</li><li><a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a></li><li><a href="tel:+922135874920">{CONFIG["phone"]}</a></li><li><a href="visit.html#book">{CONFIG["cta"]}</a></li></ul></div></div>
<p class="fine">© 2026 AlHafeez. All rights reserved.</p>
<div class="creator"><p>Made by <strong>Hafizullah Khokhar</strong> · <a href="mailto:hafizullahkhokhar1@gmail.com">hafizullahkhokhar1@gmail.com</a></p>
<div class="social-links" aria-label="Hafizullah Khokhar social profiles">
<a href="https://www.linkedin.com/in/hafizullahkhokhar1/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14ZM8.34 18V9.7H5.57V18h2.77ZM6.96 8.57a1.6 1.6 0 1 0 0-3.2 1.6 1.6 0 0 0 0 3.2ZM18.43 18v-4.55c0-2.44-1.3-3.58-3.03-3.58a2.62 2.62 0 0 0-2.36 1.3V9.7h-2.77V18h2.77v-4.1c0-1.08.2-2.12 1.54-2.12s1.35 1.23 1.35 2.2V18h2.5Z"/></svg></a>
<a href="https://www.instagram.com/hafizullahkhokhar1/" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="18" cy="6" r="1" fill="currentColor" stroke="none"/></svg></a>
<a href="https://www.facebook.com/hafizullahkhokhar1/" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M13.5 21v-8h2.7l.4-3h-3.1V8.1c0-.9.3-1.5 1.6-1.5h1.7V3.9c-.3 0-1.4-.1-2.6-.1-2.6 0-4.4 1.6-4.4 4.5V10H7v3h2.8v8h3.7Z"/></svg></a>
</div></div></footer></body></html>'''

def hero(img, eyebrow, h1, lead, small=False, cta=True):
    c = f'<a class="btn" href="visit.html#book">{CONFIG["cta"]}</a>' if cta else ""
    return f'''<section class="hero{" small" if small else ""}"><img src="images/{img}" alt="{h1}" fetchpriority="high">
<div class="in"><span class="eyebrow" style="color:var(--beige)">{eyebrow}</span><h1>{h1}</h1><p class="lead">{lead}</p>{c}</div>
{'' if small else '<span class="scrollcue">Scroll</span>'}</section>'''

def split(eyebrow, h2, ps, img, alt, rev=False, cls=""):
    return f'''<section class="wrap {cls}"><div class="split{" rev" if rev else ""}"><div class="rv"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2>{"".join(f"<p>{p}</p>" for p in ps)}</div>
<div class="imgreveal"><img src="images/{img}" alt="{alt}" loading="lazy" width="1200" height="800"></div></div></section>'''

def card(href, img, title, meta, t="", desc=""):
    d = f' data-t="{t}"' if t else ""
    return f'''<a class="card rv"{d} href="{href}"><div class="imgreveal"><img src="images/{img}" alt="{title}" loading="lazy" width="1200" height="800"></div><div class="b"><span class="eyebrow" style="margin:0">{meta[0]}</span><h3>{title}</h3><p>{desc}</p><div class="meta">{"".join(f"<span>{m}</span>" for m in meta[1:])}</div><span class="go">View residence →</span></div></a>'''

def cta_end(h="Come and see it for yourself."):
    return f'''<section class="wrap dark" style="text-align:center"><span class="eyebrow">Visit</span><p class="big">{h}</p><p class="lead" style="margin:0 auto 2rem">Open Tuesday to Sunday, 10:00 AM – 6:00 PM by appointment.</p><a class="btn solid" href="visit.html#book">{CONFIG["cta"]}</a></section>'''

def tower():
    return '''<section class="tower-track" data-tower-track aria-label="Walk around the building">
<div class="tower-sticky"><header class="tower-heading"><span class="eyebrow">Walk around the building</span><h2>Scroll to turn the tower.</h2></header>
<div class="tower-stage" role="img" aria-label="Three views of the AlHafeez tower: front, rear and side">
<img class="tower-image" src="images/aaranya-facade-front.webp" alt="" aria-hidden="true">
<img class="tower-image" src="images/aaranya-facade-back.webp" alt="" aria-hidden="true">
<img class="tower-image" src="images/aaranya-facade-side.webp" alt="" aria-hidden="true">
</div><p class="tower-caption">A closer look at the facade from every side.</p></div></section>'''

PAGE = {}

# ---------------------------------------------------------------- pages
def home():
    h = head("Home", "Thoughtfully designed residences in Clifton, Karachi.", "index")
    h += hero("aaranya-hero.jpeg", "Private residences", f"{CONFIG['tagline']}.", "Terraced homes framed by timber fins, planted balconies and palms, designed to connect daily life with the outdoors.")
    h += '''<section class="wrap lime"><div class="statement" aria-label="Architectural statements">
<p>Every terrace is a garden in the sky.</p><p>Timber, stone and shade — read as one façade.</p><p>Light moves through the building, all day.</p></div></section>'''
    h += split("Architecture", "A building that behaves like a landscape.",
               ["Stepped terraces, vertical timber fins and layered native planting soften the volume across every level. Deep overhangs filter afternoon sun while opening rooms to cross-breezes and garden views. Built to weather naturally, the facade shifts quietly from morning light to dusk.", "Open the architecture page for the full design language."],
               "aaranya-building-angle-01.jpeg", "Angle of the AlHafeez building with terraces and timber fins")
    h += tower()
    h += '''<section class="wrap"><span class="eyebrow">Residences</span><h2>Three ways to live here.</h2>
<div class="rail">''' + card("garden-residence.html", "aaranya-residence-garden.jpeg", "Garden Residence", ["Ground & podium", "185 M²", "2 beds"], desc="A private garden, deep shade and direct access to planting.") + \
        card("terrace-residence.html", "aaranya-residence-terrace.jpeg", "Terrace Residence", ["Mid levels", "240 M²", "3 beds"], desc="A planted terrace that extends the living space.") + \
        card("sky-penthouse.html", "aaranya-residence-penthouse.jpeg", "Sky Penthouse", ["Upper levels", "360 M²", "4 beds"], desc="Canopy-level living with long views.") + '</div></section>'
    h += '<div class="marq" aria-hidden="true"><div>' + "".join(f"<span>{w} ✦</span>" for w in ["Terraces", "Timber", "Palms", "Limestone", "Shade", "Light", "Stillness"] * 2) + "</div></div>"
    h += split("Amenities", "Slow mornings, shared quiet.", ["A calm courtyard pool, shaded garden paths, a wellness studio and an upper sky lounge overlooking the canopy."], "aaranya-amenity-pool.jpeg", "Courtyard pool framed by palms", True, "dark")
    h += split("Materials", "Honest, warm, weathered well.", ["Timber that silvers, limestone that glows, planting that grows into the building."], "Gemini_Generated_Image_p6qkd2p6qkd2p6qk.jpeg", "Timber fins, limestone and planted balconies")
    h += f'''<section class="wrap char"><div class="split"><div class="rv"><span class="eyebrow">Location</span><h2>Quiet, yet connected.</h2><p>Set on a quiet, tree-lined residential street within easy reach of local cafes, parks, daily markets and main roads.</p><p><a class="btn" href="location.html">View the map</a></p></div>
<div class="mapbox imgreveal"><img src="images/aaranya-location-map.jpg" alt="Illustrative neighborhood map" loading="lazy"><span class="pin me" style="left:46%;top:44%">AlHafeez</span></div></div></section>'''
    return h + cta_end() + foot()

def architecture():
    h = head("Architecture", "Design language, massing and façade.", "architecture")
    h += hero("aaranya-building-angle-01.jpeg", "Architecture", "Terraces, fins and a canopy of green.", "How the building meets light, climate and landscape.", True)
    h += split("Massing", "Stepped, shaded, open.", ["Stepped terraces, vertical timber fins and layered native planting soften the volume across every level. Deep overhangs filter afternoon sun while opening rooms to cross-breezes and garden views. Built to weather naturally, the facade shifts quietly from morning light to dusk."], "aaranya-building-angle-01.jpeg", "Massing of the building")
    h += tower()
    h += '''<section class="wrap dark"><span class="eyebrow">Design language</span><h2>Four ideas, one façade.</h2><div class="grid3">
<div><i>01</i><h3>Vertical fins</h3><p>Timber-look fins filter sun and frame views.</p></div>
<div><i>02</i><h3>Planted balconies</h3><p>Every home owns a layer of green.</p></div>
<div><i>03</i><h3>Stone plinth</h3><p>A grounded base in warm limestone.</p></div>
<div><i>04</i><h3>Quiet roofline</h3><p>A slim, shaded crown with shared terraces.</p></div></div></section>'''
    return h + cta_end() + foot()

def residences():
    h = head("Residences", "Garden, Terrace and Sky residences.", "residences")
    h += hero("aaranya-residence-terrace.jpeg", "Residences", "Homes that open outward.", "Discover homes shaped by garden, terrace and canopy living.", True)
    h += '''<section class="wrap"><div class="fwrap"><div class="filters" role="radiogroup" aria-label="Filter residences">
<input type="radio" name="f" id="f-a" checked><label for="f-a">All</label><input type="radio" name="f" id="f-g"><label for="f-g">Garden</label>
<input type="radio" name="f" id="f-t"><label for="f-t">Terrace</label><input type="radio" name="f" id="f-s"><label for="f-s">Sky</label></div><div class="rail">'''
    h += card("garden-residence.html", "aaranya-residence-garden.jpeg", "Garden Residence", ["Ground", "185 M²", "2 beds"], "g", "Private garden at your door.")
    h += card("terrace-residence.html", "aaranya-residence-terrace.jpeg", "Terrace Residence", ["Mid levels", "240 M²", "3 beds"], "t", "Terrace as an outdoor room.")
    h += card("sky-penthouse.html", "aaranya-residence-penthouse.jpeg", "Sky Penthouse", ["Upper levels", "360 M²", "4 beds"], "s", "Canopy-level living.")
    h += '</div></div></section>'
    return h + cta_end() + foot()

def residence(slug, name, img, blurb, level):
    sizes = {"garden-residence": ("185 M²", "2"), "terrace-residence": ("240 M²", "3"), "sky-penthouse": ("360 M²", "4")}
    area, bedrooms = sizes[slug]
    h = head(name, blurb, slug)
    h += hero(img, level, name, blurb, True)
    h += f'''<section class="wrap"><p class="crumb"><a href="residences.html">← All residences</a></p>
<div class="split"><div class="rv"><span class="eyebrow">Overview</span><h2>{name}</h2><p>{blurb}</p>
<div class="specs"><div><b>{area}</b><span>Interior</span></div><div><b>{bedrooms}</b><span>Bedrooms</span></div></div>
<p><a class="btn" href="visit.html#book">Enquire about this home</a></p></div><div class="imgreveal"><img src="images/{img}" alt="{name} interior" loading="lazy" width="1200" height="800"></div></div></section>'''
    h += split("Details", "Made for slow living.", ["Warm natural finishes and layered planting create a quiet, tactile home."], "Gemini_Generated_Image_p6qkd2p6qkd2p6qk.jpeg", "Timber fins, limestone and planted balconies", True, "lime")
    return h + cta_end() + foot()

def amenities():
    h = head("Amenities", "Pool court, sky lounge, gardens and more.", "amenities")
    h += hero("aaranya-amenity-pool.jpeg", "Amenities", "Shared spaces, shared calm.", "Quiet by design.", True)
    items = [("Pool court", "Sheltered water garden."), ("Sky lounge", "Shaded roof terrace."), ("Garden walk", "A planted loop between towers."),
             ("Wellness studio", "Light, ventilated, private."), ("Co-working nook", "A quiet table with a view."), ("Kids' lawn", "Safe, green, overlooked.")]
    h += '<section class="wrap dark"><span class="eyebrow">Lifestyle</span><h2>Everything within the canopy.</h2><div class="grid3">' + \
         "".join(f"<div><i>{i+1:02}</i><h3>{a}</h3><p>{b}</p></div>" for i, (a, b) in enumerate(items)) + "</div></section>"
    h += split("Pool court", "Water, palms, shade.", ["A sheltered courtyard pool sits among palms, shaded paths and quiet places to pause."], "aaranya-amenity-pool.jpeg", "Pool court with palms")
    return h + cta_end() + foot()

def materials_p():
    h = head("Materials", "Timber, limestone, charcoal and planting.", "materials")
    h += hero("Gemini_Generated_Image_p6qkd2p6qkd2p6qk.jpeg", "Materials", "A restrained palette.", "Timber, limestone and greenery bring warmth and texture to the facade.", True)
    sw = [("#1d3a2b", "Forest", "#efe8d8"), ("#26231f", "Charcoal", "#efe8d8"), ("#e6dcc5", "Limestone", "#1a1814"), ("#cdbfa3", "Beige", "#1a1814"), ("#a9753f", "Timber", "#fff")]
    h += '<section class="wrap"><span class="eyebrow">Palette</span><h2>Colour from the site.</h2><div class="swatches">' + \
         "".join(f'<div class="sw" style="background:{c};color:{t}">{n}</div>' for c, n, t in sw) + "</div></section>"
    h += split("Timber", "Warm, vertical, filtering.", ["Vertical timber fins add warmth, filter sunlight and frame views across the planted terraces."], "Gemini_Generated_Image_p6qkd2p6qkd2p6qk.jpeg", "Timber fins and planted terraces", True, "lime")
    return h + cta_end() + foot()

def sustainability():
    h = head("Sustainability", "Passive design and planting.", "sustainability")
    h += hero("aaranya-building-angle-01.jpeg", "Sustainability", "Designed to breathe.", "Shade, ventilation, planting.", True)
    items = [("Deep shade", "Overhangs cut solar gain."), ("Cross-ventilation", "Open plans, breezy corners."), ("Native planting", "Low-water, habitat-rich."), ("Rain harvesting", "Water for the gardens.")]
    h += '<section class="wrap dark"><span class="eyebrow">Principles</span><h2>Quietly responsible.</h2><div class="grid3">' + \
         "".join(f"<div><i>{i+1:02}</i><h3>{a}</h3><p>{b}</p></div>" for i, (a, b) in enumerate(items)) + "</div></section>"
    return h + cta_end() + foot()

def gallery():
    h = head("Gallery", "A closer look at AlHafeez residences and shared spaces.", "gallery")
    h += hero("aaranya-hero.jpeg", "Gallery", "A closer look.", "Explore the residences, gardens and shared spaces.", True)
    imgs = [("aaranya-hero.jpeg", "Building at dusk"), ("aaranya-building-angle-01.jpeg", "Building angle"), ("aaranya-residence-terrace.jpeg", "Terrace interior"),
            ("aaranya-residence-garden.jpeg", "Garden residence"), ("aaranya-residence-penthouse.jpeg", "Penthouse"), ("aaranya-amenity-pool.jpeg", "Pool court")]
    h += '<section class="wrap"><div class="gal">' + "".join(f'<a href="#g{i}"><img src="images/{f}" alt="{a}" loading="lazy"></a>' for i, (f, a) in enumerate(imgs)) + "</div>"
    h += "".join(f'<div class="lb" id="g{i}" role="dialog" aria-label="{a}"><a class="x" href="#">Close ✕</a><img src="images/{f}" alt="{a}"></div>' for i, (f, a) in enumerate(imgs)) + "</section>"
    return h + cta_end() + foot()

def location():
    h = head("Location", "Map and nearby destinations.", "location")
    h += hero("aaranya-location-map.jpg", "Location", "Close to everything that matters.", "A quiet address in Clifton Block 4, Karachi.", True)
    h += f'''<section class="wrap dark"><div class="split"><div class="mapbox imgreveal"><img src="images/aaranya-location-map.jpg" alt="Illustrative neighborhood map for Clifton Block 4">
<span class="pin me" style="left:50%;top:48%">AlHafeez</span></div>
<div class="rv"><span class="eyebrow">Nearby</span><h2>Within reach.</h2><p>Set on a quiet, tree-lined residential street within easy reach of local cafes, parks, daily markets and main roads.</p><p class="location-address">42 Canopy Grove, Clifton Block 4, Karachi</p></div></div></section>'''
    return h + cta_end() + foot()

def visit():
    h = head("Contact", "Book a private visit.", "visit")
    h += hero("aaranya-hero.jpeg", "Contact", "Book a private visit.", "We'll arrange a walkthrough at a time that suits you.", True, False)
    h += f'''<section class="wrap" id="book"><div class="split"><div class="rv"><span class="eyebrow">Enquire</span><h2>Let's talk.</h2><ul class="list"><li><span>Email</span><span><a href="mailto:{CONFIG["email"]}">{CONFIG["email"]}</a></span></li><li><span>Phone</span><span><a href="tel:+922135874920">{CONFIG["phone"]}</a></span></li><li><span>Address</span><span>{CONFIG["address"]}</span></li><li><span>Hours</span><span>Tuesday to Sunday, 10:00 AM – 6:00 PM by appointment.</span></li></ul></div>
<form data-mailto="{CONFIG["email"]}" action="mailto:{CONFIG["email"]}" method="post" enctype="text/plain"><label class="f">Full name<input type="text" name="name" required autocomplete="name"></label>
<label class="f">Email<input type="email" name="email" required autocomplete="email"></label><label class="f">Phone<input type="tel" name="phone" autocomplete="tel"></label>
<label class="f">Interested in<select name="type"><option>Garden Residence</option><option>Terrace Residence</option><option>Sky Penthouse</option></select></label>
<label class="f">Message<textarea name="message"></textarea></label><button class="btn solid" type="submit">{CONFIG["cta"]}</button></form></div></section>'''
    return h + foot()

# ---------------------------------------------------------------- build
if os.path.exists(OUT): shutil.rmtree(OUT)
write("css/style.css", CSS)
with open(os.path.join(os.path.dirname(__file__), "..", "js", "site.js"), encoding="utf-8") as source:
    write("js/site.js", source.read())
write("images/aaranya-logo.svg", logo())
write("images/aaranya-hero.jpeg", building(1600, 900, 1, 1.0))
write("images/aaranya-building-angle-01.jpeg", building(1600, 900, 5, 1.35, 1600 * .42, 7))
write("images/aaranya-residence-terrace.jpeg", interior(2, "#cdbfa3"))
write("images/aaranya-residence-garden.jpeg", interior(3, "#d8ceb8"))
write("images/aaranya-residence-penthouse.jpeg", interior(4, "#bfae8c"))
write("images/aaranya-amenity-pool.jpeg", pool())
write("images/Gemini_Generated_Image_p6qkd2p6qkd2p6qk.jpeg", materials())
write("images/aaranya-location-map.jpg", mapsvg())
write("images/README.txt", "Drop your own renders/photos here. Easiest: save your image with the same name but a new extension (e.g. aaranya-hero.webp), then in your code editor use Find and Replace across the project: aaranya-hero.jpeg -> aaranya-hero.webp.\nRecommended: hero 1920px wide, others 1200px wide, .webp or .jpg under 300 KB each.")
source_images = os.path.join(os.path.dirname(__file__), "..", "images")
for image_name in os.listdir(source_images):
    source_image = os.path.join(source_images, image_name)
    if os.path.isfile(source_image):
        shutil.copy2(source_image, os.path.join(OUT, "images", image_name))
pages = {"index": home(), "architecture": architecture(), "residences": residences(),
         "terrace-residence": residence("terrace-residence", "Terrace Residence", "aaranya-residence-terrace.jpeg", "A planted terrace as large as the living room.", "Mid levels"),
         "garden-residence": residence("garden-residence", "Garden Residence", "aaranya-residence-garden.jpeg", "A private garden at your door.", "Ground & podium"),
         "sky-penthouse": residence("sky-penthouse", "Sky Penthouse", "aaranya-residence-penthouse.jpeg", "Canopy-level living with long views.", "Upper levels"),
         "amenities": amenities(), "materials": materials_p(), "sustainability": sustainability(), "gallery": gallery(), "location": location(), "visit": visit()}
for k, v in pages.items(): write(f"{k}.html", v)
write("404.html", head("Not found", "Page not found", "") + '<section class="wrap dark" style="min-height:80vh;display:grid;align-content:center"><span class="eyebrow">404</span><h1>Lost in the canopy.</h1><p class="lead" style="margin:1rem 0 2rem">That page doesn\'t exist.</p><a class="btn" href="index.html">Back home</a></section>' + foot())
print("built", len(pages) + 1, "pages")
