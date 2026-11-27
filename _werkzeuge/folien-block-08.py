# Folien Block 08 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-08.py assets/folien/block-08
# Vorschau: magick -density 72 assets/folien/block-08/01-excel-oberflaeche.svg vorschau.png
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
{text(60,694,"Block 08 · Excel-Grundlagen",20,fill=MUTED)}
{text(W-60,694,"Haus Lichtblick – Microsoft 365  ·  Folie "+str(nr),20,fill=MUTED,anchor="end")}
</svg>
'''

slides = []
SOFTX = "#E7F4EC"
def grid(x, y, cols, rows, cw, rh, data=None, sel=None, headfill="#F3F5F8", colw=None, bold_row=None, aligns=None, size=17):
    """Excel-Raster mit Spalten- und Zeilenköpfen. data: dict (r,c)->text (r,c ab 1)."""
    colw = colw or [cw] * cols
    s = rect(x, y, 40, rh, headfill, LINE, 0, 1)
    cx = x + 40
    for c in range(cols):
        s += rect(cx, y, colw[c], rh, headfill, LINE, 0, 1) + text(cx + colw[c] / 2, y + rh * 0.68, chr(65 + c), 15, fill=MUTED, anchor="middle")
        cx += colw[c]
    for r in range(1, rows + 1):
        yy = y + r * rh
        s += rect(x, yy, 40, rh, headfill, LINE, 0, 1) + text(x + 20, yy + rh * 0.68, str(r), 15, fill=MUTED, anchor="middle")
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

# 1 Oberfläche
b = ""
x0, y0, x1, y1 = 60, 140, 1220, 630
b += rect(x0, y0, x1 - x0, y1 - y0, "#FFFFFF", INK, 10, 3)
b += f'<path d="M{x0} {y0+10} a10 10 0 0 1 10 -10 h{x1-x0-20} a10 10 0 0 1 10 10 v28 h-{x1-x0} z" fill="{EXCEL}"/>'
b += text(640, y0 + 25, "Inventarliste.xlsx", 16, "bold", "#FFFFFF", "middle")
for i, t in enumerate(["Datei", "Start", "Einfügen", "Seitenlayout", "Formeln", "Daten", "Ansicht"]):
    b += text(x0 + 20 + i * 100, y0 + 60, t, 16, "bold" if i == 1 else "normal", EXCEL if i == 1 else INK)
b += rect(x0 + 2, y0 + 70, x1 - x0 - 4, 50, GREY, rx=0)
b += pill(300, y0 + 104, "Menüband", NAVY, 18, "middle")
# Namenfeld + Bearbeitungsleiste
fy = y0 + 128
b += rect(x0 + 10, fy, 110, 30, "#FFFFFF", LINE, 2, 1.5) + text(x0 + 20, fy + 21, "C2", 16, "bold", INK)
b += text(x0 + 140, fy + 21, "fx", 16, "bold", MUTED, italic=True)
b += rect(x0 + 170, fy, 980, 30, "#FFFFFF", LINE, 2, 1.5) + text(x0 + 182, fy + 21, "15", 16, fill=INK)
data = {(1, 1): "Artikel", (1, 2): "Lagerort", (1, 3): "Bestand", (2, 1): "Allzweckreiniger", (2, 2): "Lagerraum EG-01", (2, 3): "15",
        (3, 1): "Müllbeutel 120 l", (3, 2): "Lagerraum EG-01", (3, 3): "200"}
b += grid(x0 + 10, fy + 44, 7, 7, 120, 32, data, (2, 3), colw=[200, 180, 110, 120, 120, 120, 120], bold_row=1, aligns={3: "end"})
b += rect(x0 + 2, y1 - 40, x1 - x0 - 4, 38, GREY, rx=0)
b += rect(x0 + 40, y1 - 38, 110, 32, "#FFFFFF", EXCEL, 0, 2) + text(x0 + 95, y1 - 16, "Inventar", 16, "bold", EXCEL, "middle") + text(x0 + 170, y1 - 15, "+", 20, "bold", MUTED)
b += pill(x0 + 65, fy - 14, "Namenfeld", EXCEL, 16, "middle")
b += pill(700, fy - 14, "Bearbeitungsleiste", EXCEL, 16, "middle")
b += pill(1100, 480, "aktive Zelle C2", EXCEL, 18, "middle") + f'<path d="M990 470 L560 {fy+44+2*32+16}" stroke="{ACCENT}" stroke-width="3" marker-end="url(#pf)"/>'
b += pill(430, y1 - 14, "Tabellenblatt", NAVY, 16, "middle")
slides.append(("01-excel-oberflaeche", "Excel auf einen Blick", b,
  "Schema des Excel-Fensters: oben die Registerkarten Datei, Start, Einfügen, Seitenlayout, Formeln, Daten, Ansicht und das Menüband, darunter links das Namenfeld mit C2 und rechts die Bearbeitungsleiste mit dem Inhalt 15. Darunter das Tabellenraster mit Spaltenköpfen A bis G und Zeilennummern, die aktive Zelle C2 ist grün umrandet. Unten das Tabellenblatt „Inventar“."))

# 2 Zelladresse und Navigation
b = text(60, 175, "Jede Zelle hat eine Adresse: erst die Spalte, dann die Zeile.", 26, "bold", INK)
b += grid(80, 210, 5, 6, 90, 50, {(4, 3): "C4"}, (4, 3), size=22)
b += f'<rect x="{80+40+180}" y="210" width="90" height="350" fill="{EXCEL}" fill-opacity="0.08"/>'
b += f'<rect x="80" y="{210+4*50}" width="490" height="50" fill="{EXCEL}" fill-opacity="0.08"/>'
b += text(345, 205, "Spalte C", 18, "bold", EXCEL, "middle")
keys = [("Pfeiltasten", "eine Zelle weiter"), ("Enter", "nach unten"), ("Tab", "nach rechts"), ("Strg+Pos1", "zurück nach A1"), ("Namenfeld", "Adresse tippen, Enter")]
for i, (k, t) in enumerate(keys):
    y = 220 + i * 72
    b += rect(660, y, 190, 50, SOFTX, EXCEL, 8, 2) + text(755, y + 33, k, 21, "bold", EXCEL, "middle")
    b += text(870, y + 33, t, 22, fill=INK)
b += text(660, 610, "Wie beim Stadtplan: Planquadrat C4.", 22, fill=MUTED, italic=True)
slides.append(("02-zelladresse", "Zellen und Adressen", b,
  "Links ein Raster mit den Spalten A bis E und den Zeilen 1 bis 6; Spalte C und Zeile 4 sind hervorgehoben, wo sie sich kreuzen, liegt die Zelle C4. Rechts die Tasten zum Bewegen: Pfeiltasten eine Zelle weiter, Enter nach unten, Tab nach rechts, Strg+Pos1 zurück nach A1, Namenfeld – Adresse tippen und Enter. Vergleich: wie ein Planquadrat auf dem Stadtplan."))

# 3 Eingeben
b = ""
data = {(1, 1): "Artikel", (1, 2): "Bestand", (1, 3): "Stand", (2, 1): "Glasreiniger", (2, 2): "8", (2, 3): "15.04.2025", (3, 1): "Schwämme", (3, 2): "25", (3, 3): "######"}
b += grid(60, 160, 3, 3, 0, 52, data, colw=[210, 120, 150], bold_row=1, aligns={2: "end", 3: "end"}, size=20)
b += rect(60 + 40 + 330, 160 + 3 * 52, 150, 52, "none", BAD, 0, 3)
notes = [("Text", "steht links", WORD), ("Zahlen und Datum", "stehen rechts – Excel kann damit rechnen", EXCEL), ("######", "Spalte zu schmal – breiter ziehen", BAD)]
for i, (h, t, col) in enumerate(notes):
    y = 180 + i * 90
    b += text(700, y, h, 26, "bold", col) + text(700, y + 34, t, 21, fill=INK)
b += rect(60, 420, 1160, 200, SOFTYELLOW, ACCENT, 12, 2)
b += text(90, 462, "So geht's", 24, "bold", INK)
rows = ["Zelle anklicken, tippen, mit Enter (nach unten) oder Tab (nach rechts) bestätigen", "Datum mit Punkten eingeben: 15.04.2025",
        "Inhalt ändern: Zelle anklicken und neu tippen – oder F2 bzw. in die Bearbeitungsleiste klicken", "Esc bricht die Eingabe ab, Entf leert die Zelle"]
for i, t in enumerate(rows): b += text(90, 500 + i * 30, "•  " + t, 20, fill=INK)
slides.append(("03-eingeben", "Text, Zahlen und Datum eingeben", b,
  "Ein kleines Raster: Text wie „Glasreiniger“ steht links, Zahlen wie 8 und das Datum 15.04.2025 stehen rechts; eine zu schmale Spalte zeigt ######. Darunter: Zelle anklicken, tippen, mit Enter oder Tab bestätigen; Datum mit Punkten eingeben; Inhalt ändern mit neu tippen, F2 oder in der Bearbeitungsleiste; Esc bricht ab, Entf leert die Zelle."))

# 4 Spaltenbreite und Format
b = ""
# Spaltenköpfe mit Doppelpfeil
b += rect(80, 170, 40, 44, GREY, LINE, 0, 1)
for i, (c, w) in enumerate([("A", 150), ("B", 220)]):
    b += rect(120 + (0 if i == 0 else 150), 170, w, 44, GREY, LINE, 0, 1) + text(120 + (0 if i == 0 else 150) + w / 2, 200, c, 20, fill=MUTED, anchor="middle")
b += f'<line x1="270" y1="160" x2="270" y2="225" stroke="{EXCEL}" stroke-width="4"/>'
b += f'<path d="M245 192 h-14 l8 -6 m-8 6 l8 6 M295 192 h14 l-8 -6 m8 6 l-8 6" stroke="{EXCEL}" stroke-width="3" fill="none"/>'
b += text(80, 260, "Doppelklick auf die Trennlinie im Spaltenkopf:", 22, "bold", INK)
b += text(80, 292, "Die Spalte passt sich dem längsten Eintrag an.", 22, fill=INK)
b += text(80, 324, "Oder mit gedrückter Maustaste ziehen.", 22, fill=INK)
# Kopfzeile formatieren
data = {(1, 1): "Artikel", (1, 2): "Lagerort", (1, 3): "Bestand", (2, 1): "Allzweckreiniger", (2, 2): "Lagerraum EG-01", (2, 3): "15"}
b += grid(660, 160, 3, 2, 0, 48, data, colw=[200, 180, 110], bold_row=1, aligns={3: "end"}, size=19)
b += f'<rect x="700" y="208" width="490" height="48" fill="{EXCEL}" fill-opacity="0.18"/>'
b += text(660, 330, "Kopfzeile: markieren, dann", 22, "bold", INK)
for i, (k, t) in enumerate([("F", "Fett · Strg+Umschalt+F"), ("▰", "Füllfarbe · Start → Schriftart")]):
    y = 355 + i * 58
    b += rect(660, y, 46, 42, "#FFFFFF", LINE, 6, 1.5) + text(683, y + 30, k, 22, "bold", EXCEL if i else INK, "middle") + text(722, y + 29, t, 21, fill=INK)
b += rect(60, 500, 1160, 120, SOFTX, EXCEL, 12, 2)
b += text(90, 540, "Mehrere Spalten auf einmal: Spaltenköpfe A bis E markieren,", 22, "bold", INK)
b += text(90, 574, "dann auf eine der Trennlinien doppelklicken.", 22, "bold", INK)
b += text(90, 606, "Wie beim Kleiderschrank: Jede Spalte bekommt so viel Platz, wie sie braucht.", 19, fill=MUTED, italic=True)
slides.append(("04-spaltenbreite-format", "Spaltenbreite und Kopfzeile", b,
  "Links: Doppelklick auf die Trennlinie zwischen zwei Spaltenköpfen passt die Spalte dem längsten Eintrag an, oder man zieht mit gedrückter Maustaste. Rechts: Die Kopfzeile Artikel, Lagerort, Bestand wird markiert und mit Fett (Strg+Umschalt+F) und Füllfarbe hervorgehoben. Unten: mehrere Spalten markieren und auf eine Trennlinie doppelklicken."))

# 5 Erste Formel
b = text(60, 175, "Jede Formel beginnt mit =", 30, "bold", INK)
data = {(1, 3): "Bestand", (1, 4): "Mindestmenge", (1, 6): "Differenz", (2, 3): "8", (2, 4): "10", (2, 6): "=C2-D2"}
b += grid(60, 200, 6, 2, 0, 50, data, (2, 6), colw=[90, 40, 110, 170, 40, 140], bold_row=1, aligns={3: "end", 4: "end"}, size=20)
b += rect(60 + 40 + 130, 300, 110, 50, "none", OUTLOOK, 0, 3) + rect(60 + 40 + 240, 300, 170, 50, "none", BAD, 0, 3)
b += text(840, 300, "=C2-D2", 40, "bold", INK) + text(1060, 300, "→  -2", 40, "bold", BAD)
b += text(840, 340, "Bestand minus Mindestmenge", 22, fill=MUTED)
steps = ["= tippen", "Zelle C2 anklicken", "- tippen", "Zelle D2 anklicken", "Enter"]
for i, t in enumerate(steps):
    x = 60 + i * 232
    b += rect(x, 450, 215, 70, SOFTX, EXCEL, 10, 2) + text(x + 107, 494, t, 21, "bold", INK, "middle")
    if i < 4: b += f'<path d="M{x+217} 485 h12" stroke="{ACCENT}" stroke-width="4" marker-end="url(#pf)"/>'
b += text(60, 580, "Negativ heißt: weniger als die Mindestmenge – nachbestellen.", 23, "bold", BAD)
b += text(60, 614, "Ändert sich der Bestand, rechnet Excel sofort neu.", 21, fill=INK)
slides.append(("05-erste-formel", "Die erste Formel", b,
  "In Zelle F2 steht die Formel =C2-D2: Bestand 8 minus Mindestmenge 10 ergibt minus 2. Die Schritte: Gleichheitszeichen tippen, Zelle C2 anklicken, Minus tippen, Zelle D2 anklicken, Enter. Ein negatives Ergebnis heißt: weniger als die Mindestmenge, nachbestellen. Ändert sich der Bestand, rechnet Excel sofort neu."))

for i, (name, title, body, desc) in enumerate(slides, 1):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(frame(i, title, body, desc))
print("ok", len(slides))
