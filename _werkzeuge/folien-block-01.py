# Folien Block 01 als SVG erzeugen.
# Aufruf: python3 _werkzeuge/folien-block-01.py assets/folien/block-01
# Vorschau: magick -density 72 assets/folien/block-01/01-microsoft-365.svg vorschau.png
import sys, html
OUT = sys.argv[1]
W, H = 1280, 720
FONT = "Segoe UI, Aptos, Arial, Helvetica, sans-serif"
NAVY = "#1F3A5F"; INK = "#1E2430"; MUTED = "#5B6472"; LINE = "#D5DAE1"
OUTLOOK = "#0F6CBD"; WORD = "#185ABD"; EXCEL = "#107C41"; ONEDRIVE = "#2C7BC0"; ACCENT = "#E8A33D"

def esc(s): return html.escape(s, quote=True)
def text(x, y, s, size=28, weight="normal", fill=INK, anchor="start", italic=False):
    st = ' font-style="italic"' if italic else ''
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{st}>{esc(s)}</text>'
def rect(x, y, w, h, fill="#fff", stroke="none", rx=12, sw=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
def frame(nr, title, body, desc):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t d">
<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>
{rect(0,0,W,H,"#FFFFFF",rx=0)}
{rect(0,0,W,110,NAVY,rx=0)}
{text(60,72,title,44,"bold","#FFFFFF")}
{body}
<line x1="60" y1="660" x2="{W-60}" y2="660" stroke="{LINE}" stroke-width="2"/>
{text(60,694,"Block 01 · Orientierung in Microsoft 365",20,fill=MUTED)}
{text(W-60,694,"Haus Lichtblick – Microsoft 365  ·  Folie "+str(nr),20,fill=MUTED,anchor="end")}
</svg>
'''
def card(x, y, w, h, color, head, lines, sub=None):
    s = rect(x, y, w, h, "#FFFFFF", LINE, 14)
    s += f'<path d="M{x} {y+14} a14 14 0 0 1 14 -14 h{w-28} a14 14 0 0 1 14 14 v66 h-{w} z" fill="{color}"/>'
    s += text(x + w/2, y + 54, head, 34, "bold", "#FFFFFF", "middle")
    yy = y + 150
    for i, l in enumerate(lines):
        if not l: continue
        s += text(x + w/2, yy, l, 32 if i == 0 else 26, "bold" if i == 0 else "normal", INK if i == 0 else MUTED, "middle"); yy += 60 if i == 0 else 38
    if sub:
        yy = y + 340
        s += f'<line x1="{x+30}" y1="{yy-40}" x2="{x+w-30}" y2="{yy-40}" stroke="{LINE}" stroke-width="2"/>'
        s += text(x + w/2, yy, "Im Haus Lichtblick", 20, "bold", MUTED, "middle"); yy += 40
        for l in sub:
            s += text(x + w/2, yy, l, 26, fill=color, anchor="middle"); yy += 36
    return s

slides = []

# 1 Microsoft 365 – Werkzeugkasten
b = text(60,180,"Ein Programmpaket für den Büroalltag – früher hieß es „Office“.",30,fill=INK)
# toolbox
b += f'<path d="M250 300 h780 a16 16 0 0 1 16 16 v240 a16 16 0 0 1 -16 16 h-780 a16 16 0 0 1 -16 -16 v-240 a16 16 0 0 1 16 -16 z" fill="#F3F5F8" stroke="{NAVY}" stroke-width="4"/>'
b += f'<path d="M520 300 v-40 a14 14 0 0 1 14 -14 h212 a14 14 0 0 1 14 14 v40" fill="none" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>'
for i,(name,col,sub) in enumerate([("Outlook",OUTLOOK,"E-Mail, Termine"),("Word",WORD,"Texte"),("Excel",EXCEL,"Listen, Zahlen"),("OneDrive",ONEDRIVE,"Online-Speicher")]):
    x = 280 + i*185
    b += rect(x,340,165,190,"#FFFFFF",col,12,3)
    b += rect(x+52,365,60,60,col,rx=10)
    b += text(x+82,407,name[0],34,"bold","#FFFFFF","middle")
    b += text(x+82,470,name,26,"bold",INK,"middle")
    b += text(x+82,505,sub,20,fill=MUTED,anchor="middle")
b += text(640,620,"Wie ein Werkzeugkasten: Jedes Werkzeug hat seinen eigenen Zweck.",26,fill=MUTED,anchor="middle",italic=True)
slides.append(("01-microsoft-365","Was ist Microsoft 365?",b,"Microsoft 365 als Werkzeugkasten mit Outlook, Word, Excel und dem Online-Speicher OneDrive."))

# 2 drei Programme
b = ""
for i,(name,col,lines,sub) in enumerate([
    ("Outlook",OUTLOOK,["E-Mails + Termine","Briefkasten +","Terminkalender"],["Störungsmeldung","Wartungstermin"]),
    ("Word",WORD,["Texte + Dokumente","Schreibmaschine",""],["Aushang","Protokoll"]),
    ("Excel",EXCEL,["Zahlen + Listen","Rechenheft mit","Tabellen"],["Mieterliste","Stromverbrauch"])]):
    b += card(70+i*390,150,360,470,col,name,lines,sub)
slides.append(("02-drei-programme","Die drei Programme",b,"Drei Karten: Outlook für E-Mails und Termine, Word für Texte und Dokumente, Excel für Zahlen und Listen, jeweils mit Alltagsvergleich und Beispiel aus dem Haus Lichtblick."))

# 3 Haus Lichtblick
b = ""
floors = ["4. OG","3. OG","2. OG","1. OG","EG"]
bx, by, bw, fh = 120, 170, 360, 80
b += f'<polygon points="{bx-20},{by} {bx+bw/2},{by-40} {bx+bw+20},{by}" fill="{NAVY}"/>'
for i,f in enumerate(floors):
    y = by + i*fh
    b += rect(bx,y,bw,fh,"#F3F5F8",NAVY,0,3)
    b += text(bx+20,y+50,f,24,"bold",NAVY)
    for k in range(4):
        if f == "EG" and k < 2: continue
        b += rect(bx+130+k*55,y+20,38,40,"#FFF4D6" if (i+k)%3 else "#FFFFFF",MUTED,4,1.5)
b += rect(bx+140,by+4*fh+22,80,58,NAVY,rx=4)
facts = [("Adresse","Sonnenallee 45, 10115 Berlin"),("Gebäude","Bürogebäude, Baujahr 2010"),("Geschosse","Erdgeschoss + 4 Obergeschosse"),("Fläche","ca. 3.200 m² Nutzfläche"),("Mieter","12 Firmen")]
for i,(k,v) in enumerate(facts):
    y = 200 + i*66
    b += text(580,y,k,22,"bold",MUTED); b += text(760,y,v,28,fill=INK)
b += rect(580,540,640,96,"#FFF4D6",ACCENT,10,2)
b += text(604,580,"Ihre Rolle:",22,"bold",MUTED)
b += text(604,616,"Koordination des Facility Managements",28,"bold",INK)
slides.append(("03-haus-lichtblick","Ihr Arbeitsplatz: Haus Lichtblick",b,"Schematisches Bürogebäude mit Erdgeschoss und vier Obergeschossen, daneben Adresse Sonnenallee 45 in Berlin, Baujahr 2010, 3.200 Quadratmeter, 12 Mieter. Ihre Rolle: Koordination des Facility Managements."))

# 4 Desktop, Taskleiste, Startmenü
b = ""
sx, sy, sw, sh = 90, 150, 700, 440
b += rect(sx,sy,sw,sh,"#2E4A6B",INK,14,4)
b += rect(sx+12,sy+12,sw-24,sh-82,"#DCE8F5",rx=8)
for k,(lab) in enumerate(["Papierkorb","Ordner"]):
    b += rect(sx+40,sy+40+k*100,56,56,"#FFFFFF",MUTED,8,1.5); b += text(sx+68,sy+120+k*100,lab,16,fill=INK,anchor="middle")
b += rect(sx+12,sy+sh-62,sw-24,50,"#F3F5F8",rx=6)
cx = sx+sw/2
# start icon (4 squares)
for dx,dy in [(0,0),(14,0),(0,14),(14,14)]:
    b += rect(cx-100+dx,sy+sh-51+dy,12,12,OUTLOOK,rx=1)
for k,col in enumerate([OUTLOOK,WORD,EXCEL]):
    x = cx-50+k*45
    b += rect(x,sy+sh-52,30,30,col,rx=5)
    b += f'<line x1="{x+8}" y1="{sy+sh-16}" x2="{x+22}" y2="{sy+sh-16}" stroke="{MUTED}" stroke-width="3" stroke-linecap="round"/>'
def callout(x1,y1,x2,y2,lab,desc,col):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="3"/><circle cx="{x1}" cy="{y1}" r="7" fill="{col}"/>'
    s += text(x2+12,y2+8,lab,28,"bold",col); s += text(x2+12,y2+42,desc,22,fill=MUTED)
    return s
b += callout(sx+300,sy+180,830,220,"Desktop","Ihre Arbeitsfläche – wie ein Schreibtisch",NAVY)
b += callout(sx+560,sy+sh-37,830,420,"Taskleiste","zeigt geöffnete Programme",EXCEL)
b += f'<path d="M{cx-86} {sy+sh-6} C {cx-86} 640, 760 640, 830 560" fill="none" stroke="{OUTLOOK}" stroke-width="3"/><circle cx="{cx-86}" cy="{sy+sh-6}" r="7" fill="{OUTLOOK}"/>'
b += text(842,568,"Startmenü",28,"bold",OUTLOOK); b += text(842,602,"Windows-Symbol – alle Programme",22,fill=MUTED)
slides.append(("04-desktop-taskleiste","Desktop, Taskleiste und Startmenü",b,"Schematischer Windows-11-Bildschirm: die blaue Arbeitsfläche ist der Desktop, unten die Taskleiste mit Programmsymbolen, in ihrer Mitte das Windows-Symbol für das Startmenü."))

# 5 Programme starten
b = ""
steps = [("1","Startmenü öffnen","Windows-Symbol in","der Taskleiste klicken"),("2","Programm suchen","Namen ins Suchfeld tippen","oder „Alle“ anklicken"),("3","Programm anklicken","Einmal klicken genügt –","das Fenster öffnet sich")]
for i,(n,h,l1,l2) in enumerate(steps):
    x = 70+i*390
    b += f'<path d="M{x} 200 h300 l50 140 l-50 140 h-300 l50 -140 z" fill="{["#E6F0FA","#E8EEF9","#E7F4EC"][i]}" stroke="{[OUTLOOK,WORD,EXCEL][i]}" stroke-width="3"/>'
    b += f'<circle cx="{x+120}" cy="255" r="30" fill="{[OUTLOOK,WORD,EXCEL][i]}"/>'
    b += text(x+120,267,n,32,"bold","#FFFFFF","middle")
    b += text(x+195,335,h,28,"bold",INK,"middle")
    b += text(x+195,385,l1,21,fill=MUTED,anchor="middle")
    b += text(x+195,415,l2,21,fill=MUTED,anchor="middle")
b += rect(170,535,940,80,"#E7F4EC",EXCEL,10,2)
b += text(640,585,"Tipp: Die Windows-Taste auf der Tastatur öffnet das Startmenü auch.",26,"bold",INK,"middle")
slides.append(("05-programme-starten","Programme starten",b,"Drei Schritte als Pfeile: Startmenü öffnen, Programm suchen, Programm anklicken. Tipp: Die Windows-Taste öffnet das Startmenü."))

# 6 Fenster anordnen
b = ""
def screen(x,y,w,h,label):
    s = rect(x,y,w,h,"#2E4A6B",INK,12,3)+rect(x+10,y+10,w-20,h-20,"#DCE8F5",rx=6)
    s += text(x+w/2,y+h+40,label,24,"bold",INK,"middle")
    return s
def win(x,y,w,h,col,name):
    s = rect(x,y,w,h,"#FFFFFF",col,6,2)
    s += f'<path d="M{x} {y+6} a6 6 0 0 1 6 -6 h{w-12} a6 6 0 0 1 6 6 v22 h-{w} z" fill="{col}"/>'
    s += text(x+w/2,y+20,name,16,"bold","#FFFFFF","middle")
    for k in range(4):
        s += f'<line x1="{x+14}" y1="{y+50+k*26}" x2="{x+w-14-(k%2)*30}" y2="{y+50+k*26}" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>'
    return s
b += screen(90,170,500,320,"Zwei Fenster: an den Rand ziehen")
b += win(100,180,235,300,WORD,"Word")+win(345,180,235,300,EXCEL,"Excel")
b += f'<path d="M300 140 h-150" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/><path d="M380 140 h150" stroke="{ACCENT}" stroke-width="5" marker-end="url(#pf)"/>'
b += '<defs><marker id="pf" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="'+ACCENT+'"/></marker></defs>'
b += screen(690,170,500,320,"Drei Fenster: Andocklayout")
b += win(700,180,155,300,OUTLOOK,"Outlook")+win(862,180,155,300,WORD,"Word")+win(1024,180,156,300,EXCEL,"Excel")
b += rect(170,560,940,70,"#FFF4D6",ACCENT,10,2)
b += text(640,605,"Andocklayout: Maus über „Maximieren“ (Quadrat oben rechts) halten",24,"bold",INK,"middle")
slides.append(("06-fenster-anordnen","Fenster nebeneinander anordnen",b,"Links ein Bildschirm mit Word und Excel nebeneinander, an den Rand gezogen. Rechts ein Bildschirm mit Outlook, Word und Excel in drei Spalten über ein Andocklayout. Hinweis: Andocklayout erscheint, wenn die Maus über der Schaltfläche Maximieren steht."))

for i,(name,title,body,desc) in enumerate(slides,1):
    open(f"{OUT}/{name}.svg","w",encoding="utf-8").write(frame(i,title,body,desc))
print("ok", len(slides))
