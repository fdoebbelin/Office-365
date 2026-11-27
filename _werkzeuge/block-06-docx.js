// Word-Dateien Block 06 erzeugen (Aushang und Störungsprotokoll roh und als Lösung, Übungsblatt).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-06-docx.js _resources/Grundkurs/Block-06
// Das Übungsblatt muss inhaltlich Grundkurs/Block-06-Uebungsblatt.md entsprechen.
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
const SUBBUL = s => new Paragraph({ children: runs(s), numbering: { reference: 'bullets', level: 0 }, indent: { left: 1134, hanging: 283 } });
const ROH = ['Heizung im 3. OG', 'Information für die Mieter im 3. OG – Haus Lichtblick', '', 'Liebe Mieterinnen und Mieter,',
  'in einigen Büros im 3. OG bleiben die Heizkörper kalt. Die Firma Heizungstechnik Berlin prüft die Heizung morgen ab 8 Uhr.',
  'Bitte halten Sie die Büros 301 bis 308 an diesem Vormittag zugänglich.', '', 'Wir bitten um Ihr Verständnis.', '',
  'Bei Fragen wenden Sie sich bitte an:', 'Thomas Weber, Hausmeister', 'thomas.weber@haus-lichtblick.de', '', 'Ihre Koordination Facility Management'];
if (ROH.filter(s => s === '').length !== 4) throw new Error('Anzahl leerer Absätze stimmt nicht');
const plain = s => new Paragraph({ spacing: { after: 0 }, children: s ? [new TextRun(s)] : [] });
const A = (children, o = {}) => new Paragraph({ spacing: { after: 240 }, ...o, children });
const T = (text, o = {}) => new TextRun({ text, ...o });
const MASSN = ['Heizungstechnik Berlin beauftragt', 'Termin zur Prüfung vereinbart', 'Mieter im 3. OG per Aushang informiert', 'Hausverwaltung in Kenntnis gesetzt'];
const KOPF = ['Gemeldet von: Tim Rauch, Lernwerk Akademie (3. OG)', 'Aufgenommen von: Koordination Facility Management'];
const TAB = [['Datum', 'Gewerk', 'Befund', 'Maßnahme', 'Erledigt'], ['(heutiges Datum)', 'Heizung', 'Heizkörper in den Büros im 3. OG bleiben kalt', 'Heizungstechnik Berlin beauftragt', 'Nein']];
const FU = 'Übungsdatei Block 06 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden';
const FL = 'Lösungsdatei Block 06 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden';

(async () => {
  await save('Block-06-Aushang-Heizung.docx', 'Aushang Heizung 3. OG (Rohtext)', ROH.map(plain), FU);
  await save('Block-06-Loesung-Aushang-Heizung.docx', 'Aushang Heizung 3. OG (Beispiellösung)', [
    A([T('Heizung im 3. OG', { bold: true, size: 72 })], { alignment: AlignmentType.CENTER }),
    A([T('Information für die Mieter im 3. OG – Haus Lichtblick', { bold: true, size: 36 })], { alignment: AlignmentType.CENTER }),
    A([T('Liebe Mieterinnen und Mieter,', { size: 32 })]),
    A([T('in einigen Büros im 3. OG bleiben die Heizkörper kalt. Die Firma Heizungstechnik Berlin prüft die Heizung ', { size: 32 }), T('morgen ab 8 Uhr', { size: 32, bold: true }), T('.', { size: 32 })]),
    A([T('Bitte halten Sie die Büros 301 bis 308 an diesem Vormittag zugänglich.', { size: 32 })]),
    A([T('Wir bitten um Ihr Verständnis.', { size: 32 })]),
    A([T('Bei Fragen wenden Sie sich bitte an:', { size: 32 })]),
    A([T('Thomas Weber, Hausmeister', { size: 28, italics: true }), new TextRun({ break: 1 }), T('thomas.weber@haus-lichtblick.de', { size: 28, italics: true })]),
    A([T('Ihre Koordination Facility Management', { size: 32 })]),
  ], FL);
  await save('Block-06-Stoerungsprotokoll.docx', 'Störungsprotokoll Heizung 3. OG (Rohfassung)', [
    P('Störungsprotokoll Heizung 3. OG'), ...KOPF.map(s => P(s)),
    P('Meldung'), P('Die Heizkörper in mehreren Büros im 3. OG bleiben kalt.'),
    P('Maßnahmen'), ...MASSN.map(s => P(s)),
    P('Übersicht'), P('[Hier die Tabelle einfügen]'),
    P('Offene Punkte'), P('Rückmeldung von Heizungstechnik Berlin abwarten.'),
  ], FU);
  await save('Block-06-Loesung-Stoerungsprotokoll.docx', 'Störungsprotokoll Heizung 3. OG (Beispiellösung)', [
    H1('Störungsprotokoll Heizung 3. OG'), ...KOPF.map(s => P(s)),
    H2('Meldung'), P('Die Heizkörper in mehreren Büros im 3. OG bleiben kalt.'),
    H2('Maßnahmen'), ...STEPS(MASSN),
    H2('Übersicht'), table([1700, 1150, 2500, 2620, 1100], TAB),
    H2('Offene Punkte'), P('Rückmeldung von Heizungstechnik Berlin abwarten.'),
  ], FL);

  await save('Block-06-Uebungsblatt.docx', 'Übungsblatt Block 06 – Praxis Outlook und Word', [
    TITLE('Übungsblatt Block 06'),
    SUB('Praxis Outlook und Word'),
    P('**Sie brauchen:** einen PC mit dem neuen Outlook, Ihrem E-Mail-Konto und Word sowie die Übungsdateien Block-06-Aushang-Heizung.docx und Block-06-Stoerungsprotokoll.docx von der Seite zu Block 06. Die Lösungsdateien zeigen fertige Beispiele – sehen Sie sie erst am Ende an.'),
    P('**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Montagmorgen ruft Tim Rauch von der Lernwerk Akademie an: „Bei uns im 3. OG bleiben die Heizkörper kalt – in mehreren Büros.“ Sie kümmern sich darum, von der ersten E-Mail bis zum Protokoll.'),
    ...BOX('Achtung:', ['E-Mails nur an **Ihre eigene Adresse**. Sie steht in diesem Fall für Heizungstechnik Berlin und für Petra Schönfeld von der Hausverwaltung.'], 'FBE9E7', 'B3261E'),
    H1('Schritt 1 – Die E-Mail'),
    ...STEPS(['Schreiben Sie eine neue E-Mail. **An:** Ihre eigene Adresse (für Heizungstechnik Berlin). **Cc:** noch einmal Ihre eigene Adresse (für die Hausverwaltung).',
      'Wählen Sie einen Betreff, der sagt, **was** los ist und **wo**.',
      'Schreiben Sie den Text selbst. Er soll enthalten: eine Anrede; was gemeldet wurde und von wem; die Bitte, die Heizung **morgen ab 8 Uhr** zu prüfen; dass der Hausmeister Thomas Weber den Technikraum 1 aufschließt; einen Gruß mit Ihrem Namen.',
      'Lesen Sie An, Cc und Betreff noch einmal und klicken Sie auf **„Senden“**.']),
    H1('Schritt 2 – Der Termin'),
    ...STEPS(['Wechseln Sie zum Kalender und legen Sie ein **neues Ereignis** an.', 'Titel: Prüfung Heizung 3. OG – Heizungstechnik Berlin',
      'Datum: morgen, Beginn 08:00 Uhr, Ende 09:30 Uhr. Ort: Technikraum 1 (Heizung) und 3. OG', 'Erinnerung: **15 Minuten vorher**. Speichern.']),
    H1('Schritt 3 – Der Aushang'),
    ...STEPS(['Öffnen Sie Block-06-Aushang-Heizung.docx, klicken Sie auf „Bearbeitung aktivieren“ und speichern Sie die Datei in Dokumente\\Haus-Lichtblick als Aushang-Heizung-3OG.',
      'Gestalten Sie den Aushang selbst – so, dass man ihn im Treppenhaus aus der Entfernung lesen kann:']),
    SUBBUL('leere Absätze entfernen'), SUBBUL('Titel groß, fett und zentriert'), SUBBUL('Text gut lesbar (14–16 pt)'),
    SUBBUL('**wann** die Prüfung ist, fett hervorheben'), SUBBUL('Name und E-Mail-Adresse des Hausmeisters in **einem** Absatz (Umschalt+Enter)'),
    P('Speichern Sie und prüfen Sie in der Druckvorschau: Passt alles auf eine Seite?', { spacing: { before: 120, after: 120 } }),
    H1('Schritt 4 – Das Protokoll'),
    ...STEPS(['Öffnen Sie Block-06-Stoerungsprotokoll.docx und speichern Sie sie in Dokumente\\Haus-Lichtblick als Stoerungsprotokoll-Heizung-3OG.',
      'Weisen Sie der ersten Zeile **Überschrift 1** zu und den Zeilen „Meldung“, „Maßnahmen“, „Übersicht“ und „Offene Punkte“ **Überschrift 2**.',
      'Machen Sie aus den vier Zeilen unter „Maßnahmen“ eine **nummerierte Liste**.',
      'Ersetzen Sie „[Hier die Tabelle einfügen]“ durch eine Tabelle mit **5 Spalten und 2 Zeilen**:']),
    table([1700, 1150, 2500, 2620, 1100], [TAB[0], ['heutiges Datum', ...TAB[1].slice(1)]]),
    P('Machen Sie die erste Tabellenzeile fett. Blenden Sie den Navigationsbereich ein: Wie viele Einträge sehen Sie? Speichern Sie mit **Strg+S**.', { spacing: { before: 160, after: 120 } }),
    H1('Schritt 5 – Ordnung und Aufräumen'),
    ...STEPS(['Verschieben Sie die E-Mail aus Schritt 1 in den Ordner **„Störungsmeldungen“** (aus Block 02 – oder legen Sie ihn jetzt an).',
      'Löschen Sie den Termin aus Schritt 2 – es war eine Übung.', 'Vergleichen Sie Aushang und Protokoll mit den Lösungsdateien.']),
    H1('Selbstcheck'),
    CHECK('Meine E-Mail hat einen Betreff mit Was und Wo, die Technik in An und die Hausverwaltung in Cc.'),
    CHECK('Der Termin hatte eine Erinnerung.'),
    CHECK('Mein Aushang ist aus der Entfernung lesbar, das Wichtigste ist fett.'),
    CHECK('Mein Protokoll hat Überschriften aus den Formatvorlagen, eine nummerierte Liste und eine Tabelle.'),
    CHECK('Ich habe aufgeschrieben, wo ich nachschlagen musste.'),
    table([6500, 2570], [['Hier musste ich nachschlagen', 'Block'], ['', ''], ['', ''], ['', '']], { minHeight: 500 }),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Beispiellösungen'),
    H2('Schritt 1'),
    P('Ein möglicher Betreff: „Heizungsausfall – Heizkörper Büros 3. OG bleiben kalt“. Ein möglicher Text:'),
    ...BOX('', ['Guten Tag,', 'Herr Rauch von der Lernwerk Akademie meldet, dass im 3. OG die Heizkörper in mehreren Büros kalt bleiben. Bitte prüfen Sie die Heizung morgen ab 8 Uhr. Unser Hausmeister Thomas Weber schließt Ihnen den Technikraum 1 auf.',
      'Vielen Dank und viele Grüße', '[Ihr Name]', 'Koordination Facility Management, Haus Lichtblick'], SOFT, NAVY),
    H2('Schritt 3'),
    P('Die Übungsdatei hat 4 leere Absätze. Ein Beispiel für den fertigen Aushang steht in Block-06-Loesung-Aushang-Heizung.docx.'),
    H2('Schritt 4'),
    P('Im Navigationsbereich stehen **5 Einträge**: die Überschrift 1 und die vier Abschnitte. Die nummerierte Liste passt, weil die Maßnahmen der Reihe nach erledigt wurden. Ein Beispiel steht in Block-06-Loesung-Stoerungsprotokoll.docx.'),
  ], 'Übungsblatt Block 06 · Microsoft 365 im Facility Management');
})();
