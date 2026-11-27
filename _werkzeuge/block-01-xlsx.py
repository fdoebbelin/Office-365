# Excel-Datei Block 01 erzeugen (Mieterliste, Daten aus der Referenzliste).
# Voraussetzung: openpyxl
# Aufruf: python3 _werkzeuge/block-01-xlsx.py _resources/Grundkurs/Block-01/Block-01-Mieterliste.xlsx
import sys, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
out = sys.argv[1]
rows = [
 ("TechSolutions","1. OG",420,"Anna Klein",dt.date(2018,3,1),1260),
 ("DesignWerk","2. OG",310,"Michael Braun",dt.date(2019,7,15),930),
 ("Consulting Plus","3. OG",520,"Sarah Meyer",dt.date(2017,1,1),1560),
 ("Steuerbüro Hahn","1. OG",180,"Jürgen Hahn",dt.date(2020,10,1),540),
 ("Praxis am Park","2. OG",260,"Lena Ott",dt.date(2021,4,1),780),
 ("Lernwerk Akademie","3. OG",240,"Tim Rauch",dt.date(2022,2,15),720),
 ("Kanzlei Berg & Partner","4. OG",300,"Nina Berg",dt.date(2016,9,1),900),
 ("Grünraum Architekten","1. OG",150,"Paul Grün",dt.date(2023,6,1),450),
]
for r in rows: assert r[2]*3 == r[5], r
F = "Aptos"
wb = Workbook(); ws = wb.active; ws.title = "Mieterliste"
ws["A1"] = "Mieterliste Haus Lichtblick"; ws["A1"].font = Font(name=F, size=16, bold=True, color="1F3A5F")
ws["A2"] = "Auszug: 8 von 12 Mietern · Sonnenallee 45, 10115 Berlin"; ws["A2"].font = Font(name=F, size=11, italic=True, color="5B6472")
head = ["Firma","Etage","Fläche m²","Ansprechperson","Mietbeginn","Nebenkosten €/Monat"]
thin = Side(style="thin", color="BFC7D2")
for c, h in enumerate(head, 1):
    cell = ws.cell(row=4, column=c, value=h)
    cell.font = Font(name=F, bold=True, color="FFFFFF"); cell.fill = PatternFill("solid", fgColor="107C41")
    cell.alignment = Alignment(horizontal="left" if c in (1,2,4) else "right", vertical="center"); cell.border = Border(bottom=thin)
for i, r in enumerate(rows, 5):
    for c, v in enumerate(r, 1):
        cell = ws.cell(row=i, column=c, value=v); cell.font = Font(name=F); cell.border = Border(bottom=thin)
        if i % 2 == 0: cell.fill = PatternFill("solid", fgColor="EEF5F0")
    ws.cell(row=i, column=3).number_format = '#,##0'
    ws.cell(row=i, column=5).number_format = 'DD.MM.YYYY'
    ws.cell(row=i, column=6).number_format = '#,##0 "€"'
n = 5 + len(rows) + 1
ws.cell(row=n, column=1, value="Die Nebenkostenvorauszahlung beträgt 3 € je m² und Monat.").font = Font(name=F, italic=True, color="5B6472")
ws.cell(row=n+1, column=1, value="Übungsdatei Block 01 · Namen, Firmen und Adressen sind erfunden.").font = Font(name=F, italic=True, color="5B6472", size=9)
for col, w in zip("ABCDEF", [26, 9, 12, 18, 13, 21]): ws.column_dimensions[col].width = w
ws.row_dimensions[4].height = 22
ws.freeze_panes = "A5"
ws.print_title_rows = "4:4"
ws.page_setup.orientation = "landscape"; ws.page_setup.fitToWidth = 1
wb.properties.title = "Mieterliste Haus Lichtblick"
wb.save(out); print("geschrieben", out)
