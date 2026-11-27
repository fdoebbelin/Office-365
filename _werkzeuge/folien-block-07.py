# Folien Block 07 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-07.py assets/folien/block-07
# Vorschau: magick -density 72 assets/folien/block-07/01-themen.svg vorschau.png
import sys, html
OUT = sys.argv[1]
W, H = 1280, 720
FONT = "Segoe UI, Aptos, Arial, Helvetica, sans-serif"
NAVY = "#1F3A5F"; INK = "#1E2430"; MUTED = "#5B6472"; LINE = "#D5DAE1"
OUTLOOK = "#0F6CBD"; WORD = "#185ABD"; EXCEL = "#107C41"; ACCENT = "#E8A33D"; BAD = "#B3261E"
SOFTBLUE = "#E6F0FA"; SOFTGREEN = "#E7F4EC"; SOFTRED = "#FBE9E7"; SOFTYELLOW = "#FFF4D6"; GREY = "#F3F5F8"

def esc(s): return html.escape(s, quote=True)
def text(x, y, s, size=28, weight="normal", fill=INK, anchor="start", italic=False, rotate=None):
    st = ' font-style="italic"' if italic else ''
    tr = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ''
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{st}{tr}>{esc(s)}</text>'
def rect(x, y, w, h, fill="#fff", stroke="none", rx=12, sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def bar(x, y, w, col=LINE, sw=6):
    return f'<line x1="{x}" y1="{y}" x2="{x+w}" y2="{y}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'
def pill(x, y, s, col, size=22, anchor="start"):
    w = len(s) * size * 0.58 + 28
    x0 = x - w / 2 if anchor == "middle" else x
    return rect(x0, y - size - 6, w, size + 18, col, rx=(size + 18) / 2) + text(x0 + w / 2, y + 2, s, size, "bold", "#FFFFFF", "middle")
def frame(nr, title, body, desc):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>
<defs><marker id="pf" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{ACCENT}"/></marker></defs>
{rect(0,0,W,H,"#FFFFFF",rx=0)}
{rect(0,0,W,110,NAVY,rx=0)}
{text(60,72,title,44,"bold","#FFFFFF")}
{body}
<line x1="60" y1="660" x2="{W-60}" y2="660" stroke="{LINE}" stroke-width="2"/>
{text(60,694,"Block 07 · Selbsttest Outlook und Word",20,fill=MUTED)}
{text(W-60,694,"Haus Lichtblick – Microsoft 365  ·  Folie "+str(nr),20,fill=MUTED,anchor="end")}
</svg>
'''

slides = []
SOFTX = "#E7F4EC"
def grid(x, y, cols, rows, cw, rh, data=None, sel=None, headfill="#F3F5F8", colw=None, bold_row=None, aligns=None, size=17, rowlabels=None):
    """Excel-Raster mit Spalten- und Zeilenköpfen. data: dict (r,c)->text (r,c ab 1)."""
    colw = colw or [cw] * cols
    s = rect(x, y, 40, rh, headfill, LINE, 0, 1)
    cx = x + 40
    for c in range(cols):
        s += rect(cx, y, colw[c], rh, headfill, LINE, 0, 1) + text(cx + colw[c] / 2, y + rh * 0.68, chr(65 + c), 15, fill=MUTED, anchor="middle")
        cx += colw[c]
    for r in range(1, rows + 1):
        yy = y + r * rh
        s += rect(x, yy, 40, rh, headfill, LINE, 0, 1) + text(x + 20, yy + rh * 0.68, str(rowlabels[r - 1] if rowlabels else r), 15, fill=OUTLOOK if rowlabels else MUTED, anchor="middle")
        cx = x + 40
        for c in range(cols):
            s += rect(cx, yy, colw[c], rh, "#FFFFFF", LINE, 0, 1)
            t = (data or {}).get((r, c + 1))
            if t is not None:
                a = (aligns or {}).get(c + 1, "start")
                tx = cx + 8 if a == "start" else cx + colw[c] - 8
                s += text(tx, yy + rh * 0.68, t, size, "bold" if r == bold_row else "normal", INK, a)
            cx += colw[c]
    if sel:
        r, c = sel
        sx = x + 40 + sum(colw[:c - 1]); sy = y + r * rh
        s += rect(sx, sy, colw[c - 1], rh, "none", EXCEL, 0, 3) + rect(sx + colw[c - 1] - 4, sy + rh - 4, 8, 8, EXCEL, "#FFFFFF", 0, 1)
    return s

MON = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]
VAL = [4850, 4670, 4530, 4240, 3890, 3540, 3320, 3240, 3360, 3650, 4030, 4530]
def columns(x, y, w, h, title=None, ytitle=None, xtitle=None, labels=True, col=EXCEL, hi=None):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 8, 1.5)
    px, py, pw, ph = x + (70 if ytitle else 50), y + (50 if title else 20), w - (100 if ytitle else 70), h - (110 if xtitle else 80) - (30 if title else 0)
    if title: s += text(x + w / 2, y + 34, title, 20, "bold", INK, "middle")
    vmax = 5000
    for k in range(6):
        yy = py + ph - ph * k / 5
        s += f'<line x1="{px}" y1="{yy}" x2="{px+pw}" y2="{yy}" stroke="{LINE}" stroke-width="1"/>'
        if labels: s += text(px - 8, yy + 5, f"{k*1000:,}".replace(",", "."), 12, fill=MUTED, anchor="end")
    bw = pw / 12
    for i, v in enumerate(VAL):
        bh = ph * v / vmax
        c = (BAD if hi and i in hi else col)
        s += rect(px + i * bw + bw * 0.18, py + ph - bh, bw * 0.64, bh, c, rx=2)
        if labels: s += text(px + i * bw + bw / 2, py + ph + 18, MON[i], 12, fill=MUTED, anchor="middle")
    if ytitle: s += text(x + 22, py + ph / 2, ytitle, 14, "bold", MUTED, "middle", rotate=-90)
    if xtitle: s += text(px + pw / 2, py + ph + 44, xtitle, 14, "bold", MUTED, "middle")
    return s

def appcard(x, y, w, h, col, name, lines):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 14, 2)
    s += f'<path d="M{x} {y+14} a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v56 h-{w} z" fill="{col}"/>'
    s += text(x + w / 2, y + 46, name, 28, "bold", "#FFFFFF", "middle")
    for i, l in enumerate(lines):
        s += text(x + w / 2, y + 120 + i * 34, l, 21 if i else 24, "normal" if i else "bold", MUTED if i else INK, "middle")
    return s

def checkrow(x, y, t, col, size=19):
    return rect(x, y - 18, 22, 22, col, rx=4) + f'<path d="M{x+5} {y-7} l5 5 l8 -10" stroke="#FFFFFF" stroke-width="2.5" fill="none"/>' + text(x + 34, y, t, size, fill=INK)
def key(x, y, t, w=None):
    w = w or len(t) * 14 + 30
    return rect(x, y, w, 52, "#FFFFFF", MUTED, 8, 2) + f'<line x1="{x+4}" y1="{y+48}" x2="{x+w-4}" y2="{y+48}" stroke="{LINE}" stroke-width="4"/>' + text(x + w / 2, y + 34, t, 22, "bold", INK, "middle"), w

# 1 Themen
b = ""
groups = [(OUTLOOK, "Outlook – E-Mail", "Block 02", ["Oberfläche und Ordner", "An, Cc, Bcc", "Betreff: Was? Wo?", "Antworten, Weiterleiten", "Ordner anlegen"]),
          (OUTLOOK, "Outlook – Kalender", "Block 03", ["Neues Ereignis", "Termin, Besprechung", "ganztägig, Erinnerung", "Serie", "Ändern und löschen"]),
          (WORD, "Word – Texte", "Block 04", ["Speichern, Kursordner", "markieren, formatieren", "¶ und leere Absätze", "Umschalt+Enter", "Strg+Z"]),
          (WORD, "Word – Struktur", "Block 05", ["Aufzählung, Nummerierung", "Überschrift 1 und 2", "Navigationsbereich", "Tabellen", "Seitenränder, Vorschau"])]
for i, (col, h, blk, items) in enumerate(groups):
    x = 60 + i * 292; w = 272
    b += rect(x, 150, w, 470, "#FFFFFF", LINE, 14, 2)
    b += f'<path d="M{x} 164 a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v76 h-{w} z" fill="{col}"/>'
    b += text(x + w / 2, 190, h, 21, "bold", "#FFFFFF", "middle") + text(x + w / 2, 220, blk, 17, fill="#FFFFFF", anchor="middle")
    for k, t in enumerate(items): b += f'<circle cx="{x+24}" cy="{283+k*62}" r="5" fill="{col}"/>' + text(x + 38, 290 + k * 62, t, 18, fill=INK)
slides.append(("01-themen", "Was der Selbsttest abfragt", b,
  "Vier Spalten mit den Themen aus Block 02 bis 05. Outlook E-Mail: Oberfläche und Ordner; An, Cc, Bcc; Betreff; Antworten und Weiterleiten; Ordner. Outlook Kalender: Neues Ereignis; Termin, Besprechung, ganztägig; Erinnerung; Serie; Ändern und Löschen. Word Texte: Speichern; markieren und formatieren; Absatzzeichen und leere Absätze; Umschalt+Enter; Strg+Z. Word Struktur: Aufzählung und Nummerierung; Überschrift 1 und 2; Navigationsbereich; Tabellen; Seitenränder und Vorschau."))

# 2 So nutzen Sie den Selbsttest
b = ""
import math
steps = [("1", "Beantworten", "ohne nachzusehen", OUTLOOK), ("2", "Prüfen", "mit den Lösungen", EXCEL), ("3", "Nachschlagen", "im genannten Block", WORD), ("4", "Wiederholen", "die passende Übung", ACCENT)]
cx, cy, r = 400, 390, 170
for i, (n, h, t, col) in enumerate(steps):
    a = -math.pi / 2 + i * math.pi / 2
    x, y = cx + r * math.cos(a), cy + r * math.sin(a)
    b += f'<circle cx="{x}" cy="{y}" r="78" fill="#FFFFFF" stroke="{col}" stroke-width="4"/>'
    b += text(x, y - 20, n, 26, "bold", col, "middle") + text(x, y + 10, h, 20, "bold", INK, "middle") + text(x, y + 36, t, 14, fill=MUTED, anchor="middle")
    a2 = a + math.pi / 4
    ax, ay = cx + (r - 10) * math.cos(a2), cy + (r - 10) * math.sin(a2)
    b += f'<path d="M{ax-12*math.sin(a2):.1f} {ay+12*math.cos(a2):.1f} l{24*-math.sin(a2):.1f} {24*math.cos(a2):.1f}" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
b += rect(700, 180, 520, 430, SOFTYELLOW, ACCENT, 14, 2)
b += text(730, 225, "Ehrlich zu sich sein", 26, "bold", INK)
for k, t in enumerate(["Eine falsche Antwort ist kein", "Fehler, sondern ein Hinweis:", "Hier lohnt sich ein zweiter Blick.", "", "Was Sie in Block 06 nachschlagen", "mussten, prüfen Sie hier besonders.", "", "Ziel: 12 von 15 richtig – dann", "geht es mit Excel weiter."]):
    b += text(730, 275 + k * 36, t, 21, "bold" if k in (7, 8) else "normal", INK)
slides.append(("02-so-gehts", "So nutzen Sie den Selbsttest", b,
  "Ein Kreislauf aus vier Schritten: 1 Beantworten ohne nachzusehen, 2 Prüfen mit den Lösungen, 3 Nachschlagen im genannten Block, 4 die passende Übung wiederholen. Daneben: Eine falsche Antwort ist ein Hinweis, wo sich ein zweiter Blick lohnt; was in Block 06 nachgeschlagen werden musste, besonders prüfen; Ziel 12 von 15 richtig, dann geht es mit Excel weiter."))

for i, (name, title, body, desc) in enumerate(slides, 1):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(frame(i, title, body, desc))
print("ok", len(slides))
