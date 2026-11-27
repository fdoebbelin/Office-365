# Excel-Dateien Block 09 erzeugen (Strom 2025, Nebenkosten, Inventar – Daten aus der Referenzliste).
# Voraussetzung: openpyxl
# Aufruf: python3 _werkzeuge/block-09-xlsx.py _resources/Grundkurs/Block-09
#
# Die Lösungsdatei enthält Formeln mit vorab berechneten Ergebnissen (cache_values), damit sie auch
# in der „Geschützten Ansicht“ Werte zeigt. Die erwarteten Ergebnisse sind unten mit assert geprüft
# und stehen so im Übungsblatt.
# In der Datei stehen Funktionen englisch (SUM, AVERAGE, COUNT) – so verlangt es das Dateiformat;
# das deutsche Excel zeigt sie als SUMME, MITTELWERT, ANZAHL an.
import sys, os, re, zipfile, shutil
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

OUT = sys.argv[1]
F = "Aptos"; GREEN = "107C41"; SOFT = "E7F4EC"; MUTED = "5B6472"; NAVY = "1F3A5F"
thin = Side(style="thin", color="BFC7D2")

MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
ZAEHLER = [125450, 130120, 134650, 138890, 142780, 146320, 149640, 152880, 156240, 159890, 163920, 168450]
VERBRAUCH = [4850, 4670, 4530, 4240, 3890, 3540, 3320, 3240, 3360, 3650, 4030, 4530]  # Referenzliste
for i in range(1, 12):
    assert ZAEHLER[i] - ZAEHLER[i - 1] == VERBRAUCH[i], MONATE[i]
SUMME = sum(VERBRAUCH); MITTEL = SUMME / 12
assert SUMME == 47850 and MITTEL == 3987.5 and min(VERBRAUCH) == 3240 and max(VERBRAUCH) == 4850
assert MONATE[VERBRAUCH.index(3240)] == "August"

MIETER = [("TechSolutions", "1. OG", 420, 1260), ("DesignWerk", "2. OG", 310, 930), ("Consulting Plus", "3. OG", 520, 1560),
          ("Steuerbüro Hahn", "1. OG", 180, 540), ("Praxis am Park", "2. OG", 260, 780), ("Lernwerk Akademie", "3. OG", 240, 720),
          ("Kanzlei Berg & Partner", "4. OG", 300, 900), ("Grünraum Architekten", "1. OG", 150, 450)]
for m in MIETER: assert m[2] * 3 == m[3]
NK = sum(m[3] for m in MIETER); FL = sum(m[2] for m in MIETER)
assert NK == 7140 and FL == 2380

INVENTAR = [("Allzweckreiniger", 15, 10, "Flaschen"), ("Müllbeutel 120 l", 200, 150, "Stück"), ("Handtuchpapier", 50, 30, "Pakete"),
            ("Toilettenpapier", 80, 60, "Rollen"), ("Glasreiniger", 8, 10, "Flaschen"), ("Bodenreiniger", 12, 8, "Flaschen"),
            ("Desinfektionsmittel", 6, 5, "Flaschen"), ("Schwämme", 25, 20, "Stück"), ("Einweghandschuhe", 5, 10, "Pakete"),
            ("Wischmopps", 4, 3, "Stück")]
NACH = ["Ja" if b < m else "Nein" for _, b, m, _ in INVENTAR]
assert [a for (a, *_), n in zip(INVENTAR, NACH) if n == "Ja"] == ["Glasreiniger", "Einweghandschuhe"]
assert [a for a, _, _, e in INVENTAR if e == "Flaschen"] == ["Allzweckreiniger", "Glasreiniger", "Bodenreiniger", "Desinfektionsmittel"]
assert sorted(INVENTAR, key=lambda r: r[1])[0][0] == "Wischmopps"

def cell(ws, ref, v, bold=False, fmt=None, italic=False, color=None, size=None):
    c = ws[ref]; c.value = v
    c.font = Font(name=F, bold=bold, italic=italic, color=color, size=size or 11)
    if fmt: c.number_format = fmt
    return c

def header(ws, row, names):
    for i, n in enumerate(names):
        c = ws.cell(row=row, column=i + 1, value=n)
        c.font = Font(name=F, bold=True); c.fill = PatternFill("solid", fgColor=SOFT); c.border = Border(bottom=thin)

def title(ws, t, sub):
    cell(ws, "A1", t, bold=True, color=NAVY, size=14); cell(ws, "A2", sub, italic=True, color=MUTED)

def build(loesung):
    wb = Workbook(); vals = {}
    note = ("Lösungsdatei" if loesung else "Übungsdatei") + " Block 09 · Namen, Firmen und Adressen sind erfunden."
    # Blatt 1: Strom 2025
    ws = wb.active; ws.title = "Strom 2025"
    title(ws, "Stromverbrauch Haus Lichtblick 2025", "Zählerstand jeweils am Monatsende")
    header(ws, 3, ["Monat", "Zählerstand (kWh)", "Verbrauch (kWh)"])
    for i, m in enumerate(MONATE):
        r = 4 + i
        cell(ws, f"A{r}", m); cell(ws, f"B{r}", ZAEHLER[i], fmt="#,##0")
        if i == 0:
            cell(ws, f"C{r}", VERBRAUCH[0], fmt="#,##0")
        elif loesung:
            cell(ws, f"C{r}", f"=B{r}-B{r-1}", fmt="#,##0"); vals[("Strom 2025", f"C{r}")] = VERBRAUCH[i]
        else:
            ws[f"C{r}"].number_format = "#,##0"  # leere Zelle schon formatiert: die Ergebnisse erscheinen mit Trennzeichen
    cell(ws, "D4", "Januar: Wert vom Stromversorger", italic=True, color=MUTED)
    labels = [("Summe", "=SUM(C4:C15)", SUMME), ("Mittelwert", "=AVERAGE(C4:C15)", MITTEL), ("Kleinster Wert", "=MIN(C4:C15)", min(VERBRAUCH)),
              ("Größter Wert", "=MAX(C4:C15)", max(VERBRAUCH)), ("Anzahl Monate", "=COUNT(C4:C15)", 12)]
    for k, (lab, f, v) in enumerate(labels):
        r = 17 + k
        cell(ws, f"A{r}", lab, bold=True)
        if loesung:
            cell(ws, f"C{r}", f, bold=True, fmt="#,##0.0" if lab == "Mittelwert" else "#,##0"); vals[("Strom 2025", f"C{r}")] = v
        else:
            ws[f"C{r}"].number_format = "#,##0.0" if lab == "Mittelwert" else "#,##0"
    cell(ws, "A23", note, italic=True, color=MUTED, size=9)
    for col, w in zip("ABCD", [16, 19, 17, 32]): ws.column_dimensions[col].width = w
    # Blatt 2: Nebenkosten
    ws = wb.create_sheet("Nebenkosten")
    title(ws, "Nebenkostenvorauszahlung der Mieter", "3 € je m² und Monat")
    header(ws, 3, ["Firma", "Etage", "Fläche m²", "Nebenkosten €/Monat"])
    for i, (fi, et, fl, nk) in enumerate(MIETER):
        r = 4 + i
        cell(ws, f"A{r}", fi); cell(ws, f"B{r}", et); cell(ws, f"C{r}", fl, fmt="#,##0")
        cell(ws, f"D{r}", nk, fmt='#,##0.00 "€"' if loesung else "General")
    cell(ws, "A12", "Summe", bold=True)
    if loesung:
        cell(ws, "C12", "=SUM(C4:C11)", bold=True, fmt="#,##0"); vals[("Nebenkosten", "C12")] = FL
        cell(ws, "D12", "=SUM(D4:D11)", bold=True, fmt='#,##0.00 "€"'); vals[("Nebenkosten", "D12")] = NK
    cell(ws, "A14", note, italic=True, color=MUTED, size=9)
    for col, w in zip("ABCD", [24, 9, 11, 21]): ws.column_dimensions[col].width = w
    # Blatt 3: Inventar
    ws = wb.create_sheet("Inventar")
    title(ws, "Inventar Reinigungsmaterial – Lagerraum EG-01", "Nachbestellen: Bestand unter der Mindestmenge")
    header(ws, 3, ["Artikel", "Bestand", "Mindestmenge", "Einheit", "Nachbestellen"])
    for i, ((a, b, m, e), n) in enumerate(zip(INVENTAR, NACH)):
        r = 4 + i
        for c, v in zip("ABCDE", (a, b, m, e, n)): cell(ws, f"{c}{r}", v)
    if loesung: ws.auto_filter.ref = "A3:E13"
    cell(ws, "A15", note, italic=True, color=MUTED, size=9)
    for col, w in zip("ABCDE", [21, 10, 15, 11, 15]): ws.column_dimensions[col].width = w
    if loesung: wb.calculation.fullCalcOnLoad = True
    wb.properties.title = "Auswertung Haus Lichtblick" + (" (Lösung)" if loesung else "")
    return wb, vals

def cache_values(path, sheetnames, values):
    """Trägt die Ergebnisse der Formelzellen ein: values = {(blatt, "C5"): wert}."""
    idx = {n: i + 1 for i, n in enumerate(sheetnames)}
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            m = re.match(r"xl/worksheets/sheet(\d+)\.xml$", item.filename)
            if m:
                xml = data.decode("utf-8")
                for (sh, ref), val in values.items():
                    if idx[sh] != int(m.group(1)): continue
                    pat = re.compile(r'(<c r="%s"[^>]*>)(<f>[^<]*</f>)(<v\s*/>|<v>[^<]*</v>)?(</c>)' % ref)
                    xml, n = pat.subn(lambda mm: mm.group(1) + mm.group(2) + "<v>%s</v>" % val + mm.group(4), xml)
                    assert n == 1, (sh, ref)
                data = xml.encode("utf-8")
            zout.writestr(item, data)
    shutil.move(tmp, path)

wb, _ = build(False)
p = os.path.join(OUT, "Block-09-Auswertung.xlsx"); wb.save(p); print("geschrieben", p)
wb, vals = build(True)
p = os.path.join(OUT, "Block-09-Loesung-Auswertung.xlsx"); wb.save(p); cache_values(p, wb.sheetnames, vals); print("geschrieben", p)
