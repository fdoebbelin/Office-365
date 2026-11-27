# Folien Block 03 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-03.py assets/folien/block-03
# Vorschau: magick -density 72 assets/folien/block-03/01-kalender.svg vorschau.png
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
{text(60,694,"Block 03 · Kalender und Termine",20,fill=MUTED)}
{text(W-60,694,"Haus Lichtblick – Microsoft 365  ·  Folie "+str(nr),20,fill=MUTED,anchor="end")}
</svg>
'''

slides = []
def bell(cx, cy, col=ACCENT, s=1.0):
    return (f'<path d="M{cx-14*s} {cy+8*s} q0 {-26*s} {14*s} {-26*s} q{14*s} 0 {14*s} {26*s} l{5*s} {6*s} h{-38*s} z" fill="{col}"/>'
            f'<circle cx="{cx}" cy="{cy+18*s}" r="{5*s}" fill="{col}"/>')
def person(cx, cy, col, lab, size=18):
    s = f'<circle cx="{cx}" cy="{cy-14}" r="14" fill="{col}"/><path d="M{cx-22} {cy+22} a22 22 0 0 1 44 0 z" fill="{col}"/>'
    return s + (text(cx, cy + 50, lab, size, "bold", INK, "middle") if lab else "")

# 1 Kalender und Ansichten
b = ""
x0, y0, x1, y1 = 60, 140, 1220, 630
b += rect(x0, y0, x1 - x0, y1 - y0, "#FFFFFF", INK, 10, 3)
b += f'<path d="M{x0} {y0+10} a10 10 0 0 1 10 -10 h{x1-x0-20} a10 10 0 0 1 10 10 v26 h-{x1-x0} z" fill="{OUTLOOK}"/>'
top = y0 + 36
b += rect(x0 + 2, top, 64, y1 - top - 2, "#E4E8EE", rx=0)
# Briefumschlag und Kalender
b += rect(x0 + 18, top + 22, 32, 32, "#FFFFFF", MUTED, 6, 2) + f'<path d="M{x0+22} {top+30} l12 9 l12 -9" fill="none" stroke="{MUTED}" stroke-width="2.5"/>'
b += rect(x0 + 18, top + 78, 32, 32, OUTLOOK, OUTLOOK, 6, 2) + rect(x0 + 24, top + 90, 20, 14, "#FFFFFF", rx=2)
b += f'<path d="M{x0+70} {top+94} h60" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
b += text(x0 + 140, top + 102, "Kalender", 22, "bold", OUTLOOK)
# Menüband mit Neues Ereignis und Ansichten
b += rect(x0 + 66, top, x1 - x0 - 68, 56, GREY, rx=0)
b += rect(x0 + 260, top + 14, 160, 30, OUTLOOK, rx=6) + text(x0 + 340, top + 35, "Neues Ereignis", 16, "bold", "#FFFFFF", "middle")
views = ["Tag", "Arbeitswoche", "Woche", "Monat"]
vx = 620
for i, v in enumerate(views):
    w = len(v) * 10 + 30
    b += rect(vx, top + 14, w, 30, SOFTBLUE if i == 1 else "#FFFFFF", OUTLOOK if i == 1 else LINE, 6, 1.5)
    b += text(vx + w / 2, top + 35, v, 16, "bold" if i == 1 else "normal", INK, "middle")
    vx += w + 10
b += text(1180, top + 35, "Heute", 16, "bold", OUTLOOK, "end")
# Wochenraster
gx, gy = x0 + 230, top + 150; days = ["Mo", "Di", "Mi", "Do", "Fr"]; cw = 180; rh = 48
for i, d in enumerate(days):
    b += text(gx + i * cw + cw / 2, gy - 14, d, 18, "bold", MUTED, "middle")
for r in range(7):
    b += f'<line x1="{gx}" y1="{gy+r*rh}" x2="{gx+5*cw}" y2="{gy+r*rh}" stroke="{LINE}" stroke-width="1.5"/>'
    b += text(gx - 14, gy + r * rh + 6, f"{8+r}:00", 15, fill=MUTED, anchor="end")
for i in range(6):
    b += f'<line x1="{gx+i*cw}" y1="{gy}" x2="{gx+i*cw}" y2="{gy+6*rh}" stroke="{LINE}" stroke-width="1.5"/>'
b += rect(gx + 4, gy + 4, cw - 8, rh * 1.5 - 8, SOFTRED, BAD, 6, 2) + text(gx + 14, gy + 30, "Heizungswartung", 15, "bold", INK)
b += rect(gx + cw * 3 + 4, gy + rh * 4 + 4, cw - 8, rh * 1.5 - 8, SOFTBLUE, OUTLOOK, 6, 2) + text(gx + cw * 3 + 14, gy + rh * 4 + 30, "Sicherheitsbegehung", 15, "bold", INK)
b += rect(gx + cw * 1 + 4, gy + rh * 2 + 4, cw - 8, rh - 8, SOFTGREEN, EXCEL, 6, 2) + text(gx + cw + 14, gy + rh * 2 + 30, "Fluchtwege prüfen", 15, "bold", INK)
b += pill(1000, top + 88, "Ansicht wählen", NAVY, 18, "middle")
slides.append(("01-kalender", "Der Kalender in Outlook", b,
  "Schema des Outlook-Kalenders: In der App-Leiste links führt das Kalendersymbol zum Kalender. Oben die Schaltfläche Neues Ereignis und die Ansichten Tag, Arbeitswoche, Woche und Monat sowie Heute. Darunter eine Arbeitswoche von Montag bis Freitag mit drei Einträgen: Heizungswartung, Fluchtwege prüfen und Sicherheitsbegehung."))

# 2 Drei Arten von Einträgen
b = text(640, 170, "Alles beginnt mit „Neues Ereignis“ – was daraus wird, entscheiden Sie beim Ausfüllen.", 24, fill=INK, anchor="middle")
cards = [("Termin", EXCEL, SOFTGREEN, ["nur für Sie", "niemand eingeladen"], "Fluchtwege prüfen", "Speichern"),
         ("Besprechung", OUTLOOK, SOFTBLUE, ["mit anderen", "Einladung per E-Mail"], "Sicherheitsbegehung", "Senden"),
         ("Ganztägig", ACCENT, SOFTYELLOW, ["ohne Uhrzeit", "gilt den ganzen Tag"], "Aufzug gesperrt", "Schalter „Ganztägig“")]
for i, (head, col, soft, lines, ex, btn) in enumerate(cards):
    x = 60 + i * 395; w = 370
    b += rect(x, 200, w, 430, "#FFFFFF", LINE, 14, 2)
    b += f'<path d="M{x} 214 a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v62 h-{w} z" fill="{col}"/>'
    b += text(x + w / 2, 250, head, 32, "bold", "#FFFFFF", "middle")
    b += text(x + w / 2, 330, lines[0], 28, "bold", INK, "middle") + text(x + w / 2, 368, lines[1], 22, fill=MUTED, anchor="middle")
    b += f'<line x1="{x+30}" y1="400" x2="{x+w-30}" y2="400" stroke="{LINE}" stroke-width="2"/>'
    b += text(x + w / 2, 440, "Im Haus Lichtblick", 18, "bold", MUTED, "middle")
    b += text(x + w / 2, 476, ex, 24, fill=col if col != ACCENT else "#9A6412", anchor="middle")
    bw = len(btn) * 12 + 40
    b += rect(x + (w - bw) / 2, 530, bw, 50, soft, col, 8, 2) + text(x + w / 2, 563, btn, 22, "bold", INK, "middle")
slides.append(("02-ereignisarten", "Termin, Besprechung, ganztägig", b,
  "Drei Karten: Ein Termin ist nur für Sie, niemand ist eingeladen, die Schaltfläche heißt Speichern – Beispiel Fluchtwege prüfen. Eine Besprechung ist mit anderen und geht als Einladung per E-Mail hinaus, die Schaltfläche heißt Senden – Beispiel Sicherheitsbegehung. Ein ganztägiges Ereignis hat keine Uhrzeit, Schalter Ganztägig – Beispiel Aufzug gesperrt."))

# 3 Das Ereignisfenster
b = ""
fx, fy, fw, fh = 60, 140, 700, 490
b += rect(fx, fy, fw, fh, "#FFFFFF", INK, 10, 3)
rows = [("Titel hinzufügen", "Heizungswartung", True), ("Teilnehmende einladen", "", False), ("Datum · Beginn · Ende", "Mo · 08:00 – 09:30", True), ("Ort", "Technikraum 1 (Heizung)", True)]
for i, (lab, val, filled) in enumerate(rows):
    y = fy + 40 + i * 70
    b += rect(fx + 30, y, fw - 60, 50, "#FFFFFF", LINE, 6, 1.5)
    b += text(fx + 46, y + 32, val if filled else lab, 20, "bold" if i == 0 else "normal", INK if filled else MUTED)
# Ganztägig / Serie / Erinnerung
y = fy + 330
b += rect(fx + 30, y, 54, 28, LINE, rx=14) + f'<circle cx="{fx+44}" cy="{y+14}" r="11" fill="#FFFFFF"/>' + text(fx + 96, y + 21, "Ganztägig", 18, fill=INK)
b += rect(fx + 230, y - 4, 190, 36, SOFTBLUE, OUTLOOK, 6, 2) + text(fx + 325, y + 20, "Serie erstellen", 18, "bold", OUTLOOK, "middle")
b += rect(fx + 450, y - 4, 220, 36, SOFTYELLOW, ACCENT, 6, 2) + bell(fx + 472, y + 10, ACCENT, 0.6) + text(fx + 492, y + 20, "1 Tag vorher", 18, "bold", INK)
b += rect(fx + 30, y + 52, fw - 60, 44, GREY, rx=6) + text(fx + 46, y + 80, "Notiz, z. B. Checkliste", 18, fill=MUTED)
# Erklärungen rechts
notes = [("1", "Titel: Was?", "kurz und eindeutig"), ("2", "Teilnehmende einladen", "macht daraus eine Besprechung"), ("3", "Datum und Uhrzeit", "oder Schalter „Ganztägig“"), ("4", "Serie erstellen", "für Wiederkehrendes"), ("5", "Erinnerung", "Glocke: z. B. 1 Tag vorher"), ("6", "Speichern / Senden", "Senden, sobald jemand eingeladen ist")]
for i, (n, h, d) in enumerate(notes):
    y = 172 + i * 76
    b += f'<circle cx="820" cy="{y}" r="22" fill="{OUTLOOK}"/>' + text(820, y + 8, n, 22, "bold", "#FFFFFF", "middle")
    b += text(856, y + 2, h, 24, "bold", INK) + text(856, y + 32, d, 19, fill=MUTED)
for n, (cx, cy) in zip("12345", [(fx + fw - 50, fy + 65), (fx + fw - 50, fy + 135), (fx + fw - 50, fy + 205), (fx + 436, fy + 344), (fx + 688, fy + 344)]):
    b += f'<circle cx="{cx}" cy="{cy}" r="15" fill="{OUTLOOK}"/>' + text(cx, cy + 6, n, 17, "bold", "#FFFFFF", "middle")
b += rect(fx + 30, fy + fh - 50, 130, 36, OUTLOOK, rx=6) + text(fx + 95, fy + fh - 26, "Speichern", 17, "bold", "#FFFFFF", "middle")
b += f'<circle cx="{fx+178}" cy="{fy+fh-32}" r="15" fill="{OUTLOOK}"/>' + text(fx + 178, fy + fh - 26, "6", 17, "bold", "#FFFFFF", "middle")
slides.append(("03-ereignisfenster", "Das Fenster „Neues Ereignis“", b,
  "Schema des Ereignisfensters mit sechs nummerierten Stellen: 1 Titel, 2 Teilnehmende einladen – macht daraus eine Besprechung, 3 Datum und Uhrzeit oder der Schalter Ganztägig, 4 Serie erstellen für Wiederkehrendes, 5 Erinnerung mit der Glocke, zum Beispiel 1 Tag vorher, 6 Speichern, oder Senden, sobald jemand eingeladen ist. Beispiel: Heizungswartung, Montag 08:00 bis 09:30, Technikraum 1."))

# 4 Serie
b = text(60, 175, "Heizungswartung: monatlich · am ersten Montag · 08:00–09:30", 28, "bold", INK)
months = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun"]
tx, ty, tw = 100, 330, 1080
b += f'<line x1="{tx}" y1="{ty}" x2="{tx+tw}" y2="{ty}" stroke="{NAVY}" stroke-width="4"/>'
for i, m in enumerate(months):
    x = tx + i * tw / 6
    b += f'<line x1="{x}" y1="{ty-14}" x2="{x}" y2="{ty+14}" stroke="{NAVY}" stroke-width="3"/>'
    b += text(x + tw / 12, ty + 50, m, 24, "bold", MUTED, "middle")
    cx = x + 40
    b += rect(cx - 30, ty - 110, 60, 70, "#FFFFFF", BAD, 8, 3) + rect(cx - 30, ty - 110, 60, 20, BAD, rx=4)
    b += text(cx, ty - 54, "1. Mo", 16, "bold", INK, "middle")
    b += f'<line x1="{cx}" y1="{ty-40}" x2="{cx}" y2="{ty}" stroke="{BAD}" stroke-width="2" stroke-dasharray="4 4"/>'
b += text(tx + tw, ty + 50, "…", 28, "bold", MUTED, "end")
b += rect(60, 420, 560, 200, SOFTBLUE, OUTLOOK, 12, 2)
b += text(90, 462, "So geht's", 24, "bold", OUTLOOK)
for i, t in enumerate(["„Serie erstellen“ anklicken", "Muster: Monatlich", "„Am ersten Montag“ wählen", "Ende festlegen, übernehmen"]):
    b += text(90, 502 + i * 30, f"{i+1}  {t}", 21, fill=INK)
b += rect(660, 420, 560, 200, SOFTYELLOW, ACCENT, 12, 2)
b += bell(710, 470, ACCENT, 1.2)
b += text(750, 478, "Einmal anlegen –", 26, "bold", INK)
b += text(750, 514, "Outlook trägt jeden Monat ein.", 22, fill=INK)
b += text(750, 560, "Erinnerung 1 Tag vorher:", 22, "bold", INK)
b += text(750, 592, "Zeit, Schlüssel und Zugang zu klären.", 22, fill=INK)
slides.append(("04-serie", "Wiederkehrende Termine: die Serie", b,
  "Zeitstrahl von Januar bis Juni, in jedem Monat ist der erste Montag markiert: Heizungswartung monatlich am ersten Montag, 08:00 bis 09:30. Darunter die Schritte: Serie erstellen anklicken, Muster Monatlich, Am ersten Montag wählen, Ende festlegen. Hinweis: einmal anlegen, Outlook trägt jeden Monat ein; Erinnerung 1 Tag vorher."))

# 5 Besprechung
b = ""
b += person(150, 330, NAVY, "Sie (Organisation)", 20)
b += rect(270, 260, 280, 130, SOFTBLUE, OUTLOOK, 12, 2)
b += f'<path d="M300 285 h60 v42 h-60 z M300 285 l30 22 l30 -22" fill="none" stroke="{OUTLOOK}" stroke-width="3"/>'
b += text(380, 302, "Einladung", 22, "bold", INK) + text(380, 330, "per E-Mail", 20, fill=MUTED)
b += text(290, 370, "Sicherheitsbegehung", 18, "bold", OUTLOOK)
b += f'<path d="M200 320 h60" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
b += f'<path d="M560 300 L640 230" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/><path d="M560 350 L640 420" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
b += person(700, 220, OUTLOOK, "Thomas Weber") + person(700, 420, OUTLOOK, "Jan Müller")
ans = [("Zusagen", EXCEL, SOFTGREEN), ("Mit Vorbehalt", ACCENT, SOFTYELLOW), ("Ablehnen", BAD, SOFTRED)]
for i, (t, col, soft) in enumerate(ans):
    y = 190 + i * 80
    b += rect(820, y, 220, 56, soft, col, 8, 2) + text(930, y + 36, t, 22, "bold", INK, "middle")
b += text(1060, 225, "→ steht im", 20, fill=MUTED) + text(1060, 252, "Kalender", 20, "bold", INK)
b += text(1060, 385, "→ Sie bekommen", 20, fill=MUTED) + text(1060, 412, "eine Antwort", 20, "bold", INK)
b += rect(60, 530, 1160, 95, SOFTYELLOW, ACCENT, 12, 2)
b += text(640, 570, "Die Eingeladenen sehen nur diese Besprechung –", 24, "bold", INK, "middle")
b += text(640, 604, "nicht Ihren übrigen Kalender.", 24, "bold", INK, "middle")
slides.append(("05-besprechung", "Zu einer Besprechung einladen", b,
  "Sie als Organisation schicken eine Einladung zur Sicherheitsbegehung per E-Mail an Thomas Weber und Jan Müller. Die beiden antworten mit Zusagen, Mit Vorbehalt oder Ablehnen; die Besprechung steht dann in ihrem Kalender, und Sie bekommen eine Antwort. Hinweis: Die Eingeladenen sehen nur diese Besprechung, nicht Ihren übrigen Kalender."))

for i, (name, title, body, desc) in enumerate(slides, 1):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(frame(i, title, body, desc))
print("ok", len(slides))
