# Excel-Dateien Block 10 erzeugen (Stromverbrauch 2025 und Fläche je Etage, Daten aus der Referenzliste).
# Voraussetzung: openpyxl
# Aufruf: python3 _werkzeuge/block-10-xlsx.py _resources/Grundkurs/Block-10
# Übungsdatei und Lösung enthalten nur feste Werte (keine Formeln); die Lösung zusätzlich zwei Diagramme.
import sys, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList

OUT = sys.argv[1]
F = "Aptos"; SOFT = "E7F4EC"; MUTED = "5B6472"; NAVY = "1F3A5F"
thin = Side(style="thin", color="BFC7D2")

MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
VERBRAUCH = [4850, 4670, 4530, 4240, 3890, 3540, 3320, 3240, 3360, 3650, 4030, 4530]
SUMME = sum(VERBRAUCH); assert SUMME == 47850
assert MONATE[VERBRAUCH.index(max(VERBRAUCH))] == "Januar" and MONATE[VERBRAUCH.index(min(VERBRAUCH))] == "August"
MIETER = [("TechSolutions", "1. OG", 420), ("DesignWerk", "2. OG", 310), ("Consulting Plus", "3. OG", 520), ("Steuerbüro Hahn", "1. OG", 180),
          ("Praxis am Park", "2. OG", 260), ("Lernwerk Akademie", "3. OG", 240), ("Kanzlei Berg & Partner", "4. OG", 300), ("Grünraum Architekten", "1. OG", 150)]
ETAGEN = ["1. OG", "2. OG", "3. OG", "4. OG"]
FLAECHE = [sum(m[2] for m in MIETER if m[1] == e) for e in ETAGEN]
assert FLAECHE == [750, 570, 760, 300] and sum(FLAECHE) == 2380
ANTEIL = [round(100 * f / sum(FLAECHE)) for f in FLAECHE]
assert ANTEIL == [32, 24, 32, 13], ANTEIL  # so zeigt Excel die Prozentwerte (gerundet)

def c(ws, ref, v, bold=False, italic=False, color=None, size=11, fmt=None):
    x = ws[ref]; x.value = v; x.font = Font(name=F, bold=bold, italic=italic, color=color, size=size)
    if fmt: x.number_format = fmt

def head(ws, row, names):
    for i, n in enumerate(names):
        x = ws.cell(row=row, column=i + 1, value=n)
        x.font = Font(name=F, bold=True); x.fill = PatternFill("solid", fgColor=SOFT); x.border = Border(bottom=thin)

def build(loesung):
    note = ("Lösungsdatei" if loesung else "Übungsdatei") + " Block 10 · Namen, Firmen und Adressen sind erfunden."
    wb = Workbook(); ws = wb.active; ws.title = "Strom 2025"
    c(ws, "A1", "Stromverbrauch Haus Lichtblick 2025", bold=True, color=NAVY, size=14)
    head(ws, 3, ["Monat", "Verbrauch (kWh)"])
    for i, (m, v) in enumerate(zip(MONATE, VERBRAUCH)):
        c(ws, f"A{4+i}", m); c(ws, f"B{4+i}", v, fmt="#,##0")
    c(ws, "A16", "Summe", bold=True); c(ws, "B16", SUMME, bold=True, fmt="#,##0")
    c(ws, "A18", note, italic=True, color=MUTED, size=9)
    ws.column_dimensions["A"].width = 14; ws.column_dimensions["B"].width = 17
    if loesung:
        ch = BarChart(); ch.type = "col"; ch.grouping = "clustered"
        ch.title = "Stromverbrauch Haus Lichtblick 2025"
        ch.y_axis.title = "Verbrauch in kWh"; ch.x_axis.title = "Monat"
        ch.add_data(Reference(ws, min_col=2, min_row=3, max_row=15), titles_from_data=True)
        ch.set_categories(Reference(ws, min_col=1, min_row=4, max_row=15))
        ch.legend = None; ch.x_axis.delete = False; ch.y_axis.delete = False
        ch.width = 18; ch.height = 9.5
        ws.add_chart(ch, "D3")
    ws2 = wb.create_sheet("Flächen")
    c(ws2, "A1", "Vermietete Fläche je Etage", bold=True, color=NAVY, size=14)
    head(ws2, 3, ["Etage", "Fläche m²"])
    for i, (e, f) in enumerate(zip(ETAGEN, FLAECHE)):
        c(ws2, f"A{4+i}", e); c(ws2, f"B{4+i}", f, fmt="#,##0")
    c(ws2, "A8", "Summe", bold=True); c(ws2, "B8", sum(FLAECHE), bold=True, fmt="#,##0")
    c(ws2, "A10", "Quelle: Mieterliste (8 von 12 Mietern), im Erdgeschoss keine Mieter.", italic=True, color=MUTED, size=9)
    c(ws2, "A11", note, italic=True, color=MUTED, size=9)
    ws2.column_dimensions["A"].width = 12; ws2.column_dimensions["B"].width = 12
    if loesung:
        pc = PieChart(); pc.title = "Vermietete Fläche je Etage"
        pc.add_data(Reference(ws2, min_col=2, min_row=3, max_row=7), titles_from_data=True)
        pc.set_categories(Reference(ws2, min_col=1, min_row=4, max_row=7))
        pc.dataLabels = DataLabelList(); pc.dataLabels.showPercent = True
        pc.width = 12; pc.height = 9
        ws2.add_chart(pc, "D3")
    wb.properties.title = "Diagramme Haus Lichtblick" + (" (Lösung)" if loesung else "")
    return wb

for loesung, name in [(False, "Block-10-Diagramme.xlsx"), (True, "Block-10-Loesung-Diagramme.xlsx")]:
    p = os.path.join(OUT, name); build(loesung).save(p); print("geschrieben", p)
