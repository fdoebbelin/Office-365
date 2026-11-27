# Excel-Dateien Block 08 erzeugen (Inventarliste Reinigungsmaterial, Daten aus der Referenzliste).
# Voraussetzung: openpyxl
# Aufruf: python3 _werkzeuge/block-08-xlsx.py _resources/Grundkurs/Block-08
#
# Die Lösungsdatei enthält Formeln. Damit sie auch in der „Geschützten Ansicht“ Ergebnisse zeigt,
# trägt das Skript die vorab berechneten Werte als zwischengespeicherte Ergebnisse (<v>) ein.
import sys, os, re, zipfile, shutil
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

OUT = sys.argv[1]
F = "Aptos"
GREEN = "107C41"; SOFT = "E7F4EC"; MUTED = "5B6472"; NAVY = "1F3A5F"
thin = Side(style="thin", color="BFC7D2")

# Referenzliste: Inventar – Reinigungsmaterial
ROWS = [
    ("Allzweckreiniger", "Lagerraum EG-01", 15, 10, "Flaschen"),
    ("Müllbeutel 120 l", "Lagerraum EG-01", 200, 150, "Stück"),
    ("Handtuchpapier", "Lagerraum EG-01", 50, 30, "Pakete"),
    ("Toilettenpapier", "Lagerraum EG-01", 80, 60, "Rollen"),
    ("Glasreiniger", "Lagerraum EG-01", 8, 10, "Flaschen"),
    ("Bodenreiniger", "Lagerraum EG-01", 12, 8, "Flaschen"),
    ("Desinfektionsmittel", "Lagerraum EG-01", 6, 5, "Flaschen"),
    ("Schwämme", "Lagerraum EG-01", 25, 20, "Stück"),
    ("Einweghandschuhe", "Lagerraum EG-01", 5, 10, "Pakete"),
    ("Wischmopps", "Lagerraum EG-01", 4, 3, "Stück"),
]
HEAD = ["Artikel", "Lagerort", "Bestand", "Mindestmenge", "Einheit"]
FIRST = 5  # erste Datenzeile

# Erwartete Ergebnisse (stehen so im Übungsblatt)
DIFF = [r[2] - r[3] for r in ROWS]
assert DIFF == [5, 50, 20, 20, -2, 4, 1, 5, -5, 1], DIFF
assert [r[0] for r, d in zip(ROWS, DIFF) if d < 0] == ["Glasreiniger", "Einweghandschuhe"]
assert max(DIFF) == 50 and ROWS[DIFF.index(50)][0] == "Müllbeutel 120 l"
assert ROWS[4][2] == 8  # C9 in der Übungsdatei

def base(ws, n_rows, note):
    ws["A1"] = "Inventar Reinigungsmaterial – Lagerraum EG-01"
    ws["A1"].font = Font(name=F, size=14, bold=True, color=NAVY)
    ws["A2"] = "Stand:"; ws["A2"].font = Font(name=F)
    for c, h in enumerate(HEAD, 1):
        ws.cell(row=4, column=c, value=h).font = Font(name=F)
    for i, r in enumerate(ROWS[:n_rows]):
        for c, v in enumerate(r, 1):
            ws.cell(row=FIRST + i, column=c, value=v).font = Font(name=F)
    ws.cell(row=FIRST + len(ROWS) + 1, column=1, value=note).font = Font(name=F, italic=True, size=9, color=MUTED)

def cache_values(path, values):
    """Trägt in der ersten Tabelle die Ergebnisse der Formelzellen ein: values = {"F5": 5, ...}."""
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "xl/worksheets/sheet1.xml":
                xml = data.decode("utf-8")
                for ref, val in values.items():
                    pat = re.compile(r'(<c r="%s"[^>]*>)(<f>[^<]*</f>)(<v\s*/>|<v>[^<]*</v>)?(</c>)' % ref)
                    xml, n = pat.subn(lambda m: m.group(1) + m.group(2) + "<v>%s</v>" % val + m.group(4), xml)
                    assert n == 1, ref
                data = xml.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, path)

# Übungsdatei: 5 Artikel eingetragen, 5 tippen die Lernenden; keine Formatierung, Standardbreiten
wb = Workbook(); ws = wb.active; ws.title = "Inventar"
base(ws, 5, "Übungsdatei Block 08 · Namen, Firmen und Adressen sind erfunden.")
wb.properties.title = "Inventarliste Reinigungsmaterial"
p = os.path.join(OUT, "Block-08-Inventarliste.xlsx"); wb.save(p); print("geschrieben", p)

# Lösung: alle 10 Artikel, Kopfzeile fett mit Füllfarbe, Spaltenbreiten, Spalte Differenz mit Formeln
wb = Workbook(); ws = wb.active; ws.title = "Inventar"
base(ws, 10, "Lösungsdatei Block 08 · Namen, Firmen und Adressen sind erfunden.")
ws["B2"] = "(Datum Ihrer Eingabe)"; ws["B2"].font = Font(name=F, italic=True, color=MUTED)
ws.cell(row=4, column=6, value="Differenz")
for c in range(1, 7):
    cell = ws.cell(row=4, column=c)
    cell.font = Font(name=F, bold=True); cell.fill = PatternFill("solid", fgColor=SOFT); cell.border = Border(bottom=thin)
vals = {}
for i in range(len(ROWS)):
    r = FIRST + i
    ws.cell(row=r, column=6, value=f"=C{r}-D{r}").font = Font(name=F, bold=DIFF[i] < 0, color="B3261E" if DIFF[i] < 0 else None)
    vals[f"F{r}"] = DIFF[i]
for col, w in zip("ABCDEF", [21, 17, 9, 14, 10, 10]): ws.column_dimensions[col].width = w
ws.freeze_panes = "A5"
wb.calculation.fullCalcOnLoad = True
wb.properties.title = "Inventarliste Reinigungsmaterial (Lösung)"
p = os.path.join(OUT, "Block-08-Loesung-Inventarliste.xlsx"); wb.save(p); cache_values(p, vals); print("geschrieben", p)
