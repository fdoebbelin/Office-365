# Folien Block 04 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-04.py assets/folien/block-04
# Vorschau: magick -density 72 assets/folien/block-04/01-word-oberflaeche.svg vorschau.png
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
{text(60,694,"Block 04 · Texte erstellen, formatieren und speichern",20,fill=MUTED)}
{text(W-60,694,"Haus Lichtblick – Microsoft 365  ·  Folie "+str(nr),20,fill=MUTED,anchor="end")}
</svg>
'''

slides = []
def btn(x, y, w, h, label, size=18, bold=True, fill="#FFFFFF", stroke=LINE, col=INK, italic=False, underline=False):
    s = rect(x, y, w, h, fill, stroke, 6, 1.5) + text(x + w / 2, y + h / 2 + size * 0.36, label, size, "bold" if bold else "normal", col, "middle", italic)
    if underline: s += f'<line x1="{x+w/2-7}" y1="{y+h/2+size*0.5}" x2="{x+w/2+7}" y2="{y+h/2+size*0.5}" stroke="{col}" stroke-width="2"/>'
    return s

# 1 Word-Oberfläche
b = ""
x0, y0, x1, y1 = 60, 140, 1220, 630
b += rect(x0, y0, x1 - x0, y1 - y0, "#F3F2F1", INK, 10, 3)
b += f'<path d="M{x0} {y0+10} a10 10 0 0 1 10 -10 h{x1-x0-20} a10 10 0 0 1 10 10 v28 h-{x1-x0} z" fill="{WORD}"/>'
b += text(x0 + 20, y0 + 25, "AutoSpeichern", 15, fill="#FFFFFF") + rect(x0 + 128, y0 + 11, 36, 18, "#FFFFFF", rx=9) + f'<circle cx="{x0+138}" cy="{y0+20}" r="6" fill="{WORD}"/>'
b += text(640, y0 + 25, "Aushang-Aufzug.docx", 16, "bold", "#FFFFFF", "middle")
# Registerkarten
tabs = ["Datei", "Start", "Einfügen", "Layout", "Überprüfen", "Ansicht"]
tx = x0 + 20
for i, t in enumerate(tabs):
    b += text(tx, y0 + 62, t, 16, "bold" if i == 1 else "normal", WORD if i == 1 else INK)
    if i == 1: b += f'<line x1="{tx}" y1="{y0+68}" x2="{tx+38}" y2="{y0+68}" stroke="{WORD}" stroke-width="3"/>'
    tx += len(t) * 9 + 34
b += rect(x0 + 2, y0 + 74, x1 - x0 - 4, 70, "#FFFFFF", rx=0)
# Gruppe Schriftart
gx = x0 + 120
b += rect(gx, y0 + 82, 130, 24, "#FFFFFF", LINE, 4, 1.5) + text(gx + 8, y0 + 99, "Aptos", 14, fill=INK)
b += rect(gx + 136, y0 + 82, 44, 24, "#FFFFFF", LINE, 4, 1.5) + text(gx + 150, y0 + 99, "11", 14, fill=INK)
b += btn(gx, y0 + 110, 26, 24, "F", 15) + btn(gx + 30, y0 + 110, 26, 24, "K", 15, italic=True) + btn(gx + 60, y0 + 110, 26, 24, "U", 15, underline=True)
b += text(gx + 90, y0 + 140, "Schriftart", 12, fill=MUTED, anchor="middle")
b += f'<line x1="{gx+200}" y1="{y0+82}" x2="{gx+200}" y2="{y0+140}" stroke="{LINE}" stroke-width="1.5"/>'
b += btn(gx + 220, y0 + 82, 30, 24, "¶", 15) + text(gx + 290, y0 + 140, "Absatz", 12, fill=MUTED, anchor="middle")
b += pill(1000, y0 + 118, "Menüband", NAVY, 20, "middle")
# Lineal
b += rect(x0 + 300, y0 + 152, 680, 18, "#FFFFFF", LINE, 2, 1)
for k in range(17): b += f'<line x1="{x0+320+k*40}" y1="{y0+162}" x2="{x0+320+k*40}" y2="{y0+170}" stroke="{MUTED}" stroke-width="1"/>'
b += pill(x0 + 140, y0 + 230, "Lineal", NAVY, 18, "middle")
# Seite
b += rect(x0 + 300, y0 + 180, 680, 260, "#FFFFFF", LINE, 0, 1.5)
b += text(x0 + 640, y0 + 236, "Aufzug außer Betrieb", 34, "bold", INK, "middle")
for k in range(4): b += bar(x0 + 360, y0 + 280 + k * 30, 560 - (k % 2) * 120)
b += pill(x0 + 1090, y0 + 300, "Dokument", NAVY, 18, "middle")
# Statusleiste
b += rect(x0 + 2, y1 - 40, x1 - x0 - 4, 38, "#E8E6E4", rx=0)
b += text(x0 + 20, y1 - 15, "Seite 1 von 1     42 Wörter     Deutsch (Deutschland)", 15, fill=INK)
b += text(x1 - 20, y1 - 15, "–  ———●———  +   100 %", 15, fill=INK, anchor="end")
b += pill(640, y1 - 52, "Statusleiste", NAVY, 18, "middle")
slides.append(("01-word-oberflaeche", "Word auf einen Blick", b,
  "Schema des Word-Fensters: oben die Titelleiste mit AutoSpeichern und dem Dateinamen, darunter die Registerkarten Datei, Start, Einfügen, Layout, Überprüfen, Ansicht und das Menüband mit der Gruppe Schriftart (Aptos, 11, F, K, U) und dem Absatzzeichen. Darunter das Lineal, die Seite mit dem Aushang „Aufzug außer Betrieb“ und unten die Statusleiste mit Seitenzahl, Wörtern, Sprache und Zoom."))

# 2 Speichern
b = ""
# Aktenschrank
items = [("PC", "Aktenschrank", NAVY), ("Ordner", "Schublade", ACCENT), ("Datei", "Akte", WORD)]
for i, (h, a, col) in enumerate(items):
    x = 80 + i * 220
    b += rect(x, 160, 180, 150, "#FFFFFF", col, 12, 3)
    b += text(x + 90, 225, h, 32, "bold", col, "middle") + text(x + 90, 270, a, 22, fill=MUTED, anchor="middle")
    if i < 2: b += f'<path d="M{x+184} 235 h30" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
b += text(80, 360, "Dokumente  ›  Haus-Lichtblick  ›  Aushang-Aufzug.docx", 24, "bold", INK)
# Schritte
steps = [("Strg+S", "Speichern drücken"), ("Name", "z. B. Aushang-Aufzug"), ("Ort", "Ordner auswählen"), ("Speichern", "klicken – fertig")]
for i, (k, t) in enumerate(steps):
    y = 175 + i * 70
    b += rect(780, y, 140, 46, SOFTBLUE, WORD, 8, 2) + text(850, y + 31, k, 20, "bold", WORD, "middle")
    b += text(940, y + 31, t, 22, fill=INK)
b += rect(80, 410, 540, 210, SOFTGREEN, EXCEL, 12, 2)
b += text(105, 450, "Gute Dateinamen", 24, "bold", EXCEL)
for i, t in enumerate(["Aushang-Aufzug", "Protokoll-Begehung-3OG", "Mieterbrief-Heizung"]):
    b += text(105, 492 + i * 38, "✓  " + t, 22, fill=INK)
b += rect(660, 470, 560, 150, SOFTRED, BAD, 12, 2)
b += text(685, 510, "So nicht", 24, "bold", BAD)
for i, t in enumerate(["Dokument1", "neu neu final 2", "Aushang/Aufzug  (/ ist verboten)"]):
    b += text(685, 548 + i * 30, "✗  " + t, 20, fill=INK)
slides.append(("02-speichern", "Speichern: Ordnung wie im Aktenschrank", b,
  "Oben der Vergleich: PC ist der Aktenschrank, der Ordner die Schublade, die Datei die Akte – Beispiel Dokumente, Haus-Lichtblick, Aushang-Aufzug.docx. Rechts die Schritte: Strg+S, Namen vergeben, Ort wählen über Weitere Speicheroptionen, Speichern. Unten gute Dateinamen wie Aushang-Aufzug und schlechte wie Dokument1 oder Namen mit Schrägstrich."))

# 3 Markieren und formatieren
b = text(640, 180, "Erst markieren, dann formatieren.", 34, "bold", INK, "middle")
b += text(640, 220, "Wie beim Streichen: erst abkleben, dann Farbe auftragen.", 22, fill=MUTED, anchor="middle", italic=True)
b += rect(140, 255, 1000, 90, "#FFFFFF", LINE, 10, 2)
b += rect(372, 272, 262, 54, "#C7DCF5", rx=4)
b += text(170, 312, "Der Aufzug ist", 30, fill=INK) + text(382, 312, "den ganzen Tag", 30, "bold", INK) + text(645, 312, "außer Betrieb.", 30, fill=INK)
b += text(503, 370, "markiert: mit gedrückter Maustaste darüberziehen", 18, fill=MUTED, anchor="middle")
fmt = [("F", "Fett", "Strg+Umschalt+F", {}), ("K", "Kursiv", "Strg+Umschalt+K", {"italic": True}), ("U", "Unterstrichen", "Strg+Umschalt+U", {"underline": True})]
for i, (k, n, sc, kw) in enumerate(fmt):
    x = 120 + i * 360
    b += btn(x, 420, 60, 60, k, 30, **kw)
    b += text(x + 80, 445, n, 26, "bold", INK) + text(x + 80, 476, sc, 20, fill=WORD)
b += rect(120, 530, 1040, 90, SOFTYELLOW, ACCENT, 12, 2)
b += text(150, 568, "Schriftart und Schriftgröße: Start → Gruppe „Schriftart“", 22, "bold", INK)
b += text(150, 600, "Fließtext 11 pt · Überschrift 16–20 pt · Aushang 14–18 pt, Titel noch größer", 20, fill=INK)
slides.append(("03-formatieren", "Text formatieren", b,
  "Merksatz: Erst markieren, dann formatieren – wie beim Streichen erst abkleben. Beispiel: In „Der Aufzug ist den ganzen Tag außer Betrieb“ sind die Wörter „den ganzen Tag“ markiert und fett. Darunter die Schaltflächen F für Fett (Strg+Umschalt+F), K für Kursiv (Strg+Umschalt+K), U für Unterstrichen (Strg+Umschalt+U). Hinweis zu Schriftgrößen: Fließtext 11 pt, Überschrift 16 bis 20 pt, Aushang 14 bis 18 pt."))

# 4 Absatz und Zeilenumbruch
b = ""
for i, (key, sym, head, lines, col, soft) in enumerate([
        ("Enter", "¶", "Neuer Absatz", ["Bitte nutzen Sie die Treppe.¶", "Wir bitten um Verständnis.¶"], WORD, SOFTBLUE),
        ("Umschalt+Enter", "↵", "Neue Zeile im selben Absatz", ["Thomas Weber, Hausmeister↵", "thomas.weber@haus-lichtblick.de¶"], EXCEL, SOFTGREEN)]):
    x = 60 + i * 590; w = 570
    b += rect(x, 150, w, 300, soft, col, 14, 2)
    b += rect(x + 30, 180, 220 if i else 120, 56, "#FFFFFF", col, 8, 3) + text(x + 30 + (110 if i else 60), 217, key, 24, "bold", col, "middle")
    b += text(x + w - 40, 225, sym, 54, "bold", col, "end")
    b += text(x + 30, 285, head, 28, "bold", INK)
    b += rect(x + 30, 310, w - 60, 115, "#FFFFFF", LINE, 8, 1.5)
    for k, l in enumerate(lines): b += text(x + 50, 355 + k * 44, l, 22, fill=INK)
b += rect(60, 475, 1160, 150, SOFTYELLOW, ACCENT, 12, 2)
b += text(90, 515, "Nicht mehrmals Enter für Abstand drücken.", 26, "bold", INK)
b += text(90, 552, "Leere Absätze verrutschen, sobald sich der Text ändert. Abstand einstellen: „Layout“ → „Abstand“.", 21, fill=INK)
b += text(90, 590, "Zeichen sichtbar machen: Start → ¶ („Alle anzeigen“) – noch einmal klicken blendet sie aus.", 21, fill=INK)
slides.append(("04-absatz-zeilenumbruch", "Absatz oder neue Zeile?", b,
  "Links: Die Enter-Taste beginnt einen neuen Absatz, sichtbar als Zeichen ¶. Rechts: Umschalt+Enter beginnt eine neue Zeile im selben Absatz, sichtbar als Pfeil – zum Beispiel zwischen Name und E-Mail-Adresse des Hausmeisters. Hinweis: nicht mehrmals Enter für Abstand drücken, Abstand über Layout einstellen; die Zeichen blendet die Schaltfläche ¶ auf der Registerkarte Start ein und aus."))

# 5 Vorher – nachher
b = ""
def page(x, y, w, h):
    return rect(x, y, w, h, "#FFFFFF", MUTED, 4, 2)
b += page(110, 150, 360, 470) + text(290, 140, "vorher", 24, "bold", MUTED, "middle")
for k, (t, sz) in enumerate([("Aufzug außer Betrieb", 15), ("Personenaufzug – Haus Lichtblick", 15), ("Liebe Mieterinnen und Mieter,", 15), ("am Montag ist der Personenaufzug", 15), ("wegen Wartung den ganzen Tag", 15), ("außer Betrieb. Bitte nutzen Sie …", 15)]):
    b += text(135, 185 + k * 24 + (k > 1) * 60, t, sz, fill=INK)
for k in range(3): b += text(135, 230 + k * 18, "¶", 14, fill=MUTED)
b += f'<path d="M500 385 h120" stroke="{ACCENT}" stroke-width="6" marker-end="url(#pf)"/>'
b += page(650, 150, 360, 470) + text(830, 140, "nachher", 24, "bold", WORD, "middle")
b += text(830, 220, "Aufzug außer", 34, "bold", BAD, "middle") + text(830, 262, "Betrieb", 34, "bold", BAD, "middle")
b += text(830, 300, "Personenaufzug – Haus Lichtblick", 17, "bold", INK, "middle")
for k, t in enumerate(["Liebe Mieterinnen und Mieter,", "am Montag ist der Personenaufzug", "wegen Wartung den ganzen Tag", "außer Betrieb. Bitte nutzen Sie …"]):
    b += text(680, 350 + k * 28, t, 17, "bold" if k == 2 else "normal", INK)
b += text(680, 520, "Thomas Weber, Hausmeister", 15, fill=MUTED, italic=True) + text(680, 542, "thomas.weber@haus-lichtblick.de", 15, fill=MUTED, italic=True)
notes = ["Titel groß und fett", "zentriert", "Text 14–16 pt", "Wichtiges fett", "leere Absätze weg"]
for i, t in enumerate(notes):
    b += f'<circle cx="1045" cy="{230+i*70}" r="8" fill="{EXCEL}"/>' + text(1060, 238 + i * 70, t, 20, fill=INK)
slides.append(("05-aushang", "Vom Rohtext zum Aushang", b,
  "Links der Rohtext des Aushangs „Aufzug außer Betrieb“ in kleiner, einheitlicher Schrift mit leeren Absätzen. Rechts derselbe Aushang formatiert: Titel groß, fett und zentriert, Untertitel fett, Text größer, die Worte „den ganzen Tag“ fett, der Kontakt zum Hausmeister kursiv. Daneben die Schritte: Titel groß und fett, zentriert, Text 14 bis 16 pt, Wichtiges fett, leere Absätze weg."))

for i, (name, title, body, desc) in enumerate(slides, 1):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(frame(i, title, body, desc))
print("ok", len(slides))
