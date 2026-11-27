# Folien Block 10 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-10.py assets/folien/block-10
# Vorschau: magick -density 72 assets/folien/block-10/01-warum-diagramm.svg vorschau.png
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
{text(60,694,"Block 10 · Diagramme erstellen",20,fill=MUTED)}
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

# 1 Warum ein Diagramm?
b = ""
b += rect(60, 150, 330, 470, "#FFFFFF", LINE, 8, 1.5)
b += text(80, 185, "Monat", 17, "bold", INK) + text(370, 185, "Verbrauch (kWh)", 17, "bold", INK, "end")
for i, (m, v) in enumerate(zip(MON, VAL)):
    b += text(80, 218 + i * 33, m, 17, fill=INK) + text(370, 218 + i * 33, f"{v:,}".replace(",", "."), 17, fill=INK, anchor="end")
b += f'<path d="M405 385 h60" stroke="{ACCENT}" stroke-width="6" marker-end="url(#pf)"/>'
b += columns(480, 150, 740, 360, "Stromverbrauch 2025", "kWh", None, hi=[0, 7])
b += rect(480, 530, 740, 90, SOFTYELLOW, ACCENT, 12, 2)
b += text(505, 567, "Die Tabelle sagt, was da ist. Das Diagramm zeigt sofort,", 21, "bold", INK)
b += text(505, 598, "wo es hoch und wo es niedrig ist: Winter hoch, Sommer niedrig.", 21, fill=INK)
slides.append(("01-warum-diagramm", "Warum ein Diagramm?", b,
  "Links die Tabelle mit dem Stromverbrauch 2025 von Januar 4.850 bis Dezember 4.530 kWh, rechts dieselben Werte als Säulendiagramm; der höchste Wert im Januar und der niedrigste im August sind rot hervorgehoben. Aussage: Die Tabelle sagt, was da ist; das Diagramm zeigt sofort, wo es hoch und wo es niedrig ist – Winter hoch, Sommer niedrig."))

# 2 Diagrammtypen
b = ""
cards = [("Säulen", "Werte vergleichen,", "Monate nebeneinander", "Stromverbrauch je Monat"),
         ("Balken", "wie Säulen, liegend –", "gut bei langen Namen", "Fläche je Mieter"),
         ("Linie", "Verlauf über die Zeit", "zeigen", "Zählerstand Jan–Dez"),
         ("Kreis", "Anteile an einem Ganzen", "(höchstens 5–6 Teile)", "Fläche je Etage")]
for i, (h, l1, l2, ex) in enumerate(cards):
    x = 60 + i * 292; w = 272
    b += rect(x, 150, w, 470, "#FFFFFF", LINE, 14, 2)
    b += f'<path d="M{x} 164 a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v50 h-{w} z" fill="{EXCEL}"/>'
    b += text(x + w / 2, 194, h, 26, "bold", "#FFFFFF", "middle")
    cx, cy = x + w / 2, 320
    if i == 0:
        for k, hh in enumerate([90, 70, 110, 50]): b += rect(cx - 80 + k * 42, cy + 60 - hh, 30, hh, EXCEL, rx=2)
    elif i == 1:
        for k, ww in enumerate([150, 110, 170, 80]): b += rect(cx - 90, cy - 55 + k * 30, ww, 22, EXCEL, rx=2)
    elif i == 2:
        b += f'<polyline points="{cx-90},{cy+50} {cx-45},{cy+20} {cx},{cy+5} {cx+45},{cy-25} {cx+90},{cy-50}" fill="none" stroke="{EXCEL}" stroke-width="5"/>'
    else:
        import math
        parts = [750, 570, 760, 300]; tot = sum(parts); a0 = -math.pi / 2; r = 70
        cols = [EXCEL, "#5DA87A", "#A8D5B8", NAVY]
        for k, p in enumerate(parts):
            a1 = a0 + 2 * math.pi * p / tot
            x1, y1 = cx + r * math.cos(a0), cy + r * math.sin(a0); x2, y2 = cx + r * math.cos(a1), cy + r * math.sin(a1)
            b += f'<path d="M{cx} {cy} L{x1:.1f} {y1:.1f} A{r} {r} 0 {1 if a1-a0>math.pi else 0} 1 {x2:.1f} {y2:.1f} z" fill="{cols[k]}" stroke="#FFFFFF" stroke-width="2"/>'
            a0 = a1
    b += text(x + w / 2, 440, l1, 19, fill=INK, anchor="middle") + text(x + w / 2, 466, l2, 19, fill=INK, anchor="middle")
    b += f'<line x1="{x+24}" y1="495" x2="{x+w-24}" y2="495" stroke="{LINE}" stroke-width="2"/>'
    b += text(x + w / 2, 530, "Im Haus Lichtblick", 15, "bold", MUTED, "middle") + text(x + w / 2, 562, ex, 18, fill=EXCEL, anchor="middle")
slides.append(("02-diagrammtypen", "Welches Diagramm wofür?", b,
  "Vier Karten: Säulen vergleichen Werte, etwa den Stromverbrauch je Monat; Balken sind liegende Säulen und gut bei langen Namen, etwa Fläche je Mieter; Linien zeigen einen Verlauf über die Zeit, etwa den Zählerstand; Kreise zeigen Anteile an einem Ganzen mit höchstens fünf bis sechs Teilen, etwa die Fläche je Etage."))

# 3 Diagramm einfügen
b = ""
data = {(1, 1): "Monat", (1, 2): "Verbrauch (kWh)"}
for i in range(6): data[(i + 2, 1)] = ["Januar", "Februar", "März", "April", "Mai", "…"][i]; data[(i + 2, 2)] = ["4.850", "4.670", "4.530", "4.240", "3.890", "…"][i]
b += grid(60, 160, 2, 7, 0, 42, data, colw=[150, 190], bold_row=1, aligns={2: "end"}, size=17)
b += f'<rect x="100" y="202" width="340" height="294" fill="{EXCEL}" fill-opacity="0.15" stroke="{EXCEL}" stroke-width="3"/>'
b += text(60, 540, "1  Überschriften und Zahlen markieren –", 20, "bold", INK) + text(60, 568, "    Monat UND Verbrauch, ohne Summenzeile", 20, fill=INK)
b += rect(520, 160, 700, 200, GREY, LINE, 10, 1.5)
b += text(545, 195, "2  Einfügen → Gruppe „Diagramme“", 20, "bold", INK)
for k in range(4):
    b += rect(545 + k * 70, 215, 56, 50, "#FFFFFF", EXCEL if k == 0 else LINE, 6, 2 if k == 0 else 1.5)
for k, hh in enumerate([18, 30, 24]): b += rect(556 + k * 12, 255 - hh, 8, hh, EXCEL, rx=1)
b += text(545, 300, "Säulen- oder Balkendiagramm einfügen", 17, fill=INK)
b += rect(860, 215, 330, 125, "#FFFFFF", MUTED, 6, 1.5) + text(875, 242, "2D-Säule", 15, "bold", MUTED)
for k in range(3):
    b += rect(875 + k * 70, 255, 56, 50, SOFTX if k == 0 else "#FFFFFF", EXCEL if k == 0 else LINE, 4, 2 if k == 0 else 1)
b += text(875, 328, "3  „Gruppierte Säulen“ anklicken", 17, "bold", INK)
b += columns(520, 385, 700, 235, None, None, None, labels=False)
b += pill(1080, 412, "fertig – jetzt beschriften", EXCEL, 18, "middle")
slides.append(("03-diagramm-einfuegen", "Ein Säulendiagramm einfügen", b,
  "Links eine Tabelle mit Monat und Verbrauch; Überschriften und Zahlen sind markiert. Rechts Schritt 2: Einfügen, Gruppe Diagramme, Säulen- oder Balkendiagramm einfügen, und Schritt 3: unter 2D-Säule „Gruppierte Säulen“ anklicken. Darunter das fertige Säulendiagramm, das jetzt beschriftet wird."))

# 4 Beschriften
b = ""
b += columns(60, 150, 760, 470, "Stromverbrauch Haus Lichtblick 2025", "Verbrauch in kWh", "Monat")
b += rect(830, 170, 36, 36, "#FFFFFF", EXCEL, 4, 2) + text(848, 196, "+", 26, "bold", EXCEL, "middle")
b += rect(830, 215, 36, 36, "#FFFFFF", LINE, 4, 1.5) + f'<path d="M840 240 l8 -14 l8 14" fill="none" stroke="{MUTED}" stroke-width="2.5"/>'
b += pill(440, 140, "Diagrammtitel: anklicken, überschreiben", ACCENT, 15, "middle")
b += text(900, 190, "Diagrammelemente (+)", 20, "bold", INK)
for k, (t, on) in enumerate([("Achsen", True), ("Achsentitel", True), ("Diagrammtitel", True), ("Datenbeschriftungen", False), ("Gitternetzlinien", True), ("Legende", False)]):
    y = 225 + k * 34
    b += rect(900, y - 16, 18, 18, EXCEL if on else "#FFFFFF", EXCEL if on else MUTED, 3, 2)
    if on: b += f'<path d="M903 {y-7} l4 4 l8 -9" stroke="#FFFFFF" stroke-width="2.5" fill="none"/>'
    b += text(928, y, t, 18, "bold" if t == "Achsentitel" else "normal", INK)
b += rect(880, 450, 340, 170, SOFTX, EXCEL, 12, 2)
b += text(900, 485, "Oder im Menüband:", 18, "bold", INK)
b += text(900, 515, "„Diagrammentwurf“ →", 18, fill=INK)
b += text(900, 541, "„Diagrammelement hinzufügen“", 18, fill=INK)
b += text(900, 567, "→ „Achsentitel“", 18, fill=INK)
b += text(900, 600, "Erscheint nur, wenn das Diagramm markiert ist.", 14, fill=MUTED)
slides.append(("04-beschriften", "Titel und Achsentitel", b,
  "Ein Säulendiagramm mit dem Titel Stromverbrauch Haus Lichtblick 2025, der senkrechten Achsenbeschriftung Verbrauch in kWh und der waagerechten Achsenbeschriftung Monat. Rechts daneben die Schaltfläche Plus für Diagrammelemente mit Häkchen bei Achsen, Achsentitel, Diagrammtitel und Gitternetzlinien. Alternativ im Menüband: Diagrammentwurf, Diagrammelement hinzufügen, Achsentitel – erscheint nur, wenn das Diagramm markiert ist."))

# 5 Verschieben, Größe, Drucken
b = ""
b += rect(80, 180, 420, 280, "#FFFFFF", EXCEL, 4, 2)
for (cx, cy) in [(80, 180), (290, 180), (500, 180), (80, 320), (500, 320), (80, 460), (290, 460), (500, 460)]:
    b += f'<circle cx="{cx}" cy="{cy}" r="7" fill="#FFFFFF" stroke="{EXCEL}" stroke-width="2.5"/>'
b += columns(110, 210, 360, 220, None, None, None, labels=False)
b += text(520, 478, "Ecke ziehen: Größe", 19, "bold", INK)
b += f'<path d="M290 175 v-25 M290 150 l-8 10 M290 150 l8 10" stroke="{ACCENT}" stroke-width="4" fill="none"/>' + text(310, 158, "Rand ziehen: verschieben", 19, "bold", INK)
b += rect(700, 160, 520, 300, GREY, LINE, 10, 1.5)
b += text(725, 200, "Drucken: Diagramm anklicken, dann Strg+P", 20, "bold", INK)
b += rect(725, 222, 470, 40, "#FFFFFF", EXCEL, 6, 2) + text(740, 249, "Ausgewähltes Diagramm drucken", 18, "bold", INK)
b += rect(1020, 280, 170, 160, "#FFFFFF", MUTED, 3, 1.5)
b += columns(1030, 300, 150, 110, None, None, None, labels=False)
b += text(745, 320, "Vorschau: nur das", 18, fill=INK) + text(745, 346, "Diagramm, auf einer", 18, fill=INK) + text(745, 372, "ganzen Seite", 18, fill=INK)
b += rect(60, 500, 1160, 120, SOFTYELLOW, ACCENT, 12, 2)
b += text(90, 540, "Einmal klicken markiert das Diagramm. Doppelklick öffnet den Bereich zum Formatieren –", 20, "bold", INK)
b += text(90, 570, "dann Esc drücken und neu klicken.", 20, "bold", INK)
b += text(90, 602, "Ändern Sie eine Zahl in der Tabelle, ändert sich das Diagramm sofort mit.", 19, fill=INK)
slides.append(("05-verschieben-drucken", "Verschieben, Größe ändern, drucken", b,
  "Links ein markiertes Diagramm mit acht Anfassern: am Rand ziehen verschiebt es, an einer Ecke ziehen ändert die Größe. Rechts das Drucken: Diagramm anklicken, Strg+P, Einstellung „Ausgewähltes Diagramm drucken“, die Vorschau zeigt nur das Diagramm auf einer ganzen Seite. Hinweis: Einmal klicken markiert, Doppelklick öffnet den Bereich zum Formatieren; ändert sich eine Zahl in der Tabelle, ändert sich das Diagramm mit."))

for i, (name, title, body, desc) in enumerate(slides, 1):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(frame(i, title, body, desc))
print("ok", len(slides))
