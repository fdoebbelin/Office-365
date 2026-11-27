# Folien Block 05 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-05.py assets/folien/block-05
# Vorschau: magick -density 72 assets/folien/block-05/01-listen.svg vorschau.png
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
{text(60,694,"Block 05 · Vorlagen und Struktur",20,fill=MUTED)}
{text(W-60,694,"Haus Lichtblick – Microsoft 365  ·  Folie "+str(nr),20,fill=MUTED,anchor="end")}
</svg>
'''

slides = []
def bulleticon(x, y, col=WORD, num=False):
    s = rect(x, y, 44, 40, "#FFFFFF", LINE, 6, 1.5)
    for k in range(3):
        yy = y + 10 + k * 10
        s += (text(x + 10, yy + 4, str(k + 1), 9, "bold", col, "middle") if num else f'<circle cx="{x+10}" cy="{yy}" r="2.5" fill="{col}"/>')
        s += f'<line x1="{x+17}" y1="{yy}" x2="{x+36}" y2="{yy}" stroke="{MUTED}" stroke-width="2"/>'
    return s

# 1 Listen
b = ""
for i, (head, sub, num, items, col, soft) in enumerate([
        ("Aufzählung", "wie eine Einkaufsliste – Reihenfolge egal", False, ["Elektro", "Sanitär", "Heizung", "Brandschutz"], WORD, SOFTBLUE),
        ("Nummerierung", "wie ein Kochrezept – Reihenfolge zählt", True, ["Fluchtwege frei und beleuchtet", "Feuerlöscher vorhanden und geprüft", "Notbeleuchtung funktionsfähig", "Rauchmelder getestet"], EXCEL, SOFTGREEN)]):
    x = 60 + i * 590; w = 570
    b += rect(x, 145, w, 340, soft, col, 14, 2)
    b += bulleticon(x + 30, 170, col, num)
    b += text(x + 92, 198, head, 30, "bold", col)
    b += text(x + 30, 245, sub, 20, fill=MUTED, italic=True)
    b += rect(x + 30, 265, w - 60, 195, "#FFFFFF", LINE, 8, 1.5)
    for k, t in enumerate(items):
        y = 305 + k * 42
        b += (text(x + 60, y, f"{k+1}.", 22, "bold", col, "end") if num else f'<circle cx="{x+55}" cy="{y-7}" r="5" fill="{col}"/>')
        b += text(x + 75, y, t, 22, fill=INK)
b += rect(60, 505, 1160, 120, SOFTYELLOW, ACCENT, 12, 2)
b += text(90, 545, "So geht's: Start → Gruppe „Absatz“ → Aufzählungszeichen oder Nummerierung", 23, "bold", INK)
b += text(90, 580, "Enter macht den nächsten Punkt. Liste beenden: zweimal Enter.", 21, fill=INK)
b += text(90, 610, "Schon geschriebene Zeilen? Erst markieren, dann auf das Symbol klicken.", 21, fill=INK)
slides.append(("01-listen", "Aufzählung und Nummerierung", b,
  "Links eine Aufzählung mit Punkten – wie eine Einkaufsliste, die Reihenfolge ist egal: Elektro, Sanitär, Heizung, Brandschutz. Rechts eine nummerierte Liste – wie ein Kochrezept, die Reihenfolge zählt: die ersten vier Punkte der Checkliste Sicherheitsbegehung. Unten: Start, Gruppe Absatz, Aufzählungszeichen oder Nummerierung; Enter macht den nächsten Punkt, zweimal Enter beendet die Liste."))

# 2 Überschriften
b = ""
b += text(60, 170, "Start → Gruppe „Formatvorlagen“", 24, "bold", INK)
styles = [("Standard", 15, "normal"), ("Kein Leerraum", 15, "normal"), ("Überschrift 1", 17, "bold"), ("Überschrift 2", 15, "bold"), ("Titel", 20, "normal")]
for i, (n, sz, wt) in enumerate(styles):
    x = 60 + i * 150
    hl = n.startswith("Überschrift")
    b += rect(x, 190, 140, 70, SOFTBLUE if hl else "#FFFFFF", WORD if hl else LINE, 6, 2 if hl else 1.5)
    b += text(x + 70, 222, "AaBbCc", sz, wt, NAVY if hl else INK, "middle") + text(x + 70, 248, n, 13, fill=MUTED, anchor="middle")
# Navigationsbereich + Seite
b += rect(60, 300, 330, 325, GREY, LINE, 8, 1.5)
b += text(80, 335, "Navigationsbereich", 20, "bold", INK)
for i, (t, lvl) in enumerate([("Wartungsprotokoll Haus Lichtblick", 0), ("Durchgeführte Arbeiten", 1), ("Betroffene Gewerke", 1), ("Hinweise", 1)]):
    y = 380 + i * 50
    if i == 1: b += rect(70 + lvl * 20, y - 26, 310 - lvl * 20, 38, SOFTBLUE, rx=6)
    b += text(85 + lvl * 24, y, t, 18 if lvl else 16, "bold" if lvl == 0 else "normal", INK)
b += rect(420, 300, 520, 325, "#FFFFFF", MUTED, 4, 2)
b += text(450, 350, "Wartungsprotokoll Haus Lichtblick", 24, "bold", NAVY)
b += bar(450, 380, 300) + text(450, 425, "Durchgeführte Arbeiten", 20, "bold", NAVY)
b += rect(450, 440, 460, 70, "#FFFFFF", LINE, 2, 1.5)
for k in range(1, 4): b += f'<line x1="{450+k*115}" y1="440" x2="{450+k*115}" y2="510" stroke="{LINE}" stroke-width="1.5"/>'
b += text(450, 550, "Betroffene Gewerke", 20, "bold", NAVY) + bar(450, 580, 250) + bar(450, 605, 200)
b += pill(1080, 360, "Überschrift 1", WORD, 18, "middle") + f'<path d="M985 352 h-30" stroke="{ACCENT}" stroke-width="4" marker-end="url(#pf)"/>'
b += pill(1080, 435, "Überschrift 2", WORD, 18, "middle") + f'<path d="M985 427 h-30" stroke="{ACCENT}" stroke-width="4" marker-end="url(#pf)"/>'
b += rect(970, 480, 250, 145, SOFTYELLOW, ACCENT, 12, 2)
for k, t in enumerate(["Wie Kapitel im Buch:", "Ein Klick im", "Navigationsbereich", "springt dorthin."]):
    b += text(990, 515 + k * 30, t, 19, "bold" if k == 0 else "normal", INK)
slides.append(("02-ueberschriften", "Überschriften mit Formatvorlagen", b,
  "Oben der Katalog der Formatvorlagen auf der Registerkarte Start mit Standard, Kein Leerraum, Überschrift 1, Überschrift 2 und Titel. Darunter links der Navigationsbereich mit der Gliederung des Wartungsprotokolls, rechts die Seite: Wartungsprotokoll Haus Lichtblick als Überschrift 1, Durchgeführte Arbeiten und Betroffene Gewerke als Überschrift 2. Hinweis: wie Kapitel im Buch; ein Klick im Navigationsbereich springt dorthin."))

# 3 Tabelle einfügen
b = text(60, 170, "Einfügen → Tabelle → Kästchen ziehen: 5 Spalten × 5 Zeilen", 26, "bold", INK)
gx, gy, c = 80, 210, 34
for r in range(8):
    for k in range(10):
        on = r < 5 and k < 5
        b += rect(gx + k * (c + 4), gy + r * (c + 4), c, c, SOFTBLUE if on else "#FFFFFF", WORD if on else LINE, 3, 2 if on else 1.2)
b += text(gx + 5 * (c + 4) / 2, gy + 8 * (c + 4) + 26, "5 × 5 markiert", 20, "bold", WORD, "middle")
tx, ty = 560, 210
head = ["Datum", "Gewerk", "Befund", "Maßnahme", "Erledigt"]
ws = [110, 110, 170, 170, 90]
x = tx
for k, h in enumerate(head):
    b += rect(x, ty, ws[k], 44, SOFTBLUE, LINE, 0, 1.5) + text(x + 10, ty + 29, h, 17, "bold", INK)
    for r in range(1, 5): b += rect(x, ty + r * 44, ws[k], 44, "#FFFFFF", LINE, 0, 1.5)
    x += ws[k]
b += text(tx + 10, ty + 44 + 29, "15.04.2025", 16, fill=INK) + text(tx + 120, ty + 44 + 29, "Elektro", 16, fill=INK)
b += f'<line x1="{tx+232}" y1="{ty+52}" x2="{tx+232}" y2="{ty+80}" stroke="{INK}" stroke-width="2"/>'
b += f'<path d="M{tx+180} {ty+120} q30 30 60 0" fill="none" stroke="{ACCENT}" stroke-width="4" marker-end="url(#pf)"/>'
b += rect(tx, 470, 650, 150, SOFTYELLOW, ACCENT, 12, 2)
b += text(tx + 25, 510, "Tab", 24, "bold", WORD) + text(tx + 110, 510, "springt in die nächste Zelle", 22, fill=INK)
b += text(tx + 25, 548, "Umschalt+Tab", 24, "bold", WORD) + text(tx + 210, 548, "eine Zelle zurück", 22, fill=INK)
b += text(tx + 25, 590, "Tab in der letzten Zelle: neue Zeile", 22, "bold", INK)
b += rect(60, 565, 440, 60, SOFTGREEN, EXCEL, 12, 2) + text(280, 602, "Tabellen in Word: zum Ordnen, nicht zum Rechnen", 17, "bold", INK, "middle")
slides.append(("03-tabelle-einfuegen", "Eine Tabelle einfügen und ausfüllen", b,
  "Links das Raster aus dem Menü Einfügen, Tabelle: fünf mal fünf Kästchen sind markiert. Rechts die eingefügte Tabelle für das Wartungsprotokoll mit den Spalten Datum, Gewerk, Befund, Maßnahme, Erledigt, erste Zeile 15.04.2025, Elektro. Hinweise: Tab springt in die nächste Zelle, Umschalt+Tab zurück, Tab in der letzten Zelle fügt eine neue Zeile an. Tabellen in Word sind zum Ordnen, nicht zum Rechnen."))

# 4 Tabelle bearbeiten
b = ""
cards = [("Spaltenbreite", "Maus auf die Trennlinie –", "Doppelpfeil, dann ziehen", WORD),
         ("Zeile löschen", "Schreibmarke in die Zeile,", "„Layout“ → „Löschen“", BAD),
         ("Tabellenformat", "„Tabellenentwurf“ →", "Formatvorlage anklicken", EXCEL)]
for i, (h, l1, l2, col) in enumerate(cards):
    x = 60 + i * 395; w = 370
    b += rect(x, 150, w, 420, "#FFFFFF", LINE, 14, 2)
    b += f'<path d="M{x} 164 a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v62 h-{w} z" fill="{col}"/>'
    b += text(x + w / 2, 200, h, 30, "bold", "#FFFFFF", "middle")
    # mini table
    mx, my = x + 45, 260
    for r in range(4):
        for k in range(3):
            fill = "#FFFFFF"
            if i == 2 and r == 0: fill = EXCEL
            elif i == 2 and r % 2 == 0: fill = SOFTGREEN
            if i == 1 and r == 2: fill = SOFTRED
            b += rect(mx + k * 93, my + r * 40, 93, 40, fill, LINE, 0, 1.5)
    if i == 0:
        b += f'<line x1="{mx+93}" y1="{my-10}" x2="{mx+93}" y2="{my+170}" stroke="{WORD}" stroke-width="4"/>'
        b += f'<path d="M{mx+60} {my+190} h-12 l8 -6 m-8 6 l8 6 M{mx+126} {my+190} h12 l-8 -6 m8 6 l-8 6" stroke="{WORD}" stroke-width="3" fill="none"/>'
    if i == 1:
        b += f'<line x1="{mx+10}" y1="{my+100}" x2="{mx+269}" y2="{my+100}" stroke="{BAD}" stroke-width="3"/>'
    b += text(x + w / 2, 500, l1, 22, fill=INK, anchor="middle") + text(x + w / 2, 534, l2, 22, "bold", INK, "middle")
b += text(640, 610, "Die Registerkarten „Tabellenentwurf“ und „Layout“ (rechts) erscheinen nur, wenn die Schreibmarke in der Tabelle steht.", 18, fill=MUTED, anchor="middle")
slides.append(("04-tabelle-bearbeiten", "Tabellen bearbeiten", b,
  "Drei Karten: Spaltenbreite ändern – Maus auf die Trennlinie, bis ein Doppelpfeil erscheint, dann ziehen. Zeile löschen – Schreibmarke in die Zeile, Layout, Löschen. Tabellenformat – Tabellenentwurf, Formatvorlage anklicken. Hinweis: Die Registerkarten Tabellenentwurf und Layout erscheinen nur, wenn die Schreibmarke in der Tabelle steht."))

# 5 Seitenränder und Druckvorschau
b = ""
for i, (n, m, col) in enumerate([("Normal", 46, WORD), ("Schmal", 22, EXCEL)]):
    x = 90 + i * 300
    b += rect(x, 180, 220, 300, "#FFFFFF", MUTED, 4, 2)
    b += rect(x + m, 180 + m, 220 - 2 * m, 300 - 2 * m, "none", col, 0, 2)
    for k in range(8): b += bar(x + m + 10, 180 + m + 18 + k * 26, 220 - 2 * m - 20 - (k % 3) * 20, LINE, 5)
    b += text(x + 110, 520, n, 26, "bold", col, "middle")
b += text(390, 560, "Schmal = 1,27 cm rundum – mehr Platz für Tabellen", 20, fill=INK, anchor="middle")
b += text(390, 170, "Layout → Seitenränder", 24, "bold", INK, "middle")
b += rect(720, 160, 500, 460, GREY, LINE, 12, 2)
b += text(745, 200, "Datei → Drucken (Strg+P)", 24, "bold", INK)
b += rect(745, 225, 170, 50, WORD, rx=8) + text(830, 257, "Drucken", 20, "bold", "#FFFFFF", "middle")
for k, t in enumerate(["Drucker", "Seiten", "Hochformat", "A4", "Seitenränder"]):
    b += rect(745, 295 + k * 50, 170, 38, "#FFFFFF", LINE, 6, 1.5) + text(757, 320 + k * 50, t, 16, fill=INK)
b += rect(950, 225, 240, 340, "#FFFFFF", MUTED, 4, 2)
b += text(1070, 265, "Vorschau", 18, "bold", MUTED, "middle")
for k in range(9): b += bar(975, 300 + k * 26, 180 - (k % 3) * 40, LINE, 5)
b += text(745, 600, "Erst Vorschau, dann Papier.", 20, "bold", INK)
slides.append(("05-seitenraender-drucken", "Seitenränder und Druckvorschau", b,
  "Links zwei Seiten: mit normalen Seitenrändern und mit schmalen Rändern von 1,27 cm rundum, die mehr Platz für Tabellen lassen – einzustellen unter Layout, Seitenränder. Rechts die Ansicht Datei, Drucken mit der Schaltfläche Drucken, den Einstellungen Drucker, Seiten, Hochformat, A4, Seitenränder und rechts der Vorschau. Merksatz: erst Vorschau, dann Papier."))

for i, (name, title, body, desc) in enumerate(slides, 1):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(frame(i, title, body, desc))
print("ok", len(slides))
