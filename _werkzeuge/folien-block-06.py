# Folien Block 06 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-06.py assets/folien/block-06
# Vorschau: magick -density 72 assets/folien/block-06/01-der-fall.svg vorschau.png
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
{text(60,694,"Block 06 · Praxis Outlook und Word",20,fill=MUTED)}
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

# 1 Der Fall
b = text(60, 175, "Tim Rauch (Lernwerk Akademie, 3. OG): „Bei uns bleiben die Heizkörper kalt.“", 24, "bold", INK)
stations = [(OUTLOOK, "1", "E-Mail", ["Auftrag an", "Heizungstechnik", "Berlin, Cc", "Hausverwaltung"], "Block 02"),
            (OUTLOOK, "2", "Termin", ["Prüfung", "durch den Techniker", "mit Erinnerung", ""], "Block 03"),
            (WORD, "3", "Aushang", ["Information", "für die Mieter", "im 3. OG", ""], "Block 04"),
            (WORD, "4", "Protokoll", ["Störung mit", "Überschriften", "und Tabelle", "festhalten"], "Block 05"),
            (OUTLOOK, "5", "Ordnung", ["E-Mails in den", "Ordner", "„Störungsmeldungen“", ""], "Block 02")]
for i, (col, n, h, lines, blk) in enumerate(stations):
    x = 60 + i * 236; w = 214
    b += rect(x, 215, w, 330, "#FFFFFF", LINE, 14, 2)
    b += f'<path d="M{x} 229 a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v56 h-{w} z" fill="{col}"/>'
    b += f'<circle cx="{x+34}" cy="250" r="18" fill="#FFFFFF"/>' + text(x + 34, 257, n, 20, "bold", col, "middle") + text(x + 62, 258, h, 24, "bold", "#FFFFFF")
    for k, t in enumerate(lines): b += text(x + w / 2, 330 + k * 32, t, 19, fill=INK, anchor="middle")
    b += text(x + w / 2, 520, blk, 17, "bold", MUTED, "middle")
    if i < 4: b += f'<path d="M{x+w+2} 380 h18" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
b += rect(60, 570, 1160, 55, SOFTYELLOW, ACCENT, 10, 2) + text(640, 606, "Ein Fall, fünf Schritte – alles, was Sie in Block 02 bis 05 gelernt haben.", 22, "bold", INK, "middle")
slides.append(("01-der-fall", "Ein Fall, fünf Schritte", b,
  "Ausgangspunkt: Tim Rauch von der Lernwerk Akademie im 3. OG meldet kalte Heizkörper. Fünf Stationen: 1 E-Mail – Auftrag an Heizungstechnik Berlin mit der Hausverwaltung in Cc (Block 02); 2 Termin – Prüfung durch den Techniker mit Erinnerung (Block 03); 3 Aushang – Information für die Mieter im 3. OG (Block 04); 4 Protokoll – Störung mit Überschriften und Tabelle festhalten (Block 05); 5 Ordnung – E-Mails in den Ordner Störungsmeldungen (Block 02)."))

# 2 Woran Sie denken
b = ""
cols = [(OUTLOOK, "Outlook", ["Betreff: Was? Wo?", "An: soll etwas tun", "Cc: soll Bescheid wissen", "nur eigene Adressen", "Erinnerung 1 Tag vorher", "Ordner statt Stapel"]),
        (WORD, "Word", ["erst markieren, dann formatieren", "Titel groß, Wichtiges fett", "Überschrift 1 / 2 aus den Vorlagen", "Tabelle: Tab springt weiter", "keine leeren Absätze", "früh und oft Strg+S"])]
for i, (col, name, items) in enumerate(cols):
    x = 60 + i * 590; w = 570
    b += rect(x, 150, w, 470, "#FFFFFF", LINE, 14, 2)
    b += f'<path d="M{x} 164 a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v50 h-{w} z" fill="{col}"/>'
    b += text(x + w / 2, 194, name, 26, "bold", "#FFFFFF", "middle")
    for k, t in enumerate(items): b += checkrow(x + 30, 268 + k * 58, t, col, 22)
slides.append(("02-checkliste", "Woran Sie denken", b,
  "Zwei Spalten mit Häkchen. Outlook: Betreff mit Was und Wo, An für die Person, die etwas tun soll, Cc für die, die Bescheid wissen soll, nur eigene Adressen, Erinnerung einen Tag vorher, Ordner statt Stapel. Word: erst markieren, dann formatieren, Titel groß und Wichtiges fett, Überschrift 1 und 2 aus den Formatvorlagen, in der Tabelle springt Tab weiter, keine leeren Absätze, früh und oft Strg+S."))

for i, (name, title, body, desc) in enumerate(slides, 1):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(frame(i, title, body, desc))
print("ok", len(slides))
