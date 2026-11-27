# Folien Block 11 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-11.py assets/folien/block-11
# Vorschau: magick -density 72 assets/folien/block-11/01-team.svg vorschau.png
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
{text(60,694,"Block 11 · Programme verknüpfen",20,fill=MUTED)}
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

# 1 Team
b = ""
for i, (col, name, lines) in enumerate([(EXCEL, "Excel", ["Daten sammeln", "rechnen,", "Diagramm"]), (WORD, "Word", ["Bericht schreiben", "Tabelle und Diagramm", "einfügen"]), (OUTLOOK, "Outlook", ["Bericht versenden", "als Anhang", "an die Hausverwaltung"])]):
    x = 60 + i * 410
    b += appcard(x, 160, 340, 270, col, name, lines)
    if i < 2: b += f'<path d="M{x+348} 295 h52" stroke="{ACCENT}" stroke-width="7" marker-end="url(#pf)"/>'
    b += text(x + 170, 470, ["Strg+C", "Strg+V", "Datei anfügen"][i], 26, "bold", col, "middle")
b += rect(60, 510, 1160, 110, SOFTYELLOW, ACCENT, 12, 2)
b += text(90, 552, "Excel ist der Rechner, Word der Schreibtisch, Outlook der Briefkasten.", 23, "bold", INK)
b += text(90, 590, "Im Haus Lichtblick: Stromzahlen → Jahresbericht → E-Mail an Petra Schönfeld", 21, fill=INK)
slides.append(("01-team", "Drei Programme als Team", b,
  "Drei Karten mit Pfeilen: Excel sammelt Daten, rechnet und erstellt das Diagramm – Strg+C; Word nimmt Tabelle und Diagramm in den Bericht auf – Strg+V; Outlook versendet den Bericht als Anhang an die Hausverwaltung – Datei anfügen. Vergleich: Excel ist der Rechner, Word der Schreibtisch, Outlook der Briefkasten."))

# 2 Tabelle kopieren
b = ""
data = {(1, 1): "Monat", (1, 2): "Verbrauch (kWh)", (2, 1): "Januar", (2, 2): "4.850", (3, 1): "Februar", (3, 2): "4.670", (4, 1): "…", (4, 2): "…"}
b += text(60, 170, "In Excel", 24, "bold", EXCEL)
b += grid(60, 190, 2, 4, 0, 44, data, colw=[140, 180], bold_row=1, aligns={2: "end"}, size=18)
b += f'<rect x="100" y="234" width="320" height="176" fill="{EXCEL}" fill-opacity="0.12" stroke="{EXCEL}" stroke-width="3" stroke-dasharray="8 5"/>'
b += text(60, 455, "markieren, Strg+C", 22, "bold", INK) + text(60, 485, "(der Rahmen „läuft“)", 19, fill=MUTED)
b += f'<path d="M460 320 h110" stroke="{ACCENT}" stroke-width="7" marker-end="url(#pf)"/>'
b += text(620, 170, "In Word", 24, "bold", WORD)
b += rect(620, 190, 600, 290, "#FFFFFF", MUTED, 4, 2)
b += text(650, 230, "1. Stromverbrauch 2025", 20, "bold", NAVY)
for r in range(4):
    for k, w in enumerate([140, 180]):
        b += rect(650 + (0 if k == 0 else 140), 250 + r * 36, w, 36, SOFTX if r == 0 else "#FFFFFF", LINE, 0, 1)
for r, (m, v) in enumerate([("Monat", "Verbrauch (kWh)"), ("Januar", "4.850"), ("Februar", "4.670"), ("…", "…")]):
    b += text(660, 274 + r * 36, m, 16, "bold" if r == 0 else "normal", INK) + text(960, 274 + r * 36, v, 16, "bold" if r == 0 else "normal", INK, "end")
b += rect(980, 400, 110, 34, "#FFFFFF", LINE, 4, 1.5) + text(1035, 423, "(Strg) ▾", 16, fill=INK, anchor="middle")
b += text(650, 465, "Schreibmarke setzen, Strg+V", 22, "bold", INK)
b += rect(60, 520, 1160, 100, SOFTYELLOW, ACCENT, 12, 2)
b += text(90, 558, "Das kleine Symbol „(Strg)“ sind die Einfügeoptionen – eingefügt ist schon.", 21, "bold", INK)
b += text(90, 592, "Die Tabelle ist jetzt eine Word-Tabelle: Sie rechnet nicht mehr und ändert sich nicht mit Excel.", 20, fill=INK)
slides.append(("02-tabelle-kopieren", "Eine Tabelle von Excel nach Word", b,
  "Links in Excel: die Tabelle mit Monat und Verbrauch ist markiert und mit Strg+C kopiert, ein laufender Rahmen zeigt das. Rechts in Word: unter der Überschrift Stromverbrauch 2025 steht nach Strg+V dieselbe Tabelle, daneben das kleine Symbol der Einfügeoptionen. Hinweis: Das Symbol muss man nicht anklicken; die Tabelle ist jetzt eine Word-Tabelle, sie rechnet nicht mehr und ändert sich nicht mit Excel."))

# 3 Diagramm kopieren
b = ""
b += text(60, 170, "In Excel", 24, "bold", EXCEL)
b += rect(60, 190, 400, 240, "#FFFFFF", EXCEL, 4, 3)
b += columns(70, 200, 380, 220, None, None, None, labels=False)
b += text(60, 470, "Rand anklicken, Strg+C", 22, "bold", INK)
b += f'<path d="M480 310 h90" stroke="{ACCENT}" stroke-width="7" marker-end="url(#pf)"/>'
b += text(620, 170, "In Word", 24, "bold", WORD)
b += rect(620, 190, 600, 290, "#FFFFFF", MUTED, 4, 2)
b += columns(650, 210, 380, 220, None, None, None, labels=False)
b += text(650, 465, "Schreibmarke in eine leere Zeile, Strg+V", 22, "bold", INK)
b += rect(1050, 230, 150, 160, GREY, LINE, 8, 1.5) + text(1125, 262, "Einfügeoptionen", 14, "bold", MUTED, "middle")
for k, t in enumerate(["Diagramm", "Diagramm", "verknüpft", "Bild"]):
    b += rect(1062 + (k % 2) * 68, 280 + (k // 2) * 52, 58, 42, "#FFFFFF", EXCEL if k == 0 else LINE, 5, 2 if k == 0 else 1)
    b += text(1091 + (k % 2) * 68, 306 + (k // 2) * 52, ["eingeb.", "eingeb.", "Verkn.", "Bild"][k], 12, fill=INK, anchor="middle")
b += rect(60, 520, 1160, 100, SOFTYELLOW, ACCENT, 12, 2)
b += text(90, 558, "Word nimmt das Diagramm mit seinen Daten mit („eingebettet“).", 21, "bold", INK)
b += text(90, 592, "Ändern sich die Zahlen in Excel, kopieren Sie das Diagramm neu. Wer nur ein Foto will: Einfügeoption „Bild“.", 19, fill=INK)
slides.append(("03-diagramm-kopieren", "Ein Diagramm von Excel nach Word", b,
  "Links in Excel ist das Säulendiagramm am Rand angeklickt und mit Strg+C kopiert. Rechts in Word steht es nach Strg+V in einer leeren Zeile; daneben die Einfügeoptionen, unter anderem eingebettet, verknüpft und Bild. Hinweis: Word nimmt das Diagramm mit seinen Daten mit; ändern sich die Zahlen in Excel, wird das Diagramm neu kopiert; wer nur ein Foto will, wählt die Option Bild."))

# 4 Anhang
b = ""
x0, y0 = 60, 150
b += rect(x0, y0, 720, 400, "#FFFFFF", INK, 10, 3)
b += f'<path d="M{x0} {y0+10} a10 10 0 0 1 10 -10 h700 a10 10 0 0 1 10 10 v26 h-720 z" fill="{OUTLOOK}"/>'
for i, t in enumerate(["Nachricht", "Einfügen", "Optionen"]):
    b += text(x0 + 20 + i * 120, y0 + 62, t, 17, "bold" if i == 1 else "normal", OUTLOOK if i == 1 else INK)
b += rect(x0 + 20, y0 + 74, 160, 32, SOFTBLUE, OUTLOOK, 6, 2) + text(x0 + 100, y0 + 96, "Datei anfügen ▾", 16, "bold", INK, "middle")
b += rect(x0 + 20, y0 + 108, 230, 34, "#FFFFFF", MUTED, 4, 1.5) + text(x0 + 32, y0 + 131, "Diesen PC durchsuchen …", 15, fill=INK)
for i, (lab, val) in enumerate([("An", "Ihre eigene Adresse"), ("Betreff", "Jahresbericht Facility Management 2025 – Haus Lichtblick")]):
    y = y0 + 160 + i * 46
    b += text(x0 + 20, y + 24, lab, 16, "bold", MUTED) + rect(x0 + 100, y, 600, 34, "#FFFFFF", LINE, 4, 1.5) + text(x0 + 112, y + 23, val, 15, fill=INK)
b += rect(x0 + 100, y0 + 260, 300, 44, SOFTBLUE, WORD, 6, 2)
b += rect(x0 + 112, y0 + 268, 26, 28, WORD, rx=3) + text(x0 + 125, y0 + 288, "W", 15, "bold", "#FFFFFF", "middle")
b += text(x0 + 150, y0 + 288, "Jahresbericht-2025.docx", 15, "bold", INK)
b += pill(x0 + 520, y0 + 290, "Anhang", OUTLOOK, 16, "middle")
for k in range(3): b += bar(x0 + 100, y0 + 330 + k * 22, 520 - k * 90)
steps = ["Bericht in Word speichern (Strg+S)", "Neue E-Mail, An und Betreff", "„Einfügen“ → „Datei anfügen“", "„Diesen PC durchsuchen“, Datei wählen", "Anhang prüfen, Senden"]
for i, t in enumerate(steps):
    y = 185 + i * 66
    b += f'<circle cx="830" cy="{y}" r="20" fill="{OUTLOOK}"/>' + text(830, y + 7, str(i + 1), 20, "bold", "#FFFFFF", "middle") + text(862, y + 8, t, 19, fill=INK)
b += rect(60, 570, 1160, 55, SOFTX, EXCEL, 10, 2) + text(640, 605, "Oder: Datei im Explorer anfassen und in die offene E-Mail ziehen.", 20, "bold", INK, "middle")
slides.append(("04-anhang", "Den Bericht als Anhang versenden", b,
  "Schema einer neuen E-Mail im neuen Outlook: Registerkarte Einfügen, Schaltfläche Datei anfügen mit dem Eintrag Diesen PC durchsuchen; An mit der eigenen Adresse, Betreff Jahresbericht Facility Management 2025 – Haus Lichtblick, darunter der Anhang Jahresbericht-2025.docx. Rechts fünf Schritte: Bericht speichern, neue E-Mail mit An und Betreff, Einfügen und Datei anfügen, Diesen PC durchsuchen und Datei doppelklicken, Anhang prüfen und senden. Alternative: Datei aus dem Explorer in die E-Mail ziehen."))

# 5 Ablauf mit nebeneinander liegenden Fenstern
b = ""
b += rect(60, 160, 560, 330, "#2E4A6B", INK, 12, 3) + rect(70, 170, 540, 290, "#DCE8F5", rx=6)
b += rect(78, 178, 262, 274, "#FFFFFF", EXCEL, 6, 2) + f'<path d="M78 184 a6 6 0 0 1 6 -6 h250 a6 6 0 0 1 6 6 v20 h-262 z" fill="{EXCEL}"/>' + text(209, 196, "Excel", 15, "bold", "#FFFFFF", "middle")
b += rect(340, 178, 262, 274, "#FFFFFF", WORD, 6, 2) + f'<path d="M340 184 a6 6 0 0 1 6 -6 h250 a6 6 0 0 1 6 6 v20 h-262 z" fill="{WORD}"/>' + text(471, 196, "Word", 15, "bold", "#FFFFFF", "middle")
for k in range(6): b += bar(95, 230 + k * 30, 220 - (k % 2) * 50, LINE, 6) + bar(357, 230 + k * 30, 220 - (k % 3) * 40, LINE, 6)
b += text(340, 525, "Windows-Taste + Pfeil links / rechts", 22, "bold", INK, "middle")
checks = ["Excel und Word nebeneinander", "Tabelle kopieren und einfügen", "Diagramm kopieren und einfügen", "Bericht speichern", "E-Mail mit gutem Betreff", "Bericht anhängen, senden"]
b += text(680, 190, "Der Weg zum Bericht", 26, "bold", INK)
for i, t in enumerate(checks):
    y = 235 + i * 48
    b += rect(680, y - 22, 26, 26, EXCEL, rx=4) + f'<path d="M686 {y-9} l6 6 l10 -12" stroke="#FFFFFF" stroke-width="3" fill="none"/>' + text(722, y, t, 21, fill=INK)
b += rect(60, 560, 1160, 60, SOFTYELLOW, ACCENT, 10, 2) + text(640, 598, "Erst speichern, dann anhängen – sonst geht der alte Stand hinaus.", 22, "bold", INK, "middle")
slides.append(("05-ablauf", "Der ganze Ablauf", b,
  "Links ein Bildschirm mit Excel und Word nebeneinander, angeordnet mit Windows-Taste und Pfeil links oder rechts. Rechts die Schritte zum Bericht: Excel und Word nebeneinander, Tabelle kopieren und einfügen, Diagramm kopieren und einfügen, Bericht speichern, E-Mail mit gutem Betreff, Bericht anhängen und senden. Merksatz: Erst speichern, dann anhängen – sonst geht der alte Stand hinaus."))

for i, (name, title, body, desc) in enumerate(slides, 1):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(frame(i, title, body, desc))
print("ok", len(slides))
