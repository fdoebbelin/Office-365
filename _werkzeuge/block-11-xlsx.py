# Excel-Datei Block 11 erzeugen (Stromverbrauch 2025 mit fertigem Säulendiagramm, Daten aus der Referenzliste)
# und das Diagramm zusätzlich als SVG für die Lösungsdatei des Berichts.
# Voraussetzung: openpyxl
# Aufruf: python3 _werkzeuge/block-11-xlsx.py _resources/Grundkurs/Block-11 <pfad/diagramm.svg>
#   danach: magick -density 150 <pfad/diagramm.svg> <pfad/diagramm.png>  (für block-11-docx.js)
import sys, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side
from openpyxl.chart import BarChart, Reference

OUT, SVG = sys.argv[1], sys.argv[2]
F = "Aptos"; SOFT = "E7F4EC"; MUTED = "5B6472"; NAVY = "1F3A5F"; GREEN = "#107C41"
thin = Side(style="thin", color="BFC7D2")
MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
VERBRAUCH = [4850, 4670, 4530, 4240, 3890, 3540, 3320, 3240, 3360, 3650, 4030, 4530]
assert sum(VERBRAUCH) == 47850

wb = Workbook(); ws = wb.active; ws.title = "Strom 2025"
def c(ref, v, **k):
    x = ws[ref]; x.value = v; x.font = Font(name=F, bold=k.get("bold", False), italic=k.get("italic", False), color=k.get("color"), size=k.get("size", 11))
    if "fmt" in k: x.number_format = k["fmt"]
c("A1", "Stromverbrauch Haus Lichtblick 2025", bold=True, color=NAVY, size=14)
for i, h in enumerate(["Monat", "Verbrauch (kWh)"]):
    x = ws.cell(row=3, column=i + 1, value=h); x.font = Font(name=F, bold=True); x.fill = PatternFill("solid", fgColor=SOFT); x.border = Border(bottom=thin)
for i, (m, v) in enumerate(zip(MONATE, VERBRAUCH)):
    c(f"A{4+i}", m); c(f"B{4+i}", v, fmt="#,##0")
c("A16", "Summe", bold=True); c("B16", sum(VERBRAUCH), bold=True, fmt="#,##0")
c("A18", "Übungsdatei Block 11 · Namen, Firmen und Adressen sind erfunden.", italic=True, color=MUTED, size=9)
ws.column_dimensions["A"].width = 14; ws.column_dimensions["B"].width = 17
ch = BarChart(); ch.type = "col"; ch.grouping = "clustered"; ch.title = "Stromverbrauch Haus Lichtblick 2025"
ch.y_axis.title = "Verbrauch in kWh"; ch.x_axis.title = "Monat"; ch.legend = None
ch.x_axis.delete = False; ch.y_axis.delete = False
ch.add_data(Reference(ws, min_col=2, min_row=3, max_row=15), titles_from_data=True)
ch.set_categories(Reference(ws, min_col=1, min_row=4, max_row=15))
ch.width = 18; ch.height = 9.5
ws.add_chart(ch, "D3")
wb.properties.title = "Stromverbrauch 2025 mit Diagramm"
p = os.path.join(OUT, "Block-11-Strom.xlsx"); wb.save(p); print("geschrieben", p)

# Diagramm als SVG (so ähnlich, wie es nach dem Einfügen in Word aussieht)
W, H = 900, 480; px, py, pw, ph = 110, 70, 750, 320
s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#fff"/>',
     f'<text x="{W/2}" y="40" font-family="Aptos, Arial, sans-serif" font-size="24" font-weight="bold" text-anchor="middle" fill="#1E2430">Stromverbrauch Haus Lichtblick 2025</text>']
for k in range(6):
    y = py + ph - ph * k / 5
    s.append(f'<line x1="{px}" y1="{y}" x2="{px+pw}" y2="{y}" stroke="#D5DAE1"/><text x="{px-10}" y="{y+5}" font-family="Aptos, Arial, sans-serif" font-size="14" text-anchor="end" fill="#5B6472">{f"{k*1000:,}".replace(",", ".")}</text>')
bw = pw / 12
for i, v in enumerate(VERBRAUCH):
    h = ph * v / 5000
    s.append(f'<rect x="{px+i*bw+bw*0.2}" y="{py+ph-h}" width="{bw*0.6}" height="{h}" fill="{GREEN}"/>')
    s.append(f'<text x="{px+i*bw+bw/2}" y="{py+ph+22}" font-family="Aptos, Arial, sans-serif" font-size="14" text-anchor="middle" fill="#5B6472">{MONATE[i][:3]}</text>')
s.append(f'<text x="{px+pw/2}" y="{py+ph+55}" font-family="Aptos, Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#5B6472">Monat</text>')
s.append(f'<text x="35" y="{py+ph/2}" font-family="Aptos, Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="#5B6472" transform="rotate(-90 35 {py+ph/2})">Verbrauch in kWh</text></svg>')
open(SVG, "w", encoding="utf-8").write("".join(s)); print("geschrieben", SVG)
