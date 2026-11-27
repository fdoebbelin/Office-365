// Word-Dateien Block 05 erzeugen (Wartungsprotokoll und Checkliste roh und als Lösung, Übungsblatt).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-05-docx.js _resources/Grundkurs/Block-05
// Das Übungsblatt muss inhaltlich Grundkurs/Block-05-Uebungsblatt.md entsprechen.
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
// Daten aus der Referenzliste (Wartungsprotokoll, Checkliste Sicherheitsbegehung)
const PROTOKOLL = [['Datum', 'Gewerk', 'Befund', 'Maßnahme', 'Erledigt'],
  ['15.04.2025', 'Elektro', 'Deckenlampe Flur EG flackert', 'Leuchtmittel getauscht', 'Ja'],
  ['18.04.2025', 'Sanitär', 'Wasserhahn Teeküche 2. OG tropft', 'Dichtung erneuert', 'Ja'],
  ['22.04.2025', 'Heizung', 'Heizkörper Büro 305 bleibt kalt', 'Entlüftet', 'Ja'],
  ['25.04.2025', 'Brandschutz', 'Feuerlöscher EG-Flur abgelaufen', 'Neuen Löscher installiert', 'Ja']];
const GEWERKE = ['Elektro', 'Sanitär', 'Heizung', 'Brandschutz'];
const CHECKLISTE = ['Fluchtwege frei und beleuchtet', 'Feuerlöscher vorhanden und geprüft', 'Notbeleuchtung funktionsfähig', 'Rauchmelder getestet',
  'Erste-Hilfe-Kästen vollständig', 'Brandschutztüren schließen ordnungsgemäß', 'Notausgänge gekennzeichnet und zugänglich', 'Elektrische Geräte geprüft (VDE-Plakette)'];
const LINIE = '______________________________';
const FOOT_U = 'Übungsdatei Block 05 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden';
const FOOT_L = 'Lösungsdatei Block 05 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden';
async function saveM(name, title, children, foot, m) {
  const pg = { size: page.size, margin: { top: m, bottom: m, left: m, right: m } };
  const doc = new Document({ creator: 'Microsoft 365 im Facility Management', title, styles, numbering,
    sections: [{ properties: { page: pg }, footers: footer(foot), children }] });
  fs.writeFileSync(path.join(OUT, name), await Packer.toBuffer(doc));
  console.log('geschrieben', name);
}
const KOPF = ['Zeitraum: 15.04.2025 bis 25.04.2025', 'Erstellt von: Koordination Facility Management'];
const EINL = 'Die folgenden Störungen wurden im April 2025 gemeldet und behoben.';
const HINW = ['Alle vier Störungen sind erledigt.', 'Die nächste Sicherheitsbegehung folgt nach der Checkliste Sicherheitsbegehung.'];
const CKOPF = ['Gebäude: Haus Lichtblick, Sonnenallee 45, 10115 Berlin', 'Datum: ' + LINIE, 'Durchgeführt von: ' + LINIE];

(async () => {
  await save('Block-05-Wartungsprotokoll.docx', 'Wartungsprotokoll Haus Lichtblick (Rohfassung)', [
    P('Wartungsprotokoll Haus Lichtblick'), ...KOPF.map(s => P(s)),
    P('Durchgeführte Arbeiten'), P(EINL), P('[Hier die Tabelle einfügen]'),
    P('Betroffene Gewerke'), ...GEWERKE.map(s => P(s)),
    P('Hinweise'), ...HINW.map(s => P(s)),
  ], FOOT_U);

  await save('Block-05-Loesung-Wartungsprotokoll.docx', 'Wartungsprotokoll Haus Lichtblick (Lösung)', [
    H1('Wartungsprotokoll Haus Lichtblick'), ...KOPF.map(s => P(s)),
    H2('Durchgeführte Arbeiten'), P(EINL),
    table([1300, 1350, 2700, 2620, 1100], PROTOKOLL),
    H2('Betroffene Gewerke'), ...GEWERKE.map(BUL),
    H2('Hinweise'), ...HINW.map(s => P(s)),
  ], FOOT_L);

  await save('Block-05-Checkliste.docx', 'Checkliste Sicherheitsbegehung (Rohfassung)', [
    P('Checkliste Sicherheitsbegehung'), ...CKOPF.map(s => P(s)),
    P('Prüfpunkte'), ...CHECKLISTE.map(s => P(s)),
    P('Bemerkungen'), P(LINIE + LINIE), P(LINIE + LINIE), P(LINIE + LINIE),
    P('Unterschrift: ' + LINIE),
  ], FOOT_U);

  await saveM('Block-05-Loesung-Checkliste.docx', 'Checkliste Sicherheitsbegehung (Lösung)', [
    H1('Checkliste Sicherheitsbegehung'), ...CKOPF.map(s => P(s)),
    H2('Prüfpunkte'), ...STEPS(CHECKLISTE),
    H2('Bemerkungen'), P(LINIE + LINIE), P(LINIE + LINIE), P(LINIE + LINIE),
    P('Unterschrift: ' + LINIE),
  ], FOOT_L, 720);

  await save('Block-05-Uebungsblatt.docx', 'Übungsblatt Block 05 – Vorlagen und Struktur', [
    TITLE('Übungsblatt Block 05'),
    SUB('Vorlagen und Struktur'),
    P('**Sie brauchen:** einen PC mit Word und die Übungsdateien Block-05-Wartungsprotokoll.docx und Block-05-Checkliste.docx von der Seite zu Block 05. Die Lösungsdateien zeigen die fertigen Dokumente – sehen Sie sie erst am Ende an.'),
    P('**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Im April 2025 gab es vier Störungen, die alle behoben sind. Sie bringen das Wartungsprotokoll in Form und bereiten die Checkliste für die nächste Sicherheitsbegehung zum Ausdrucken vor.'),
    H1('Aufgabe 1 – Das Protokoll gliedern'),
    ...STEPS(['Öffnen Sie Block-05-Wartungsprotokoll.docx aus dem Ordner Downloads und klicken Sie gegebenenfalls auf **„Bearbeitung aktivieren“**.',
      'Speichern Sie die Datei mit **„Datei“** → **„Speichern unter“** in Dokumente\\Haus-Lichtblick unter dem Namen Wartungsprotokoll-April.',
      'Blenden Sie den Navigationsbereich ein: **„Ansicht“** → Häkchen bei **„Navigationsbereich“**. Er ist noch leer.',
      'Klicken Sie in die erste Zeile „Wartungsprotokoll Haus Lichtblick“ und wählen Sie auf der Registerkarte **„Start“** die Formatvorlage **„Überschrift 1“**.',
      'Weisen Sie den Zeilen „Durchgeführte Arbeiten“, „Betroffene Gewerke“ und „Hinweise“ die Formatvorlage **„Überschrift 2“** zu.',
      'Schauen Sie in den Navigationsbereich: Wie viele Einträge stehen dort? Klicken Sie auf „Hinweise“ – wohin springt Word?']),
    H1('Aufgabe 2 – Eine Aufzählung'),
    ...STEPS(['Markieren Sie die vier Zeilen unter „Betroffene Gewerke“ (Elektro bis Brandschutz).',
      'Klicken Sie auf **„Aufzählungszeichen“**.',
      'Probieren Sie **„Nummerierung“** aus und kehren Sie zu den Aufzählungszeichen zurück. Was passt hier besser?']),
    H1('Aufgabe 3 – Die Tabelle einfügen und ausfüllen'),
    ...STEPS(['Klicken Sie in die Zeile „[Hier die Tabelle einfügen]“, markieren Sie den Text und löschen Sie ihn. Die leere Zeile bleibt.',
      'Fügen Sie eine Tabelle mit **5 Spalten und 5 Zeilen** ein: **„Einfügen“** → **„Tabelle“**.',
      'Füllen Sie die Tabelle aus. Springen Sie mit **Tab** von Zelle zu Zelle.']),
    table([1300, 1350, 2700, 2620, 1100], PROTOKOLL),
    P('Markieren Sie zum Schluss die erste Zeile der Tabelle und machen Sie sie **fett**.', { spacing: { before: 160, after: 120 } }),
    H1('Aufgabe 4 – Die Tabelle bearbeiten'),
    ...STEPS(['Doppelklicken Sie auf die Trennlinie zwischen „Datum“ und „Gewerk“. Die Spalte passt sich dem Inhalt an. Machen Sie es bei den anderen Spalten genauso – oder ziehen Sie die Linien mit der Maus.',
      'Klicken Sie in die letzte Zelle („Ja“ in der letzten Zeile) und drücken Sie **Tab**. Eine neue Zeile erscheint.',
      'Löschen Sie die leere Zeile wieder: Schreibmarke hinein, Registerkarte **„Layout“** ganz rechts → **„Löschen“** → **„Zeilen löschen“**.',
      'Für Schnelle: Wählen Sie auf der Registerkarte **„Tabellenentwurf“** ein Tabellenformat.',
      'Speichern Sie mit **Strg+S**.']),
    H1('Aufgabe 5 – Die Checkliste'),
    ...STEPS(['Öffnen Sie Block-05-Checkliste.docx und speichern Sie sie in Dokumente\\Haus-Lichtblick als Checkliste-Begehung.',
      '„Checkliste Sicherheitsbegehung“ wird **Überschrift 1**, „Prüfpunkte“ und „Bemerkungen“ werden **Überschrift 2**.',
      'Markieren Sie die acht Prüfpunkte und klicken Sie auf **„Nummerierung“**.',
      'Stellen Sie die Seitenränder auf **„Schmal“**: **„Layout“** → **„Seitenränder“**.']),
    H1('Aufgabe 6 – Druckvorschau und Druck'),
    ...STEPS(['Öffnen Sie mit **Strg+P** die Druckvorschau.', 'Wie viele Seiten hat die Checkliste?',
      'Drucken Sie die Checkliste. Ohne Drucker wählen Sie **„Microsoft Print to PDF“** und speichern die PDF-Datei in Dokumente\\Haus-Lichtblick.',
      'Speichern Sie mit **Strg+S** und vergleichen Sie mit den Lösungsdateien.']),
    H1('Aufgabe 7 – Kurze Fragen'),
    table([600, 4970, 3500], [['Nr.', 'Frage', 'Ihre Antwort'],
      ['1', 'Welcher Befund betrifft das 2. OG?', ''],
      ['2', 'Welcher Prüfpunkt steht in der Checkliste an Stelle 6?', ''],
      ['3', 'Warum ist die Checkliste nummeriert, die Liste der Gewerke aber nicht?', '']], { minHeight: 700 }),
    H1('Selbstcheck'),
    CHECK('Ich habe Überschriften mit „Überschrift 1“ und „Überschrift 2“ zugewiesen.'),
    CHECK('Ich habe mit dem Navigationsbereich zu einer Überschrift gesprungen.'),
    CHECK('Ich habe eine Aufzählung und eine nummerierte Liste angelegt.'),
    CHECK('Ich habe eine Tabelle eingefügt, mit Tab ausgefüllt und eine Zeile gelöscht.'),
    CHECK('Ich habe die Seitenränder geändert und die Druckvorschau geprüft.'),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Lösungen'),
    H2('Aufgabe 1'),
    P('Im Navigationsbereich stehen **4 Einträge**: „Wartungsprotokoll Haus Lichtblick“ und darunter eingerückt die drei Abschnitte. Ein Klick auf „Hinweise“ springt zu diesem Abschnitt am Ende des Protokolls.'),
    H2('Aufgabe 2'),
    P('Die **Aufzählung** passt besser: Die Gewerke haben keine Reihenfolge.'),
    H2('Aufgabe 6'),
    P('Die Checkliste hat **eine Seite**.'),
    H2('Aufgabe 7'),
    ...STEPS(['Wasserhahn Teeküche 2. OG tropft (18.04.2025, Sanitär)', 'Brandschutztüren schließen ordnungsgemäß',
      'Bei der Begehung geht man die Punkte der Reihe nach durch und kann sich auf eine Nummer beziehen („Punkt 6 nicht in Ordnung“). Die Gewerke sind gleichrangig.']),
    P('Die fertigen Dokumente stehen in Block-05-Loesung-Wartungsprotokoll.docx und Block-05-Loesung-Checkliste.docx.'),
  ], 'Übungsblatt Block 05 · Microsoft 365 im Facility Management');
})();
