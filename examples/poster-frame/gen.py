import random, math, pathlib
random.seed(5)
W, H = 1920, 1080
S = []
def add(s): S.append(s)
def rnd(a,b): return random.uniform(a,b)

# palette: five hexes, nothing else
INK   = "#08080f"
DEEP  = "#12102a"
PLUM  = "#2c1b3a"
EMBER = "#7a2b2f"
RED   = "#e8434b"
WARM  = "#ffcf8a"

add(f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">')

# --- sky: flat bands, poster style ---
add(f'<rect width="{W}" height="{H}" fill="{DEEP}"/>')
add(f'<rect y="430" width="{W}" height="330" fill="{PLUM}"/>')
add(f'<rect y="700" width="{W}" height="200" fill="{EMBER}"/>')
add(f'<rect y="880" width="{W}" height="200" fill="{INK}"/>')

# --- the moon: one flat disc, one thin ring ---
mx, my, mr = 640, 400, 300
add(f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="{RED}"/>')
add(f'<circle cx="{mx}" cy="{my}" r="{mr+22}" fill="none" stroke="{RED}" stroke-width="3" opacity=".35"/>')
add(f'<circle cx="{mx}" cy="{my}" r="{mr+60}" fill="none" stroke="{RED}" stroke-width="2" opacity=".16"/>')

# --- city: one flat silhouette, a few roof shapes ---
base = 880
pts = [f"M0,{base}"]
x = 0
while x < W:
    w = rnd(70, 170); h = rnd(40, 150)
    pts.append(f"L{x},{base-h:.0f} L{x+w:.0f},{base-h:.0f} L{x+w:.0f},{base}")
    x += w + rnd(0, 30)
pts.append(f"L{W},{base} L{W},{H} L0,{H} Z")
add(f'<path d="{" ".join(pts)}" fill="{INK}"/>')

# pagoda, one clean silhouette
# --- foreground rooftop: one diagonal ---
add(f'<path d="M0,{H} L0,790 L580,986 L1010,{H} Z" fill="#04040a"/>')
add(f'<path d="M0,790 L580,986" stroke="{RED}" stroke-width="3" opacity=".35" fill="none"/>')

# --- lantern string: one line, six dots ---
add(f'<path d="M60,120 Q460,330 900,250" stroke="{INK}" stroke-width="3" fill="none"/>')
for i in range(6):
    t = i/5
    bx = (1-t)**2*60 + 2*(1-t)*t*460 + t*t*900
    by = (1-t)**2*120 + 2*(1-t)*t*330 + t*t*250
    add(f'<line x1="{bx:.0f}" y1="{by:.0f}" x2="{bx:.0f}" y2="{by+18:.0f}" stroke="{INK}" stroke-width="2"/>')
    add(f'<circle cx="{bx:.0f}" cy="{by+34:.0f}" r="16" fill="{WARM}"/>')

# --- the figure: a clean silhouette on the roof edge ---
fx, fy = 300, 892
add(f'<g fill="{INK}">'
    f'<circle cx="{fx}" cy="{fy-186}" r="30"/>'
    f'<path d="M{fx-30},{fy-206} C{fx-20},{fy-232} {fx+22},{fy-230} {fx+30},{fy-202} '
    f'C{fx+12},{fy-214} {fx-14},{fy-214} {fx-30},{fy-206} Z"/>'
    f'<path d="M{fx-56},{fy} C{fx-54},{fy-104} {fx-26},{fy-152} {fx},{fy-156} '
    f'C{fx+26},{fy-152} {fx+54},{fy-104} {fx+56},{fy} Z"/>'
    f'<path d="M{fx-58},{fy-26} C{fx-78},{fy-72} {fx-76},{fy-116} {fx-56},{fy-140} '
    f'C{fx-52},{fy-96} {fx-46},{fy-56} {fx-38},{fy-22} Z"/>'
    '</g>')
# a single warm edge, because the moon is behind
add(f'<path d="M{fx+42},{fy-282} C{fx+54},{fy-244} {fx+52},{fy-212} {fx+42},{fy-188}" stroke="{RED}" stroke-width="5" fill="none" opacity=".85"/>')
add(f'<path d="M{fx+76},{fy-134} C{fx+82},{fy-84} {fx+80},{fy-40} {fx+78},{fy}" stroke="{RED}" stroke-width="5" fill="none" opacity=".5"/>')

# --- rain: uniform thin diagonals, flat ---
for i in range(90):
    rx, ry = rnd(0, W), rnd(0, H)
    ln = rnd(26, 60)
    add(f'<line x1="{rx:.0f}" y1="{ry:.0f}" x2="{rx-ln*.32:.0f}" y2="{ry+ln:.0f}" stroke="{RED}" stroke-width="2" opacity="{rnd(.05,.16):.2f}"/>')

# --- one accent: a lantern glow on the roof, flat ring, no blur ---
add(f'<circle cx="700" cy="980" r="26" fill="{WARM}" opacity=".18"/>')
add(f'<circle cx="700" cy="980" r="12" fill="{WARM}"/>')

add('</svg>')
svg = "".join(S)
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8" /><title>AnimeForge AI — poster frame, five colours</title>
<style>
 html,body{{margin:0;background:#05050a}}
 .frame{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
 .grain{{position:absolute;inset:0;pointer-events:none;opacity:.045;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/></filter><rect width='180' height='180' filter='url(%23n)'/></svg>")}}
 .vig{{position:absolute;inset:0;pointer-events:none;background:radial-gradient(125% 100% at 40% 45%, transparent 42%, rgba(3,3,8,.72) 100%)}}
</style></head>
<body><div class="frame">{svg}<div class="grain"></div><div class="vig"></div></div></body></html>'''
pathlib.Path("/scratch/work/poster/index.html").write_text(html)
print("nodes:", svg.count("<rect")+svg.count("<path")+svg.count("<circle")+svg.count("<line"))
