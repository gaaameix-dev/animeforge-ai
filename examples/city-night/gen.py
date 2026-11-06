import random, math, pathlib

random.seed(11)
W, H = 1920, 1080
S = []

def rnd(a, b): return random.uniform(a, b)

S.append('''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#04070e"/><stop offset=".4" stop-color="#0a1322"/>
  <stop offset=".68" stop-color="#16283a"/><stop offset=".86" stop-color="#4a3a26"/>
  <stop offset="1" stop-color="#8a5a2a"/>
</linearGradient>
<radialGradient id="moonC" cx=".42" cy=".36" r=".7">
  <stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#e6edf7"/>
  <stop offset="1" stop-color="#aebfd2"/>
</radialGradient>
<radialGradient id="moonG" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#d6e6ff" stop-opacity=".5"/>
  <stop offset=".45" stop-color="#9fb8dd" stop-opacity=".16"/>
  <stop offset="1" stop-color="#9fb8dd" stop-opacity="0"/>
</radialGradient>
<linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#1a1a24"/><stop offset=".5" stop-color="#12121a"/>
  <stop offset="1" stop-color="#0a0a10"/>
</linearGradient>
<linearGradient id="haze" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#ff9a3c" stop-opacity="0"/>
  <stop offset=".55" stop-color="#ff9a3c" stop-opacity=".16"/>
  <stop offset="1" stop-color="#ff9a3c" stop-opacity="0"/>
</linearGradient>
<filter id="b4"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="b10"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="b26"><feGaussianBlur stdDeviation="26"/></filter>
</defs>''')

S.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')

# ---------------- moon ----------------
mx, my, mr = 1180, 190, 118
S.append(f'<circle cx="{mx}" cy="{my}" r="{mr*3.4}" fill="url(#moonG)"/>')
S.append(f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="url(#moonC)"/>')
for _ in range(8):
    S.append(f'<ellipse cx="{mx+rnd(-mr*.72,mr*.72):.0f}" cy="{my+rnd(-mr*.72,mr*.72):.0f}" '
             f'rx="{rnd(10,34):.0f}" ry="{rnd(7,22):.0f}" fill="#a8b8ca" opacity="{rnd(.07,.18):.2f}" filter="url(#b4)"/>')

# ---------------- clouds ----------------
for _ in range(12):
    S.append(f'<ellipse cx="{rnd(0,W):.0f}" cy="{rnd(90,430):.0f}" rx="{rnd(200,460):.0f}" '
             f'ry="{rnd(16,40):.0f}" fill="#8ea6c2" opacity="{rnd(.04,.1):.2f}" filter="url(#b26)"/>')

# ---------------- hills ----------------
for base, amp, col in ((600, 70, "#0b1822"), (680, 46, "#080f16")):
    pts = [f"M0,{H}"]
    x = 0
    while x <= W:
        pts.append(f"L{x},{base - amp*math.sin(x/600) - rnd(0, amp*.6):.0f}")
        x += 80
    pts.append(f"L{W},{H} Z")
    S.append(f'<path d="{" ".join(pts)}" fill="{col}"/>')

# ---------------- city, three planes ----------------
def city(base_y, hmin, hmax, wmin, wmax, body, density, op, blur=None, wsize=(6,9), warm=.8, gap=(3,14)):
    g = [f'<g opacity="{op}"' + (f' filter="url(#{blur})"' if blur else '') + '>']
    x = -80
    while x < W + 80:
        bw, bh = rnd(wmin, wmax), rnd(hmin, hmax)
        top = base_y - bh
        g.append(f'<rect x="{x:.0f}" y="{top:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="{body}"/>')
        if random.random() < .5:
            g.append(f'<rect x="{x-5:.0f}" y="{top-8:.0f}" width="{bw+10:.0f}" height="10" fill="{body}"/>')
        cw, ch = wsize
        cols, rows = int(bw // (cw+7)), int(bh // (ch+11))
        for c in range(cols):
            for r in range(rows):
                if random.random() > density: continue
                col = "#ffc06a" if random.random() < warm else "#a8dcff"
                g.append(f'<rect x="{x+6+c*(cw+7):.0f}" y="{top+10+r*(ch+11):.0f}" width="{cw}" height="{ch}" '
                         f'fill="{col}" opacity="{rnd(.3,1):.2f}"/>')
        x += bw + rnd(*gap)
    g.append('</g>')
    S.append("".join(g))

city(800, 110, 280, 55, 120, "#132430", .16, .5, blur="b10", wsize=(5,7), warm=.45)
city(880, 150, 360, 75, 160, "#0c1a26", .2, .78, blur="b4", wsize=(6,8), warm=.6)
city(980, 200, 480, 95, 210, "#070d14", .24, 1, wsize=(7,9), warm=.85)

# ---------------- horizon glow ----------------
S.append(f'<rect x="0" y="560" width="{W}" height="420" fill="url(#haze)"/>')

# ---------------- water plane with reflections ----------------
waterY = 880
S.append(f'<rect x="0" y="{waterY}" width="{W}" height="{H-waterY}" fill="url(#water)"/>')
S.append(f'<rect x="0" y="{waterY-4}" width="{W}" height="8" fill="#ff9a3c" opacity=".18" filter="url(#b4)"/>')
for _ in range(220):
    x = rnd(0, W)
    col = "#ffc06a" if random.random() < .82 else "#a8dcff"
    w = rnd(2, 7); h = rnd(10, 90)
    S.append(f'<rect x="{x:.0f}" y="{rnd(waterY+4, H-30):.0f}" width="{w:.0f}" height="{h:.0f}" '
             f'fill="{col}" opacity="{rnd(.05,.22):.2f}" filter="url(#b4)"/>')
for _ in range(26):
    y = rnd(waterY+10, H)
    S.append(f'<path d="M{rnd(0,W*.5):.0f},{y:.0f} q 60,{rnd(-3,3):.1f} 120,0" stroke="#9fb8dd" '
             f'stroke-width="{rnd(.6,1.6):.1f}" fill="none" opacity="{rnd(.04,.12):.2f}"/>')

# ---------------- pagoda roofs framing the top corners ----------------
def roof(cx, cy, w, h, color):
    S.append(f'<path d="M{cx-w},{cy} Q{cx-w*.6},{cy-h*.55} {cx},{cy-h*.62} Q{cx+w*.6},{cy-h*.55} {cx+w},{cy} '
             f'L{cx+w*.9},{cy+h*.2} Q{cx},{cy-h*.08} {cx-w*.9},{cy+h*.2} Z" fill="{color}"/>')
    S.append(f'<rect x="{cx-10}" y="{cy-h*.7}" width="20" height="{h*.12}" fill="{color}"/>')

roof(-40, 300, 300, 150, "#05080c")
roof(-90, 470, 330, 150, "#05080c")
roof(1960, 340, 300, 150, "#05080c")

# ---------------- lantern strings off the eaves ----------------
def lanterns(x0, y0, x1, y1, sag, n, r=9):
    S.append(f'<path d="M{x0},{y0} Q{(x0+x1)/2},{(y0+y1)/2+sag} {x1},{y1}" stroke="#101014" stroke-width="2" fill="none"/>')
    for i in range(n):
        t = i/(n-1)
        bx = (1-t)**2*x0 + 2*(1-t)*t*((x0+x1)/2) + t*t*x1
        by = (1-t)**2*y0 + 2*(1-t)*t*((y0+y1)/2+sag) + t*t*y1
        S.append(f'<circle cx="{bx:.0f}" cy="{by+18:.0f}" r="{r*3}" fill="#ff9a3c" opacity=".2" filter="url(#b10)"/>')
        S.append(f'<circle cx="{bx:.0f}" cy="{by+18:.0f}" r="{r}" fill="#ffcf8a"/>')
        S.append(f'<circle cx="{bx:.0f}" cy="{by+18:.0f}" r="{r*.42}" fill="#fff6e2"/>')

lanterns(120, 420, 520, 560, 60, 9, 10)
lanterns(1400, 560, 1800, 420, 60, 9, 10)

# ---------------- fireworks ----------------
def firework(cx, cy, n, rad, color, seed):
    r = random.Random(seed)
    S.append(f'<circle cx="{cx}" cy="{cy}" r="{rad*1.3}" fill="{color}" opacity=".1" filter="url(#b26)"/>')
    S.append(f'<circle cx="{cx}" cy="{cy}" r="{rad*.55}" fill="{color}" opacity=".18" filter="url(#b26)"/>')
    for i in range(n):
        a = rnd(0, math.tau); l = rnd(rad*.25, rad)
        px, py = cx + math.cos(a)*l, cy + math.sin(a)*l
        r = rnd(1.6, 4.2)
        S.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r:.1f}" fill="{color}" opacity="{rnd(.25,.85):.2f}"/>')
        S.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{r*3:.1f}" fill="{color}" opacity=".1" filter="url(#b4)"/>')

firework(380, 250, 90, 130, "#bfe4ff", 5)
firework(1560, 220, 80, 105, "#ffd9a8", 8)
firework(1620, 430, 60, 70, "#ffb0c8", 21)

# ---------------- foreground: a figure on the railing ----------------
fx, fy = 1560, 900
S.append('<g fill="#04060a">'
         f'<circle cx="{fx}" cy="{fy-150}" r="24"/>'
         f'<circle cx="{fx+14}" cy="{fy-172}" r="12"/>'
         f'<path d="M{fx-40},{fy} C{fx-38},{fy-88} {fx-18},{fy-124} {fx},{fy-126} '
         f'C{fx+20},{fy-124} {fx+40},{fy-88} {fx+42},{fy} Z"/>'
         f'<path d="M{fx-42},{fy-20} C{fx-58},{fy-46} {fx-56},{fy-70} {fx-44},{fy-84} '
         f'C{fx-40},{fy-56} {fx-38},{fy-34} {fx-30},{fy-18} Z"/>'
         f'</g>')
S.append(f'<path d="M{fx-150},{fy-6} L{fx+150},{fy-6}" stroke="#04060a" stroke-width="9" stroke-linecap="round"/>')

svg = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">' + "".join(S) + '</svg>'

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8" /><title>AnimeForge AI — city at night, drawn by a generator</title>
<style>
 html,body{{margin:0;background:#04060a}}
 .frame{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
 .grain{{position:absolute;inset:0;pointer-events:none;opacity:.05;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/></filter><rect width='180' height='180' filter='url(%23n)'/></svg>")}}
 .vig{{position:absolute;inset:0;pointer-events:none;background:radial-gradient(120% 95% at 50% 42%, transparent 38%, rgba(2,4,8,.8) 100%)}}
</style></head>
<body><div class="frame">{svg}<div class="grain"></div><div class="vig"></div></div></body></html>'''

pathlib.Path("/scratch/work/city/index.html").write_text(html)
print("nodes:", html.count("<rect")+html.count("<path")+html.count("<circle")+html.count("<line"))
