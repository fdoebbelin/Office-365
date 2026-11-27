# Folien Block 09 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-09.py assets/folien/block-09
# Vorschau: magick -density 72 assets/folien/block-09/01-ausfuellen.svg vorschau.png
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
{text(60,694,"Block 09 · Rechnen und Auswerten",20,fill=MUTED)}
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

# 1 Ausfüllen und relative Bezüge
b = ""
data = {(1, 1): "Monat", (1, 2): "Zählerstand", (1, 3): "Verbrauch", (2, 1): "Januar", (2, 2): "125.450", (2, 3): "4.850",
        (3, 1): "Februar", (3, 2): "130.120", (3, 3): "=B3-B2", (4, 1): "März", (4, 2): "134.650", (4, 3): "=B4-B3",
        (5, 1): "April", (5, 2): "138.890", (5, 3): "=B5-B4", (6, 1): "Mai", (6, 2): "142.780", (6, 3): "=B6-B5"}
b += grid(60, 160, 3, 6, 0, 50, data, (3, 3), colw=[150, 170, 160], bold_row=1, aligns={2: "end", 3: "end"}, size=20)
b += f'<rect x="420" y="{160+4*50}" width="160" height="150" fill="{EXCEL}" fill-opacity="0.10"/>'
b += f'<path d="M585 {160+4*50-6} v150" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
b += text(650, 190, "Ausfüllkästchen", 30, "bold", EXCEL)
b += text(650, 228, "das kleine Quadrat unten rechts an der Zelle", 21, fill=INK)
for i, t in enumerate(["Zelle mit der Formel anklicken", "Maus auf das Quadrat: dünnes schwarzes Kreuz", "mit gedrückter Maustaste nach unten ziehen", "oder: doppelklicken – Excel füllt bis zum Listenende"]):
    b += f'<circle cx="672" cy="{278+i*42}" r="16" fill="{EXCEL}"/>' + text(672, 285 + i * 42, str(i + 1), 18, "bold", "#FFFFFF", "middle") + text(700, 286 + i * 42, t, 20, fill=INK)
b += rect(60, 525, 1160, 100, SOFTYELLOW, ACCENT, 12, 2)
b += text(90, 563, "Excel denkt in Richtungen: „Zählerstand dieser Zeile minus Zählerstand eine Zeile darüber“.", 21, "bold", INK)
b += text(90, 597, "Beim Kopieren passt Excel die Adressen an: aus =B3-B2 wird =B4-B3, =B5-B4 …", 21, fill=INK)
slides.append(("01-ausfuellen", "Formeln nach unten ausfüllen", b,
  "Eine Liste mit Monat, Zählerstand und Verbrauch. In C3 steht =B3-B2; mit dem Ausfüllkästchen – dem kleinen Quadrat unten rechts an der Zelle – wird die Formel nach unten gezogen, und Excel passt die Adressen an: =B4-B3, =B5-B4, =B6-B5. Schritte: Zelle anklicken, Maus auf das Quadrat, nach unten ziehen oder doppelklicken."))

# 2 Funktionen
b = text(60, 175, "Aufbau:  =SUMME(C4:C15)", 30, "bold", INK)
b += text(470, 210, "Bereich: von C4 bis C15 – der Doppelpunkt heißt „bis“", 20, fill=MUTED)
rows = [("SUMME", "alles zusammenzählen", "wie der Kassenzettel", "47.850 kWh"),
        ("MITTELWERT", "Durchschnitt", "Was verbrauchen wir normalerweise?", "3.987,5 kWh"),
        ("MIN", "kleinster Wert", "der sparsamste Monat", "3.240 kWh"),
        ("MAX", "größter Wert", "der teuerste Monat", "4.850 kWh"),
        ("ANZAHL", "Zellen mit Zahlen zählen", "Wie viele Monate sind erfasst?", "12")]
for i, (fn, was, vgl, erg) in enumerate(rows):
    y = 240 + i * 76
    b += rect(60, y, 1160, 64, SOFTX if i % 2 == 0 else "#FFFFFF", LINE, 8, 1.5)
    b += text(85, y + 41, fn, 26, "bold", EXCEL) + text(330, y + 41, was, 22, fill=INK) + text(640, y + 41, vgl, 20, fill=MUTED, italic=True)
    b += text(1195, y + 41, erg, 22, "bold", INK, "end")
slides.append(("02-funktionen", "SUMME, MITTELWERT, MIN, MAX, ANZAHL", b,
  "Aufbau einer Funktion: =SUMME(C4:C15), der Bereich reicht von C4 bis C15, der Doppelpunkt heißt bis. Fünf Funktionen mit Ergebnis für den Stromverbrauch 2025: SUMME zählt alles zusammen, 47.850 kWh; MITTELWERT ist der Durchschnitt, 3.987,5 kWh; MIN der kleinste Wert, 3.240 kWh; MAX der größte, 4.850 kWh; ANZAHL zählt die Zellen mit Zahlen, 12."))

# 3 AutoSumme
b = ""
b += rect(60, 160, 360, 120, GREY, LINE, 10, 1.5)
b += rect(90, 185, 70, 70, "#FFFFFF", EXCEL, 8, 2) + text(125, 236, "Σ", 44, "bold", EXCEL, "middle")
b += text(180, 215, "AutoSumme", 24, "bold", INK) + text(180, 245, "Start oder Formeln", 18, fill=MUTED)
b += rect(205, 262, 26, 16, "#FFFFFF", LINE, 3, 1) + text(218, 275, "▾", 12, fill=MUTED, anchor="middle")
b += text(60, 330, "Der kleine Pfeil daneben: Mittelwert, Anzahl,", 20, fill=INK) + text(60, 358, "Max, Min", 20, fill=INK)
data = {(1, 1): "Monat", (1, 2): "Verbrauch", (2, 1): "Oktober", (2, 2): "3.650", (3, 1): "November", (3, 2): "4.030", (4, 1): "Dezember", (4, 2): "4.530", (5, 1): "Summe", (5, 2): "=SUMME(B2:B4)"}
b += grid(520, 160, 2, 5, 0, 50, data, (5, 2), colw=[170, 210], bold_row=1, aligns={2: "end"}, size=20)
b += f'<rect x="732" y="260" width="208" height="150" fill="none" stroke="{OUTLOOK}" stroke-width="3" stroke-dasharray="8 6"/>'
steps = ["Zelle unter der Zahlenreihe anklicken", "Σ AutoSumme klicken", "Excel schlägt den Bereich vor (gestrichelt)", "Bereich prüfen, Enter"]
for i, t in enumerate(steps):
    y = 470 + i * 40
    b += f'<circle cx="80" cy="{y-7}" r="15" fill="{EXCEL}"/>' + text(80, y, str(i + 1), 17, "bold", "#FFFFFF", "middle") + text(108, y, t, 21, fill=INK)
b += rect(700, 470, 520, 150, SOFTYELLOW, ACCENT, 12, 2)
b += text(725, 510, "Falscher Bereich?", 22, "bold", INK)
b += text(725, 545, "Vor dem Enter mit der Maus", 20, fill=INK) + text(725, 575, "den richtigen Bereich markieren.", 20, fill=INK)
slides.append(("03-autosumme", "Schneller mit AutoSumme", b,
  "Die Schaltfläche AutoSumme mit dem Summenzeichen auf den Registerkarten Start und Formeln; der kleine Pfeil daneben bietet Mittelwert, Anzahl, Max und Min. Beispiel: Unter dem Verbrauch von Oktober bis Dezember schlägt Excel =SUMME(B2:B4) vor und umrahmt den Bereich gestrichelt. Schritte: Zelle unter der Zahlenreihe anklicken, AutoSumme klicken, Bereich prüfen, Enter."))

# 4 Zahlenformate
b = text(60, 175, "Das Format ändert nur die Anzeige – der Wert bleibt gleich.", 26, "bold", INK)
ex = [("Standard", "7140", "Währung", "7.140,00 €"), ("Standard", "47850", "Zahl mit 1.000er-Trennzeichen", "47.850"), ("Standard", "45762", "Datum, kurz", "15.04.2025")]
for i, (a, v, bname, w) in enumerate(ex):
    y = 215 + i * 105
    b += rect(60, y, 300, 80, "#FFFFFF", LINE, 8, 1.5) + text(80, y + 30, a, 17, fill=MUTED) + text(340, y + 62, v, 28, "bold", INK, "end")
    b += f'<path d="M375 {y+40} h70" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
    b += rect(460, y, 420, 80, SOFTX, EXCEL, 8, 2) + text(480, y + 30, bname, 17, fill=MUTED) + text(860, y + 62, w, 28, "bold", EXCEL, "end")
b += rect(920, 215, 300, 290, GREY, LINE, 10, 1.5)
b += text(945, 255, "Start → Gruppe „Zahl“", 20, "bold", INK)
b += rect(945, 275, 250, 36, "#FFFFFF", LINE, 4, 1.5) + text(957, 299, "Standard", 17, fill=INK) + text(1182, 299, "▾", 15, fill=MUTED, anchor="end")
for k, t in enumerate(["Zahl", "Währung", "Datum, kurz", "Prozent"]):
    b += text(957, 340 + k * 34, t, 17, "bold" if t == "Währung" else "normal", INK)
b += rect(945, 465, 36, 30, "#FFFFFF", LINE, 4, 1.5) + text(963, 486, "000", 12, "bold", INK, "middle") + text(990, 487, "1.000er-Trennzeichen", 16, fill=INK)
b += rect(60, 540, 1160, 85, SOFTYELLOW, ACCENT, 12, 2)
b += text(90, 578, "Zellen markieren, dann Format wählen.", 22, "bold", INK)
b += text(90, 608, "Ein Datum ist für Excel eine Zahl – deshalb kann Excel damit rechnen.", 20, fill=INK)
slides.append(("04-zahlenformat", "Zahlen formatieren", b,
  "Drei Beispiele: 7140 wird im Format Währung zu 7.140,00 €, 47850 mit 1.000er-Trennzeichen zu 47.850, die Zahl 45762 im Format Datum kurz zu 15.04.2025. Rechts die Auswahl auf der Registerkarte Start in der Gruppe Zahl mit Standard, Zahl, Währung, Datum kurz, Prozent und der Schaltfläche 1.000er-Trennzeichen. Merksatz: Das Format ändert nur die Anzeige, der Wert bleibt gleich."))

# 5 Sortieren und Filtern
b = ""
data = {(1, 1): "Artikel ▾", (1, 2): "Bestand ▾", (1, 3): "Nachbestellen ▾", (2, 1): "Glasreiniger", (2, 2): "8", (2, 3): "Ja", (3, 1): "Einweghandschuhe", (3, 2): "5", (3, 3): "Ja"}
b += grid(60, 160, 3, 3, 0, 50, data, colw=[200, 110, 170], bold_row=1, aligns={2: "end"}, size=18, rowlabels=[3, 8, 12])
b += text(60, 400, "Die Zeilennummern springen (3, 8, 12):", 19, fill=INK) + text(60, 428, "Die übrigen Zeilen sind nur ausgeblendet,", 19, fill=INK) + text(60, 456, "nicht gelöscht.", 19, "bold", INK)
# Filtermenü
mx, my = 600, 160
b += rect(mx, my, 290, 250, "#FFFFFF", MUTED, 6, 2)
for k, t in enumerate(["Nach Größe sortieren (aufsteigend)", "Nach Größe sortieren (absteigend)"]):
    b += text(mx + 16, my + 30 + k * 30, t, 15, fill=INK)
b += f'<line x1="{mx+10}" y1="{my+80}" x2="{mx+280}" y2="{my+80}" stroke="{LINE}" stroke-width="1.5"/>'
for k, (t, on) in enumerate([("(Alle auswählen)", False), ("Ja", True), ("Nein", False)]):
    y = my + 115 + k * 36
    b += rect(mx + 16, y - 16, 20, 20, EXCEL if on else "#FFFFFF", EXCEL if on else MUTED, 3, 2)
    if on: b += f'<path d="M{mx+20} {y-6} l5 5 l9 -10" stroke="#FFFFFF" stroke-width="3" fill="none"/>'
    b += text(mx + 46, y, t, 17, fill=INK)
b += rect(mx + 170, my + 210, 100, 30, EXCEL, rx=5) + text(mx + 220, my + 231, "OK", 16, "bold", "#FFFFFF", "middle")
steps = [("Sortieren", "Zelle in der Spalte anklicken → Daten → Sortieren"), ("Filtern", "Daten → Filtern: Pfeile in der Kopfzeile"), ("Filter aufheben", "Daten → Filtern noch einmal klicken")]
for i, (h, t) in enumerate(steps):
    y = 185 + i * 100
    b += text(920, y, h, 22, "bold", EXCEL) + text(920, y + 28, t.split(" → ", 1)[0], 17, fill=INK) + (text(920, y + 52, "→ " + t.split(" → ", 1)[1], 17, fill=INK) if " → " in t else "")
b += rect(60, 500, 1160, 120, SOFTYELLOW, ACCENT, 12, 2)
b += text(90, 540, "Sortieren ändert die Reihenfolge, Filtern blendet Zeilen aus.", 23, "bold", INK)
b += text(90, 575, "Vor dem Sortieren nur EINE Zelle der Spalte anklicken, nicht die Spalte markieren.", 20, fill=INK)
b += text(90, 603, "Excel erkennt die ganze Liste von selbst – so bleiben die Zeilen zusammen.", 20, fill=INK)
slides.append(("05-sortieren-filtern", "Sortieren und Filtern", b,
  "Links die gefilterte Inventarliste: nur Glasreiniger und Einweghandschuhe mit Nachbestellen Ja sind zu sehen, die Zeilennummern springen – die übrigen Zeilen sind nur ausgeblendet. In der Mitte das Filtermenü einer Spalte mit Sortierbefehlen und Häkchen für (Alle auswählen), Ja und Nein. Rechts: Sortieren über Daten, Sortieren; Filtern über Daten, Filtern; Filter aufheben durch erneuten Klick. Hinweis: vor dem Sortieren nur eine Zelle anklicken, Excel erkennt die ganze Liste, so bleiben die Zeilen zusammen."))

for i, (name, title, body, desc) in enumerate(slides, 1):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(frame(i, title, body, desc))
print("ok", len(slides))
