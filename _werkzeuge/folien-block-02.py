# Folien Block 02 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-02.py assets/folien/block-02
# Vorschau: magick -density 72 assets/folien/block-02/01-outlook-oberflaeche.svg vorschau.png
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
{text(60,694,"Block 02 · E-Mail-Grundlagen",20,fill=MUTED)}
{text(W-60,694,"Haus Lichtblick – Microsoft 365  ·  Folie "+str(nr),20,fill=MUTED,anchor="end")}
</svg>
'''

slides = []

# 1 Outlook-Oberfläche
b = ""
x0, y0, x1, y1 = 60, 140, 1220, 630
b += rect(x0, y0, x1 - x0, y1 - y0, "#FFFFFF", INK, 10, 3)
b += f'<path d="M{x0} {y0+10} a10 10 0 0 1 10 -10 h{x1-x0-20} a10 10 0 0 1 10 10 v26 h-{x1-x0} z" fill="{OUTLOOK}"/>'
b += rect(470, y0 + 7, 340, 22, "#FFFFFF", rx=6) + text(484, y0 + 24, "Suchen", 15, fill=MUTED)
# Menüband
b += rect(x0 + 2, y0 + 36, x1 - x0 - 4, 58, GREY, rx=0)
for i, t in enumerate(["Start", "Ansicht", "Hilfe"]):
    b += text(x0 + 90 + i * 90, y0 + 58, t, 16, "bold" if i == 0 else "normal", OUTLOOK if i == 0 else MUTED)
b += f'<line x1="{x0+80}" y1="{y0+64}" x2="{x0+130}" y2="{y0+64}" stroke="{OUTLOOK}" stroke-width="3"/>'
b += rect(x0 + 80, y0 + 68, 120, 22, OUTLOOK, rx=5) + text(x0 + 140, y0 + 84, "Neue E-Mail", 14, "bold", "#FFFFFF", "middle")
for i in range(6):
    b += rect(x0 + 220 + i * 60, y0 + 70, 44, 18, "#FFFFFF", LINE, 4, 1.5)
b += pill(1010, y0 + 80, "Menüband", NAVY, 20)
# App-Leiste
top = y0 + 94
b += rect(x0 + 2, top, 64, y1 - top - 2, "#E4E8EE", rx=0)
for i, col in enumerate([OUTLOOK, MUTED, MUTED, MUTED]):
    b += rect(x0 + 18, top + 22 + i * 56, 32, 32, col if i == 0 else "#FFFFFF", col, 6, 2)
b += f'<path d="M{x0+22} {top+30} l12 9 l12 -9" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>'
b += text(x0 + 40, 545, "App-Leiste", 20, "bold", NAVY, "middle", rotate=-90)
# Ordnerbereich
fx = x0 + 66
b += rect(fx, top, 230, y1 - top - 2, "#FAFBFC", rx=0)
b += f'<line x1="{fx+230}" y1="{top}" x2="{fx+230}" y2="{y1}" stroke="{LINE}" stroke-width="2"/>'
for i, t in enumerate(["Posteingang", "Entwürfe", "Gesendete Elemente", "Gelöschte Elemente", "Archiv"]):
    yy = top + 40 + i * 40
    if i == 0: b += rect(fx + 8, yy - 24, 214, 34, SOFTBLUE, rx=6)
    b += text(fx + 22, yy, t, 17, "bold" if i == 0 else "normal", INK)
b += pill(fx + 115, 600, "Ordnerbereich", NAVY, 20, "middle")
# Nachrichtenliste
lx = fx + 230
b += f'<line x1="{lx+340}" y1="{top}" x2="{lx+340}" y2="{y1}" stroke="{LINE}" stroke-width="2"/>'
mails = [("Thomas Weber", "Wasserhahn repariert"), ("Petra Schönfeld", "Nebenkosten 2025"), ("Klara Nowak", "Reinigungsplan Dezember"), ("Lift-Service Nord", "Wartungstermin Aufzug")]
for i, (who, subj) in enumerate(mails):
    yy = top + 14 + i * 84
    if i == 0: b += rect(lx + 6, yy, 328, 76, SOFTBLUE, rx=6) + rect(lx + 6, yy, 5, 76, OUTLOOK, rx=2)
    b += text(lx + 24, yy + 30, who, 18, "bold", INK)
    b += text(lx + 24, yy + 58, subj, 16, fill=MUTED)
b += pill(lx + 170, 600, "Nachrichtenliste", NAVY, 20, "middle")
# Lesebereich
rx_ = lx + 340
b += text(rx_ + 30, top + 44, "Wasserhahn repariert", 24, "bold", INK)
b += text(rx_ + 30, top + 76, "Thomas Weber", 17, "bold", MUTED)
for i, t in enumerate(["Antworten", "Allen antworten", "Weiterleiten"]):
    b += rect(rx_ + 30 + i * 150, top + 92, 140, 30, "#FFFFFF", LINE, 6, 1.5) + text(rx_ + 100 + i * 150, top + 113, t, 14, fill=INK, anchor="middle")
for k in range(5):
    b += bar(rx_ + 30, top + 160 + k * 30, 440 - (k % 3) * 70)
b += pill(rx_ + 260, 600, "Lesebereich", NAVY, 20, "middle")
slides.append(("01-outlook-oberflaeche", "Das neue Outlook auf einen Blick", b,
  "Schema des neuen Outlook-Fensters: oben das Menüband mit der Schaltfläche Neue E-Mail, links die schmale App-Leiste, daneben der Ordnerbereich mit Posteingang, Entwürfe, Gesendete Elemente, Gelöschte Elemente und Archiv, in der Mitte die Nachrichtenliste, rechts der Lesebereich mit den Schaltflächen Antworten, Allen antworten und Weiterleiten."))

# 2 E-Mail-Adresse
b = text(640, 180, "Eine E-Mail-Adresse ist wie eine Postanschrift – ein Tippfehler, und nichts kommt an.", 26, fill=INK, anchor="middle")
parts = [("thomas.weber", 380, OUTLOOK, "Name", "wer die E-Mail bekommt"), ("@", 100, ACCENT, "„bei“", "gesprochen: „ät“"), ("haus-lichtblick.de", 480, EXCEL, "Domain", "Firma – wie Ort und Postleitzahl")]
x = (W - sum(p[1] for p in parts) - 20) / 2
for s, w, col, lab, sub in parts:
    b += rect(x, 220, w, 100, "#FFFFFF", col, 12, 4)
    b += text(x + w / 2, 288, s, 44, "bold", col, "middle")
    b += f'<path d="M{x+10} 340 q0 14 14 14 h{w/2-24} l10 14 l10 -14 h{w/2-24} q14 0 14 -14" fill="none" stroke="{col}" stroke-width="3"/>'
    b += text(x + w / 2, 404, lab, 26, "bold", col, "middle")
    b += text(x + w / 2, 436, sub, 20, fill=MUTED, anchor="middle")
    x += w + 10
b += rect(140, 480, 1000, 150, SOFTYELLOW, ACCENT, 12, 2)
b += text(170, 522, "Darauf achten", 24, "bold", INK)
for i, t in enumerate(["keine Leerzeichen", "Umlaute umschreiben: Schönfeld → schoenfeld", "Punkt und Bindestrich genau übernehmen"]):
    b += f'<circle cx="182" cy="{556+i*30}" r="5" fill="{ACCENT}"/>' + text(200, 563 + i * 30, t, 22, fill=INK)
b += text(1110, 598, "p.schoenfeld@fischer-immo.de", 22, "bold", OUTLOOK, "end")
slides.append(("02-email-adresse", "Aufbau einer E-Mail-Adresse", b,
  "Die Adresse thomas.weber@haus-lichtblick.de in drei Teilen: Name für den Empfänger, das @-Zeichen für „bei“, die Domain für die Firma. Darunter: keine Leerzeichen, Umlaute umschreiben wie in p.schoenfeld@fischer-immo.de, Punkt und Bindestrich genau übernehmen."))

# 3 An, Cc, Bcc
b = ""
rows = [("An", OUTLOOK, SOFTBLUE, "soll etwas tun", "Thomas Weber soll den Wasserhahn reparieren"),
        ("Cc", EXCEL, SOFTGREEN, "soll Bescheid wissen", "Petra Schönfeld (Hausverwaltung) liest mit"),
        ("Bcc", MUTED, GREY, "bekommt eine Kopie, die anderen sehen es nicht", "Rundmail an alle Mieter: niemand sieht die anderen Adressen")]
for i, (lab, col, soft, mean, ex) in enumerate(rows):
    y = 150 + i * 160
    b += rect(60, y, 1160, 140, soft, col, 14, 2)
    b += rect(80, y + 25, 150, 90, col, rx=12) + text(155, y + 86, lab, 40, "bold", "#FFFFFF", "middle")
    b += text(270, y + 62, mean, 32, "bold", INK)
    b += text(270, y + 104, "Im Haus Lichtblick: " + ex, 22, fill=MUTED)
slides.append(("03-an-cc-bcc", "An, Cc und Bcc", b,
  "Drei Zeilen: An heißt, die Person soll etwas tun, etwa Thomas Weber soll den Wasserhahn reparieren. Cc heißt, die Person soll Bescheid wissen, etwa Petra Schönfeld von der Hausverwaltung. Bcc ist eine Kopie, die die anderen nicht sehen, etwa bei einer Rundmail an alle Mieter."))

# 4 Betreff
b = ""
for i, (head, col, soft, items, mark) in enumerate([
        ("So nicht", BAD, SOFTRED, ["Hallo", "(kein Betreff)", "Frage", "Dringend!!!"], "✗"),
        ("So besser", EXCEL, SOFTGREEN, ["Störungsmeldung – Wasserhahn tropft, Teeküche 2. OG", "Aufzugswartung – Bitte um Terminvorschlag", "Reinigung Konferenzraum 3.10 – Rückfrage", "Ausfall Heizung – Büro 305 bleibt kalt"], "✓")]):
    x = 60 + i * 440; w = 380 if i == 0 else 780
    if i == 1: x = 460
    b += rect(x, 145, w, 380, soft, col, 14, 2)
    b += text(x + 30, 195, head, 30, "bold", col)
    for k, t in enumerate(items):
        y = 260 + k * 68
        b += rect(x + 24, y - 34, w - 48, 52, "#FFFFFF", LINE, 8, 1.5)
        b += text(x + 44, y, mark, 24, "bold", col) + text(x + 80, y, t, 22 if i else 24, fill=INK)
b += rect(60, 545, 1160, 90, SOFTYELLOW, ACCENT, 12, 2)
b += text(640, 584, "Was? Wo? – Am Betreff erkennt man, worum es geht,", 26, "bold", INK, "middle")
b += text(640, 618, "ohne die E-Mail zu öffnen.", 26, "bold", INK, "middle")
slides.append(("04-betreff", "Ein guter Betreff", b,
  "Links schlechte Betreffzeilen: Hallo, kein Betreff, Frage, Dringend. Rechts gute: Störungsmeldung – Wasserhahn tropft, Teeküche 2. OG; Aufzugswartung – Bitte um Terminvorschlag; Reinigung Konferenzraum 3.10 – Rückfrage; Ausfall Heizung – Büro 305 bleibt kalt. Regel: Was und wo – am Betreff erkennt man, worum es geht."))

# 5 Antworten, Allen antworten, Weiterleiten
b = ""
def person(cx, cy, col, lab):
    s = f'<circle cx="{cx}" cy="{cy-14}" r="14" fill="{col}"/><path d="M{cx-22} {cy+22} a22 22 0 0 1 44 0 z" fill="{col}"/>'
    return s + text(cx, cy + 50, lab, 18, "bold", INK, "middle")
cards = [("Antworten", OUTLOOK, "AW:", ["nur an die Person,", "die geschrieben hat"]),
         ("Allen antworten", WORD, "AW:", ["an die Person und alle", "aus „An“ und „Cc“"]),
         ("Weiterleiten", EXCEL, "WG:", ["an eine neue Person –", "Ihr Kommentar steht oben"])]
for i, (head, col, pre, lines) in enumerate(cards):
    x = 60 + i * 395; w = 370
    b += rect(x, 145, w, 480, "#FFFFFF", LINE, 14, 2)
    b += f'<path d="M{x} 159 a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v62 h-{w} z" fill="{col}"/>'
    b += text(x + w / 2, 195, head, 32, "bold", "#FFFFFF", "middle")
    cy = 300
    if i == 0:
        b += person(x + 90, cy, MUTED, "Sie") + person(x + 280, cy, col, "Absender")
        b += f'<path d="M{x+130} {cy} h100" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
    elif i == 1:
        b += person(x + 60, cy, MUTED, "Sie") + person(x + 190, cy, col, "Absender") + person(x + 310, cy, col, "alle")
        b += f'<path d="M{x+95} {cy} h55" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
        b += f'<path d="M{x+80} {cy-45} Q {x+190} {cy-120} {x+300} {cy-50}" fill="none" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
    else:
        b += person(x + 90, cy, MUTED, "Sie") + person(x + 280, cy, col, "neue Person")
        b += f'<path d="M{x+130} {cy} h100" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
    b += text(x + w / 2, 430, lines[0], 24, fill=INK, anchor="middle") + text(x + w / 2, 462, lines[1], 24, fill=INK, anchor="middle")
    b += f'<line x1="{x+30}" y1="500" x2="{x+w-30}" y2="500" stroke="{LINE}" stroke-width="2"/>'
    b += text(x + w / 2, 540, "Betreff beginnt mit", 20, fill=MUTED, anchor="middle")
    b += text(x + w / 2, 590, pre, 40, "bold", col, "middle")
slides.append(("05-antworten-weiterleiten", "Antworten oder weiterleiten?", b,
  "Drei Karten: Antworten geht nur an die Person, die geschrieben hat, der Betreff beginnt mit AW. Allen antworten geht an die Person und alle aus An und Cc, Betreff ebenfalls AW. Weiterleiten schickt die E-Mail an eine neue Person, der eigene Kommentar steht oben, der Betreff beginnt mit WG."))

# 6 Ordner
b = ""
b += rect(60, 145, 470, 480, "#FAFBFC", LINE, 14, 2)
tree = [("Posteingang", 0, True), ("Hausverwaltung", 1, False), ("Störungsmeldungen", 1, True), ("Wartung", 1, False), ("Entwürfe", 0, False), ("Gesendete Elemente", 0, False)]
for i, (t, lvl, hl) in enumerate(tree):
    y = 200 + i * 58
    x = 90 + lvl * 40
    if hl and lvl: b += rect(x - 10, y - 32, 400 - lvl * 40, 46, SOFTBLUE, OUTLOOK, 8, 2)
    b += f'<path d="M{x} {y-18} h14 l5 6 h19 v20 h-38 z" fill="{ACCENT if lvl else NAVY}"/>'
    b += text(x + 52, y, t, 24, "bold" if i == 0 else "normal", INK)
# gezogene E-Mail
b += rect(310, 550, 190, 60, "#FFFFFF", OUTLOOK, 8, 2) + f'<path d="M322 562 h40 v28 h-40 z M322 562 l20 14 l20 -14" fill="none" stroke="{OUTLOOK}" stroke-width="2"/>'
b += text(374, 586, "Wasserhahn …", 18, fill=INK)
b += f'<path d="M420 545 C 440 450, 450 360, 480 330" fill="none" stroke="{ACCENT}" stroke-width="5" stroke-dasharray="10 8" marker-end="url(#pf)"/>'
steps = [("1", "Rechtsklick auf „Posteingang“"), ("2", "„Neuen Unterordner erstellen“"), ("3", "Namen tippen, Enter"), ("4", "E-Mail auf den Ordner ziehen")]
for i, (n, t) in enumerate(steps):
    y = 190 + i * 85
    b += f'<circle cx="610" cy="{y}" r="26" fill="{OUTLOOK}"/>' + text(610, y + 10, n, 28, "bold", "#FFFFFF", "middle")
    b += text(660, y + 10, t, 28, fill=INK)
b += rect(580, 540, 640, 85, SOFTYELLOW, ACCENT, 12, 2)
b += text(900, 593, "Wie Aktenordner: nach Themen statt auf einem Stapel", 23, "bold", INK, "middle")
slides.append(("06-ordner", "Ordnung mit Ordnern", b,
  "Links der Ordnerbereich: unter Posteingang die Unterordner Hausverwaltung, Störungsmeldungen und Wartung; eine E-Mail wird mit der Maus auf den Ordner Störungsmeldungen gezogen. Rechts vier Schritte: Rechtsklick auf Posteingang, Neuen Unterordner erstellen, Namen tippen und Enter, E-Mail auf den Ordner ziehen. Vergleich: wie Aktenordner nach Themen."))

for i, (name, title, body, desc) in enumerate(slides, 1):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(frame(i, title, body, desc))
print("ok", len(slides))
