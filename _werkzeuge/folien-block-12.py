# Folien Block 12 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-12.py assets/folien/block-12
# Vorschau: magick -density 72 assets/folien/block-12/01-was-kann-ich.svg vorschau.png
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
{text(60,694,"Block 12 · Abschluss und Ausblick",20,fill=MUTED)}
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

# 1 Was kann ich jetzt?
b = ""
cols = [(OUTLOOK, "Outlook", ["E-Mails schreiben, antworten", "weiterleiten mit Kommentar", "An, Cc, Bcc, guter Betreff", "Ordner anlegen, sortieren", "Termine mit Erinnerung", "Serien, Besprechungen", "Anhänge versenden"]),
        (WORD, "Word", ["Dokumente speichern, öffnen", "markieren, formatieren", "Absatz und neue Zeile", "Listen, Überschriften", "Tabellen einfügen", "Seitenränder, drucken", "Excel-Daten einfügen"]),
        (EXCEL, "Excel", ["Daten eingeben", "Formeln mit Zelladressen", "Ausfüllkästchen", "SUMME, MITTELWERT …", "Zahlenformate", "sortieren und filtern", "Diagramme"])]
for i, (col, name, items) in enumerate(cols):
    x = 60 + i * 395; w = 370
    b += rect(x, 150, w, 470, "#FFFFFF", LINE, 14, 2)
    b += f'<path d="M{x} 164 a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v50 h-{w} z" fill="{col}"/>'
    b += text(x + w / 2, 194, name, 26, "bold", "#FFFFFF", "middle")
    for k, t in enumerate(items): b += checkrow(x + 24, 258 + k * 50, t, col)
slides.append(("01-was-kann-ich", "Was Sie jetzt können", b,
  "Drei Spalten mit Häkchen. Outlook: E-Mails schreiben und beantworten, weiterleiten mit Kommentar, An, Cc, Bcc und guter Betreff, Ordner, Termine mit Erinnerung, Serien und Besprechungen, Anhänge. Word: speichern und öffnen, markieren und formatieren, Absatz und neue Zeile, Listen und Überschriften, Tabellen, Seitenränder und Drucken, Excel-Daten einfügen. Excel: Daten eingeben, Formeln mit Zelladressen, Ausfüllkästchen, SUMME und MITTELWERT, Zahlenformate, sortieren und filtern, Diagramme."))

# 2 Tastenkürzel
b = ""
rows = [(["Strg", "S"], "Speichern", "Word, Excel"), (["Strg", "Z"], "Rückgängig", "alle drei"), (["Strg", "C"], "Kopieren", "alle drei"),
        (["Strg", "V"], "Einfügen", "alle drei"), (["Strg", "P"], "Drucken", "Word, Excel"), (["Strg", "F"], "Suchen", "Word, Excel"), (["Alt", "Tab"], "Programm wechseln", "Windows")]
for i, (keys, what, where) in enumerate(rows):
    y = 150 + i * 66
    x = 80
    for k, t in enumerate(keys):
        s, w = key(x, y, t, 80 if t in ("Strg", "Alt", "Tab") else 56)
        b += s; x += w + 8
        if k == 0: b += text(x - 2, y + 34, "+", 22, "bold", MUTED); x += 18
    b += text(330, y + 35, what, 26, "bold", INK) + text(640, y + 35, where, 22, fill=MUTED)
b += rect(860, 160, 360, 440, SOFTYELLOW, ACCENT, 14, 2)
b += text(885, 205, "Das wichtigste:", 24, "bold", INK)
s, w = key(885, 235, "Strg", 90); b += s
b += text(990, 270, "+", 26, "bold", MUTED)
s, w = key(1015, 235, "Z", 70); b += s
for k, t in enumerate(["macht den letzten Schritt", "rückgängig – auch mehrmals.", "", "Am Computer geht fast", "nichts kaputt. Probieren", "Sie aus!"]):
    b += text(885, 340 + k * 34, t, 21, "bold" if k >= 3 else "normal", INK)
slides.append(("02-tastenkuerzel", "Die wichtigsten Tastenkürzel", b,
  "Tastenkürzel: Strg+S Speichern in Word und Excel, Strg+Z Rückgängig in allen drei Programmen, Strg+C Kopieren, Strg+V Einfügen, Strg+P Drucken, Strg+F Suchen, Alt+Tab Programm wechseln. Hervorgehoben: Strg+Z macht den letzten Schritt rückgängig, auch mehrmals – am Computer geht fast nichts kaputt."))

# 3 Häufige Fehler
b = ""
rows = [("Datei nicht gespeichert – Arbeit weg", "früh und oft Strg+S"), ("Zahl abgetippt statt Formel", "mit = beginnen, Zellen anklicken"),
        ("Formatiert, ohne zu markieren", "erst markieren, dann formatieren"), ("E-Mail an den falschen Empfänger", "An und Betreff vor dem Senden prüfen"),
        ("Alte Fassung angehängt", "erst speichern, dann anhängen"), ("Mehrmals Enter für Abstand", "Abstand über „Layout“ einstellen")]
b += text(60, 172, "Fehler", 22, "bold", BAD) + text(700, 172, "So vermeiden Sie ihn", 22, "bold", EXCEL)
for i, (f, v) in enumerate(rows):
    y = 192 + i * 72
    b += rect(60, y, 580, 58, SOFTRED, LINE, 8, 1.5) + text(80, y + 37, f, 21, fill=INK)
    b += f'<path d="M648 {y+29} h38" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
    b += rect(700, y, 520, 58, SOFTX, LINE, 8, 1.5) + text(720, y + 37, v, 21, "bold", INK)
slides.append(("03-haeufige-fehler", "Häufige Fehler – und wie Sie sie vermeiden", b,
  "Sechs Paare: Datei nicht gespeichert – früh und oft Strg+S; Zahl abgetippt statt Formel – mit Gleichheitszeichen beginnen und Zellen anklicken; formatiert ohne zu markieren – erst markieren, dann formatieren; E-Mail an den falschen Empfänger – An und Betreff vor dem Senden prüfen; alte Fassung angehängt – erst speichern, dann anhängen; mehrmals Enter für Abstand – Abstand über Layout einstellen."))

# 4 Copilot
b = ""
cards = [("Was ist das?", ["Ein KI-Assistent in Outlook,", "Word und Excel: fasst E-Mails", "zusammen, entwirft Texte,", "schlägt Formeln vor."]),
         ("Was braucht man?", ["Je nach Vertrag enthalten", "oder extra – ob und wo,", "entscheidet der Arbeitgeber.", ""]),
         ("Worauf achten?", ["Ergebnisse immer prüfen.", "Nur mit dem Arbeitskonto.", "Keine Mieterdaten eingeben,", "wenn es nicht erlaubt ist."])]
for i, (h, lines) in enumerate(cards):
    x = 60 + i * 395; w = 370
    b += rect(x, 150, w, 300, "#FFFFFF", LINE, 14, 2)
    b += f'<path d="M{x} 164 a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v50 h-{w} z" fill="{NAVY}"/>'
    b += text(x + w / 2, 194, h, 24, "bold", "#FFFFFF", "middle")
    for k, t in enumerate(lines): b += text(x + 24, 260 + k * 36, t, 20, fill=INK)
b += rect(60, 480, 1160, 140, SOFTYELLOW, ACCENT, 14, 2)
b += text(640, 540, "„Copilot schreibt den Entwurf –", 30, "bold", INK, "middle")
b += text(640, 585, "Sie bleiben verantwortlich für das Ergebnis.“", 30, "bold", INK, "middle")
slides.append(("04-copilot", "Ausblick: Copilot", b,
  "Drei Karten zu Copilot. Was ist das: ein KI-Assistent in Outlook, Word und Excel, der E-Mails zusammenfasst, Texte entwirft und Formeln vorschlägt. Was braucht man: je nach Vertrag enthalten oder extra, der Arbeitgeber entscheidet. Worauf achten: Ergebnisse prüfen, nur mit dem Arbeitskonto, keine Mieterdaten eingeben, wenn es nicht erlaubt ist. Merksatz: Copilot schreibt den Entwurf – Sie bleiben verantwortlich für das Ergebnis."))

# 5 Wie geht es weiter?
b = ""
mods = [(WORD, "Aufbau Word", ["Absätze, Bilder, Tabellen", "Felder, Kopf- und Fußzeilen", "Formatvorlagen, Inhaltsverzeichnis", "Geschäftsbrief nach DIN 5008"]),
        (EXCEL, "Aufbau Excel", ["WENN, SUMMEWENN", "XVERWEIS", "Filter und bedingte Formatierung", "Pivot-Tabellen"]),
        (NAVY, "Aufbau Verknüpfung", ["Kassenbuch mit Datenüberprüfung", "Excel in Word: einbetten", "oder verknüpfen", "Serien-E-Mail"])]
for i, (col, h, lines) in enumerate(mods):
    x = 60 + i * 395; w = 370
    b += rect(x, 150, w, 300, "#FFFFFF", LINE, 14, 2)
    b += f'<path d="M{x} 164 a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v50 h-{w} z" fill="{col}"/>'
    b += text(x + w / 2, 194, h, 24, "bold", "#FFFFFF", "middle")
    for k, t in enumerate(lines): b += f'<circle cx="{x+30}" cy="{254+k*44}" r="5" fill="{col}"/>' + text(x + 46, 261 + k * 44, t, 19, fill=INK)
b += rect(60, 480, 1160, 140, SOFTX, EXCEL, 14, 2)
b += text(90, 525, "Am besten lernen Sie im Alltag:", 24, "bold", INK)
b += text(90, 562, "Nehmen Sie sich jede Woche eine echte Aufgabe vor – eine Störungsmeldung, eine Liste,", 20, fill=INK)
b += text(90, 592, "einen Aushang – und lösen Sie sie mit den Werkzeugen aus dem Kurs.", 20, fill=INK)
slides.append(("05-wie-weiter", "Wie geht es weiter?", b,
  "Drei Aufbaumodule: Word mit Absätzen, Bildern, Tabellen, Feldern, Kopf- und Fußzeilen, Formatvorlagen, Inhaltsverzeichnis und Geschäftsbrief nach DIN 5008; Excel mit WENN, SUMMEWENN, XVERWEIS, Filtern, bedingter Formatierung und Pivot-Tabellen; Verknüpfung mit Kassenbuch, Excel in Word einbetten oder verknüpfen und Serien-E-Mail. Darunter der Rat: jede Woche eine echte Aufgabe mit den Werkzeugen aus dem Kurs lösen."))

for i, (name, title, body, desc) in enumerate(slides, 1):
    open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(frame(i, title, body, desc))
print("ok", len(slides))
