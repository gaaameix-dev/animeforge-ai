import random, math, pathlib

random.seed(23)
W, H = 1920, 1080
VPX, VPY = 960, 600          # vanishing point
S = []
NODES = [0]

def rnd(a, b): return random.uniform(a, b)
def add(s): S.append(s); NODES[0] += 1

add('''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#03060d"/><stop offset=".45" stop-color="#0a1526"/>
  <stop offset=".78" stop-color="#1c2b3d"/><stop offset="1" stop-color="#4a3524"/>
</linearGradient>
<radialGradient id="moonC" cx=".4" cy=".34" r=".72">
  <stop offset="0" stop-color="#ffffff"/><stop offset=".62" stop-color="#e4ecf6"/>
  <stop offset="1" stop-color="#a8bacd"/>
</radialGradient>
<radialGradient id="moonG" cx=".5" cy=".5" r=".5">
  <stop offset="0" stop-color="#cfe2ff" stop-opacity=".45"/>
  <stop offset=".45" stop-color="#9fb8dd" stop-opacity=".14"/>
  <stop offset="1" stop-color="#9fb8dd" stop-opacity="0"/>
</radialGradient>
<linearGradient id="street" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#241a1a"/><stop offset=".35" stop-color="#140f12"/>
  <stop offset="1" stop-color="#08070a"/>
</linearGradient>
<filter id="b3"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="b8"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="b20"><feGaussianBlur stdDeviation="20"/></filter>
<filter id="b40"><feGaussianBlur stdDeviation="40"/></filter>
</defs>''')

add(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')

# ---------- moon ----------
mx, my, mr = 1290, 150, 96
add(f'<circle cx="{mx}" cy="{my}" r="{mr*3.6}" fill="url(#moonG)"/>')
add(f'<circle cx="{mx}" cy="{my}" r="{mr}" fill="url(#moonC)"/>')
for _ in range(7):
    add(f'<ellipse cx="{mx+rnd(-mr*.7,mr*.7):.0f}" cy="{my+rnd(-mr*.7,mr*.7):.0f}" rx="{rnd(8,26):.0f}" '
        f'ry="{rnd(5,17):.0f}" fill="#a8b8ca" opacity="{rnd(.07,.16):.2f}" filter="url(#b3)"/>')

# ---------- clouds ----------
for _ in range(14):
    add(f'<ellipse cx="{rnd(0,W):.0f}" cy="{rnd(70,420):.0f}" rx="{rnd(180,420):.0f}" ry="{rnd(14,34):.0f}" '
        f'fill="#8ea6c2" opacity="{rnd(.03,.09):.2f}" filter="url(#b40)"/>')

# ---------- distant skyline behind the vanishing point ----------
x = 240
while x < 1700:
    bw, bh = rnd(40, 110), rnd(40, 170)
    add(f'<rect x="{x:.0f}" y="{VPY-bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="#0d1a26" opacity=".85"/>')
    for _ in range(int(bh//26)):
        if random.random() < .5:
            add(f'<rect x="{x+rnd(6,bw-10):.0f}" y="{VPY-bh+rnd(6,bh-10):.0f}" width="4" height="6" '
                f'fill="#ffc06a" opacity="{rnd(.2,.7):.2f}"/>')
    x += bw + rnd(4, 20)

# ---------- street geometry ----------
def ground(x):
    d = abs(x - VPX) / (W/2)
    return VPY + (H - VPY) * (d ** 1.35)

def height_at(x):
    d = abs(x - VPX) / (W/2)
    return 120 + 620 * (d ** 1.5)

add(f'<path d="M0,{H} L{VPX},{VPY} L{W},{H} Z" fill="url(#street)"/>')
add(f'<ellipse cx="{VPX}" cy="{VPY+60}" rx="150" ry="40" fill="#ff9a3c" opacity=".18" filter="url(#b20)"/>')
for _ in range(90):
    sx = rnd(VPX-760, VPX+760)
    sy = rnd(VPY+20, H)
    if abs(sx-VPX) > (sy-VPY)*1.05: continue
    add(f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{rnd(1,4):.1f}" height="{rnd(8,40):.0f}" fill="#ffc06a" opacity="{rnd(.03,.1):.2f}" filter="url(#b3)"/>')

# ---------- buildings along both sides ----------
def side(sign):
    x = VPX + sign*70
    while 0 < x < W if sign < 0 else x < W + 80:
        d = abs(x - VPX) / (W/2)
        bw = 40 + 210 * (d ** 1.25)
        hgt = height_at(x)
        x2 = x + sign*bw
        gy1, gy2 = ground(x), ground(x2)
        ty1, ty2 = gy1 - hgt, gy2 - hgt*rnd(.92, 1.04)
        body = random.choice(["#0b1420", "#0d1723", "#101a26", "#091019"])
        add(f'<path d="M{x:.0f},{gy1:.0f} L{x2:.0f},{gy2:.0f} L{x2:.0f},{ty2:.0f} L{x:.0f},{ty1:.0f} Z" fill="{body}"/>')

        # roof cap with a slight overhang, plus tile ticks
        add(f'<path d="M{x-8*sign:.0f},{ty1-6:.0f} L{x2+8*sign:.0f},{ty2-6:.0f} L{x2+8*sign:.0f},{ty2+4:.0f} L{x-8*sign:.0f},{ty1+4:.0f} Z" fill="#060b12"/>')

        # window grid on the facade
        cols = max(1, int(abs(bw) // 18))
        rows = max(1, int(hgt // 30))
        for c in range(cols):
            for r in range(rows):
                if random.random() > .72: continue
                fx = x + sign*(c + .5) * (bw / cols)
                fy = ty1 + (r + .5) * (hgt / rows)
                if fy > ground(fx) - 8: continue
                ww, wh = max(3, 11*(1 - d*.3)), max(4, 15*(1 - d*.25))
                col = "#ffc06a" if random.random() < .8 else "#a8dcff"
                op = rnd(.25,.95)
                # frame
                add(f'<rect x="{fx-ww/2-1:.0f}" y="{fy-wh/2-1:.0f}" width="{ww+2:.0f}" height="{wh+2:.0f}" '
                    f'fill="#05080e" opacity=".8"/>')
                add(f'<rect x="{fx-ww/2:.0f}" y="{fy-wh/2:.0f}" width="{ww:.0f}" height="{wh:.0f}" '
                    f'fill="{col}" opacity="{op:.2f}"/>')
                if random.random() < .18:   # a room you can see into
                    add(f'<rect x="{fx-ww/2:.0f}" y="{fy-wh/2:.0f}" width="{ww:.0f}" height="{wh*.45:.1f}" '
                        f'fill="#fff3d8" opacity=".9"/>')
                    add(f'<rect x="{fx-ww/2:.0f}" y="{fy+wh*.1:.0f}" width="{ww:.0f}" height="{wh*.4:.1f}" '
                        f'fill="#3a1f14" opacity=".55"/>')
                # reflection
                if random.random() < .5:
                    add(f'<rect x="{fx-ww/2:.0f}" y="{ground(fx)+6:.0f}" width="{ww*.8:.1f}" height="{wh*3:.1f}" '
                        f'fill="{col}" opacity="{rnd(.04,.12):.2f}" filter="url(#b8)"/>')
        # roof tiles: ticks along the eave
        ticks = max(2, int(abs(bw) // 12))
        for i in range(ticks):
            tx = x + sign*(i + .5)*(bw/ticks)
            ty = ty1 + (i + .5)*(ty2 - ty1)/ticks
            add(f'<path d="M{tx:.0f},{ty-7:.0f} L{tx:.0f},{ty+3:.0f}" stroke="#1a2430" stroke-width="1.4" opacity=".7"/>')

        # lanterns hanging off the eave, spaced by depth
        nl = max(1, int(abs(bw) // 34))
        for i in range(nl):
            lx = x + sign*(i + .5)*(bw/nl)
            ly = ground(lx) - 26 - 12*(1 - d)
            r = 5 + 9*(1 - d)
            add(f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="{r*3:.1f}" fill="#ff9a3c" opacity=".18" filter="url(#b8)"/>')
            add(f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="{r:.1f}" fill="#ffcf8a"/>')
            add(f'<circle cx="{lx:.0f}" cy="{ly:.0f}" r="{r*.4:.1f}" fill="#fff6e2"/>')
            # reflection on the wet street
            add(f'<rect x="{lx-r*.8:.0f}" y="{ground(lx)+4:.0f}" width="{r*1.6:.1f}" height="{r*6:.1f}" '
                f'fill="#ff9a3c" opacity=".12" filter="url(#b8)"/>')
        x = x2 + sign*rnd(2, 10)

def stalls(sign):
    for i in range(26):
        d = rnd(.05, .95)
        x = VPX + sign * (60 + 1500 * d**1.6)
        if not (0 < x < W): continue
        g = ground(x)
        w = 16 + 52*d; h = 10 + 26*d
        col = random.choice(["#ff9a3c", "#ffcf8a", "#ff7043"])
        # awning, then the lit counter under it
        add(f'<path d="M{x-w/2-5:.0f},{g-h-4:.0f} L{x+w/2+5:.0f},{g-h-4:.0f} L{x+w/2:.0f},{g-h+2:.0f} L{x-w/2:.0f},{g-h+2:.0f} Z" fill="#080a10"/>')
        add(f'<rect x="{x-w/2:.0f}" y="{g-h+2:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#0a0d12"/>')
        add(f'<rect x="{x-w/2+2:.0f}" y="{g-h+4:.0f}" width="{w-4:.0f}" height="{h-3:.0f}" fill="{col}" opacity="{rnd(.25,.55):.2f}"/>')
        add(f'<ellipse cx="{x:.0f}" cy="{g+2:.0f}" rx="{w*.7:.0f}" ry="{h*.7:.0f}" fill="{col}" opacity=".1" filter="url(#b8)"/>')

side(-1)
side(1)
stalls(-1)
stalls(1)

# strings of lanterns crossing the alley overhead
def cross_string(y0, y1, sag, n, r):
    add(f'<path d="M0,{y0} Q{VPX},{y0+sag} {W},{y1}" stroke="#0b0e14" stroke-width="2" fill="none"/>')
    for i in range(n):
        u = i/(n-1)
        bx = (1-u)**2*0 + 2*(1-u)*u*VPX + u*u*W
        by = (1-u)**2*y0 + 2*(1-u)*u*(y0+sag) + u*u*y1
        add(f'<circle cx="{bx:.0f}" cy="{by+14:.0f}" r="{r*2.8:.1f}" fill="#ff9a3c" opacity=".16" filter="url(#b8)"/>')
        add(f'<circle cx="{bx:.0f}" cy="{by+14:.0f}" r="{r:.1f}" fill="#ffcf8a"/>')
        add(f'<circle cx="{bx:.0f}" cy="{by+14:.0f}" r="{r*.4:.1f}" fill="#fff6e2"/>')

cross_string(300, 300, 60, 16, 6)
cross_string(430, 430, 44, 14, 5)

# ---------- neon signs on the near facades ----------
def neon(x, y, w, h, col):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" opacity=".22" filter="url(#b20)"/>')
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{col}" opacity=".75"/>')
    add(f'<rect x="{x+4}" y="{y+4}" width="{w-8}" height="{h-8}" fill="#0a0d14" opacity=".55"/>')
    for i in range(int(h//26)):
        add(f'<rect x="{x+w*.28}" y="{y+10+i*24}" width="{w*.44}" height="10" fill="{col}" opacity=".9"/>')

neon(300, 470, 54, 210, "#ff4d6d")
neon(560, 560, 40, 150, "#7bffb0")
neon(1400, 520, 46, 180, "#59d0ff")

# ---------- foreground: eave and lanterns close to camera ----------
add(f'<path d="M0,0 L620,0 L520,120 L380,180 L150,210 L0,215 Z" fill="#05070b"/>')
add(f'<path d="M0,215 L150,210 L380,180 L520,120 L560,150 L400,230 L160,268 L0,272 Z" fill="#080b12"/>')
for i in range(5):
    lx = 60 + i*110
    ly = 250 + i*10
    r = 22 - i*2
    add(f'<circle cx="{lx}" cy="{ly}" r="{r*2.6}" fill="#ff9a3c" opacity=".2" filter="url(#b20)"/>')
    add(f'<circle cx="{lx}" cy="{ly}" r="{r}" fill="#ffcf8a"/>')
    add(f'<circle cx="{lx}" cy="{ly}" r="{r*.42}" fill="#fff8e8"/>')

# ---------- the figure, from behind ----------
fx, fy = 700, 1010
add('<g fill="#05070b">'
    # head and hair
    f'<circle cx="{fx}" cy="{fy-306}" r="44"/>'
    f'<path d="M{fx-46},{fy-320} C{fx-40},{fy-360} {fx+40},{fy-360} {fx+46},{fy-318} '
    f'C{fx+30},{fy-344} {fx-30},{fy-344} {fx-46},{fy-320} Z"/>'
    # shoulders and coat
    f'<path d="M{fx-104},{fy} C{fx-98},{fy-196} {fx-56},{fy-268} {fx},{fy-272} '
    f'C{fx+56},{fy-268} {fx+98},{fy-196} {fx+104},{fy} Z"/>'
    # collar
    f'<path d="M{fx-52},{fy-268} C{fx-30},{fy-244} {fx+30},{fy-244} {fx+52},{fy-268} '
    f'C{fx+34},{fy-232} {fx-34},{fy-232} {fx-52},{fy-268} Z"/>'
    '</g>')
# rim on the shoulder and the head, from the moon behind
add(f'<path d="M{fx+44},{fy-336} C{fx+52},{fy-300} {fx+50},{fy-268} {fx+42},{fy-244}" stroke="#9fb8dd" stroke-width="3" fill="none" opacity=".35"/>')
add(f'<path d="M{fx+96},{fy-186} C{fx+104},{fy-120} {fx+106},{fy-60} {fx+104},{fy}" stroke="#9fb8dd" stroke-width="3" fill="none" opacity=".28"/>')

# ---------- fireworks and smoke ----------
def firework(cx, cy, n, rad, color, seed):
    r = random.Random(seed)
    add(f'<circle cx="{cx}" cy="{cy}" r="{rad*1.4}" fill="{color}" opacity=".1" filter="url(#b40)"/>')
    for i in range(n):
        a = rnd(0, math.tau); l = rnd(rad*.25, rad)
        px, py = cx + math.cos(a)*l, cy + math.sin(a)*l
        rr = rnd(1.4, 3.6)
        add(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rr:.1f}" fill="{color}" opacity="{rnd(.2,.8):.2f}"/>')
        if random.random() < .4:
            add(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rr*3:.1f}" fill="{color}" opacity=".09" filter="url(#b3)"/>')

firework(1180, 260, 120, 130, "#bfe4ff", 4)
firework(820, 190, 90, 90, "#ffd9a8", 14)
firework(1500, 380, 70, 80, "#ffb0c8", 31)

for _ in range(10):
    add(f'<ellipse cx="{rnd(600,1600):.0f}" cy="{rnd(150,520):.0f}" rx="{rnd(50,160):.0f}" ry="{rnd(20,60):.0f}" '
        f'fill="#dfe8f5" opacity="{rnd(.02,.06):.2f}" filter="url(#b40)"/>')

# ---------- atmosphere ----------
add(f'<rect x="0" y="440" width="{W}" height="220" fill="#ff9a3c" opacity=".07" filter="url(#b40)"/>')
add(f'<rect x="0" y="560" width="{W}" height="260" fill="#2a4a5e" opacity=".08" filter="url(#b40)"/>')

svg = f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">' + "".join(S) + '</svg>'
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8" /><title>AnimeForge AI — the street, generated</title>
<style>
 html,body{{margin:0;background:#03050a}}
 .frame{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}
 .grain{{position:absolute;inset:0;pointer-events:none;opacity:.05;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='180' height='180'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/></filter><rect width='180' height='180' filter='url(%23n)'/></svg>")}}
 .vig{{position:absolute;inset:0;pointer-events:none;background:radial-gradient(120% 95% at 50% 45%, transparent 36%, rgba(2,4,8,.82) 100%)}}
</style></head>
<body><div class="frame">{svg}<div class="grain"></div><div class="vig"></div></div></body></html>'''
pathlib.Path("/scratch/work/street/index.html").write_text(html)
print("nodes:", NODES[0], "| kb:", len(html)//1024)
