// Word-Dateien Block 09 erzeugen (Übungsblatt; die Excel-Dateien erzeugt block-09-xlsx.py).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-09-docx.js _resources/Grundkurs/Block-09
// Das Übungsblatt muss inhaltlich Grundkurs/Block-09-Uebungsblatt.md entsprechen.
const fs = require('fs');
const path = require('path');
const d = require('docx');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType,
  ShadingType, BorderStyle, AlignmentType, LevelFormat, Footer, PageBreak, PageNumber } = d;
const OUT = process.argv[2];
const FONT = 'Aptos';
const NAVY = '1F3A5F', LINE = 'BFC7D2', SOFT = 'EEF2F7', YELLOW = 'FFF4D6', BLUE = 'E6F0FA';
const CONTENT = 9070; // A4 width 11906 - 2*1418

const styles = {
  default: { document: { run: { font: FONT, size: 22 }, paragraph: { spacing: { after: 120, line: 288 } } } },
  paragraphStyles: [
    { id: 'Title', name: 'Title', basedOn: 'Normal', run: { font: FONT, size: 44, bold: true, color: NAVY }, paragraph: { spacing: { before: 0, after: 80 }, keepNext: true } },
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 30, bold: true, color: NAVY }, paragraph: { spacing: { before: 320, after: 120 }, keepNext: true, outlineLevel: 0 } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 24, bold: true, color: NAVY }, paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 1 } },
  ],
};
const numbering = { config: [
  { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 567, hanging: 283 } } } }] },
  { reference: 'steps', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 567, hanging: 340 } } } }] },
] };

// inline **bold** parsing
function runs(s, extra = {}) {
  return s.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map(t =>
    t.startsWith('**') ? new TextRun({ text: t.slice(2, -2), bold: true, ...extra }) : new TextRun({ text: t, ...extra }));
}
const P = (s, o = {}) => new Paragraph({ children: runs(s), ...o });
const H1 = s => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(s)] });
const H2 = s => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(s)] });
const TITLE = s => new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun(s)] });
const SUB = s => new Paragraph({ children: [new TextRun({ text: s, color: '5B6472', size: 24 })], spacing: { after: 240 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 6 } } });
const BUL = s => new Paragraph({ children: runs(s), numbering: { reference: 'bullets', level: 0 } });
let inst = 0;
const STEPS = arr => { inst++; return arr.map(s => new Paragraph({ children: runs(s), numbering: { reference: 'steps', level: 0, instance: inst } })); };
const BOX = (title, lines, fill = YELLOW, color = 'E8A33D') => lines.map((s, i) => new Paragraph({
  children: i === 0 && title ? [new TextRun({ text: title + ' ', bold: true }), ...runs(s)] : runs(s),
  shading: { type: ShadingType.CLEAR, color: 'auto', fill },
  border: { left: { style: BorderStyle.SINGLE, size: 24, color, space: 8 } },
  indent: { left: 170, right: 170 }, spacing: { before: i === 0 ? 120 : 0, after: i === lines.length - 1 ? 160 : 0 } }));
const CHECK = s => new Paragraph({ children: [new TextRun({ text: '☐  ', size: 26 }), ...runs(s)], indent: { left: 340 } });

const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const borders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };
function table(widths, rows, { header = true, minHeight } = {}) {
  return new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, ri) => new TableRow({ tableHeader: header && ri === 0, height: minHeight && ri > 0 ? { value: minHeight, rule: 'atLeast' } : undefined,
      children: r.map((c, ci) => new TableCell({ borders, width: { size: widths[ci], type: WidthType.DXA },
        shading: header && ri === 0 ? { type: ShadingType.CLEAR, color: 'auto', fill: SOFT } : undefined,
        margins: { top: 60, bottom: 60, left: 110, right: 110 },
        children: [new Paragraph({ spacing: { after: 0 }, children: runs(c, header && ri === 0 ? { bold: true } : {}) })] })) })) });
}
const footer = text => ({ default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.LEFT,
  border: { top: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 4 } },
  children: [new TextRun({ text, size: 16, color: '5B6472' }), new TextRun({ text: '\tSeite ', size: 16, color: '5B6472' }),
    new TextRun({ children: [PageNumber.CURRENT], size: 16, color: '5B6472' })],
  tabStops: [{ type: 'right', position: CONTENT }] })] }) });
const page = { size: { width: 11906, height: 16838 }, margin: { top: 1418, bottom: 1418, left: 1418, right: 1418 } };

async function save(name, title, children, foot) {
  const doc = new Document({ creator: 'Microsoft 365 im Facility Management', title, styles, numbering,
    sections: [{ properties: { page }, footers: footer(foot), children }] });
  fs.writeFileSync(path.join(OUT, name), await Packer.toBuffer(doc));
  console.log('geschrieben', name);
}
const VERBR = [['Januar', '4.850'], ['Februar', '4.670'], ['März', '4.530'], ['April', '4.240'], ['Mai', '3.890'], ['Juni', '3.540'],
  ['Juli', '3.320'], ['August', '3.240'], ['September', '3.360'], ['Oktober', '3.650'], ['November', '4.030'], ['Dezember', '4.530']];

(async () => {
  await save('Block-09-Uebungsblatt.docx', 'Übungsblatt Block 09 – Rechnen und Auswerten', [
    TITLE('Übungsblatt Block 09'),
    SUB('Rechnen und Auswerten'),
    P('**Sie brauchen:** einen PC mit Excel und die Übungsdatei Block-09-Auswertung.xlsx von der Seite zu Block 09. Die Lösungsdatei Block-09-Loesung-Auswertung.xlsx zeigt alle Ergebnisse – sehen Sie sie erst am Ende an.'),
    P('**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Petra Schönfeld von der Hausverwaltung möchte für die Jahresabrechnung wissen, wie viel Strom das Haus 2025 verbraucht hat, wie hoch die Nebenkostenvorauszahlungen der Mieter sind und welches Reinigungsmaterial nachbestellt werden muss. Die Datei hat dafür drei Tabellenblätter.'),
    H1('Aufgabe 1 – Datei vorbereiten'),
    ...STEPS(['Öffnen Sie Block-09-Auswertung.xlsx aus dem Ordner Downloads und klicken Sie auf **„Bearbeitung aktivieren“**.',
      'Speichern Sie die Datei in Dokumente\\Haus-Lichtblick unter dem Namen Auswertung-2025.',
      'Sehen Sie sich die drei Tabellenblätter an: **„Strom 2025“**, **„Nebenkosten“**, **„Inventar“** – ein Klick auf das Register unten wechselt das Blatt.']),
    H1('Aufgabe 2 – Den Verbrauch berechnen'),
    P('Blatt **„Strom 2025“**. Der Verbrauch für Januar steht schon da (Wert vom Stromversorger). Für die übrigen Monate rechnen Sie: Zählerstand dieses Monats minus Zählerstand des Vormonats.'),
    ...STEPS(['Klicken Sie auf **C5** (Februar) und geben Sie ein: =B5-B4, **Enter**.',
      'Klicken Sie wieder auf C5 und ziehen Sie das **Ausfüllkästchen** nach unten bis **C15** (Dezember). Oder doppelklicken Sie darauf.',
      'Klicken Sie auf **C10** (Juli). Welche Formel steht in der Bearbeitungsleiste, welcher Wert in der Zelle?',
      'Wie viel Strom hat das Haus im Dezember verbraucht?']),
    H1('Aufgabe 3 – Funktionen'),
    P('Bleiben Sie auf dem Blatt „Strom 2025“. Geben Sie in Spalte C die Funktionen ein – jeweils für den Bereich **C4:C15**.'),
    table([1200, 3200, 4670], [['Zelle', 'Beschriftung in Spalte A', 'Funktion'],
      ['C17', 'Summe', '=SUMME(C4:C15)'], ['C18', 'Mittelwert', '=MITTELWERT(C4:C15)'], ['C19', 'Kleinster Wert', '=MIN(C4:C15)'],
      ['C20', 'Größter Wert', '=MAX(C4:C15)'], ['C21', 'Anzahl Monate', '=ANZAHL(C4:C15)']]),
    ...STEPS(['Wie hoch war der Jahresverbrauch 2025?', 'In welchem Monat war der Verbrauch am kleinsten, in welchem am größten?',
      'Zeigt der Mittelwert eine Nachkommastelle? Klicken Sie auf C18 und dann auf **„Dezimalstelle löschen“**. Was ändert sich in der Zelle, was in der Bearbeitungsleiste?']),
    H1('Aufgabe 4 – Nebenkosten mit AutoSumme und Währung'),
    P('Blatt **„Nebenkosten“**.'),
    ...STEPS(['Klicken Sie auf **D12** (unter den Nebenkosten) und dann auf **„AutoSumme“** (Σ). Prüfen Sie den gestrichelten Bereich und drücken Sie **Enter**.',
      'Summieren Sie genauso die Fläche in **C12**.',
      'Markieren Sie **D4 bis D12** und wählen Sie auf der Registerkarte „Start“ in der Gruppe „Zahl“ das Format **„Währung“**.',
      'Wie hoch sind die Nebenkostenvorauszahlungen aller acht Mieter zusammen im Monat? Wie groß ist ihre Fläche zusammen?']),
    H1('Aufgabe 5 – Sortieren und Filtern'),
    P('Blatt **„Inventar“**.'),
    ...STEPS(['Klicken Sie auf eine Zelle in der Spalte **„Bestand“** (zum Beispiel B4). Sortieren Sie über **„Daten“** → **„Sortieren“** nach Bestand, **aufsteigend**. Welcher Artikel steht jetzt oben?',
      'Prüfen Sie: Steht neben jedem Artikel noch die richtige Einheit? (Glasreiniger: Flaschen, Wischmopps: Stück.)',
      'Schalten Sie den Filter ein: **„Daten“** → **„Filtern“**.',
      'Filtern Sie die Spalte **„Nachbestellen“** auf **„Ja“**. Welche Artikel bleiben übrig? Welche Zeilennummern sehen Sie?',
      'Heben Sie den Filter auf: **„Daten“** → **„Filtern“**. Sind alle zehn Artikel wieder da?',
      'Für Schnelle: Filtern Sie die Spalte **„Einheit“** auf **„Flaschen“**. Wie viele Artikel sind es? Heben Sie den Filter danach wieder auf.',
      'Speichern Sie mit **Strg+S**.']),
    H1('Selbstcheck'),
    CHECK('Ich habe eine Formel mit dem Ausfüllkästchen nach unten übertragen und eine Zelle geprüft.'),
    CHECK('Ich habe SUMME, MITTELWERT, MIN, MAX und ANZAHL eingegeben.'),
    CHECK('Ich habe AutoSumme benutzt und den Bereich geprüft.'),
    CHECK('Ich habe Beträge als Währung formatiert.'),
    CHECK('Ich habe eine Liste sortiert, gefiltert und den Filter wieder aufgehoben.'),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Lösungen'),
    H2('Aufgabe 2'),
    P('In C10 steht =B10-B9, in der Zelle **3.320** (Juli). Im Dezember hat das Haus **4.530 kWh** verbraucht.'),
    table([3000, 2500], [['Monat', 'Verbrauch (kWh)'], ...VERBR]),
    H2('Aufgabe 3'),
    table([3000, 2500], [['Funktion', 'Ergebnis'], ['Summe', '47.850 kWh'], ['Mittelwert', '3.987,5 kWh'], ['Kleinster Wert', '3.240 kWh'], ['Größter Wert', '4.850 kWh'], ['Anzahl Monate', '12']]),
    ...STEPS(['Jahresverbrauch 2025: **47.850 kWh**', 'Am kleinsten im **August** (3.240 kWh), am größten im **Januar** (4.850 kWh)',
      'Die Zelle zeigt **3.988** (gerundet), die Bearbeitungsleiste weiter die Formel. Der Wert dahinter bleibt 3.987,5.']),
    H2('Aufgabe 4'),
    P('Nebenkosten zusammen **7.140,00 €** im Monat, Fläche zusammen **2.380 m²**. (Kontrolle: 2.380 m² × 3 € = 7.140 €.)'),
    H2('Aufgabe 5'),
    BUL('**Schritt 1:** Oben steht **Wischmopps** (Bestand 4).'),
    BUL('**Schritt 2:** Ja – Excel hat ganze Zeilen sortiert.'),
    BUL('**Schritt 4:** **Glasreiniger** und **Einweghandschuhe**. Die Zeilennummern springen, weil die übrigen Zeilen ausgeblendet sind: Nach dem Sortieren steht Einweghandschuhe in Zeile 5, Glasreiniger in Zeile 7.'),
    BUL('**Schritt 5:** Ja, alle zehn Artikel sind wieder sichtbar.'),
    BUL('**Schritt 6:** **4 Artikel**: Allzweckreiniger, Glasreiniger, Bodenreiniger, Desinfektionsmittel.'),
  ], 'Übungsblatt Block 09 · Microsoft 365 im Facility Management');
})();
