// Word-Dateien Block 04 erzeugen (Aushang roh und als Lösung, Übungsblatt).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-04-docx.js _resources/Grundkurs/Block-04
// Das Übungsblatt muss inhaltlich Grundkurs/Block-04-Uebungsblatt.md entsprechen.
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
// Aushang: Rohtext mit 8 leeren Absätzen (Lösung Aufgabe 5), alles Aptos 11 ohne Formatierung.
const ROH = ['Aufzug außer Betrieb', 'Personenaufzug – Haus Lichtblick', '', '', '',
  'Liebe Mieterinnen und Mieter,',
  'am Montag ist der Personenaufzug wegen Wartung den ganzen Tag außer Betrieb. Die Firma Lift-Service Nord führt die regelmäßige Wartung durch.',
  '', 'Bitte nutzen Sie in dieser Zeit die Treppe. Für schwere Lasten steht Ihnen der Lastenaufzug zur Verfügung.',
  '', '', 'Wir bitten um Ihr Verständnis.', '', 'Bei Fragen wenden Sie sich bitte an:',
  'Thomas Weber, Hausmeister', 'thomas.weber@haus-lichtblick.de', '', 'Ihre Koordination Facility Management'];
if (ROH.filter(s => s === '').length !== 8) throw new Error('Anzahl leerer Absätze stimmt nicht');
const plain = s => new Paragraph({ spacing: { after: 0 }, children: s ? [new TextRun(s)] : [] });
const A = (children, o = {}) => new Paragraph({ spacing: { after: 240 }, ...o, children });
const T = (text, o = {}) => new TextRun({ text, ...o });

(async () => {
  await save('Block-04-Aushang.docx', 'Aushang Aufzug außer Betrieb (Rohtext)', ROH.map(plain),
    'Übungsdatei Block 04 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden');

  await save('Block-04-Loesung-Aushang.docx', 'Aushang Aufzug außer Betrieb (Lösung)', [
    A([T('Aufzug außer Betrieb', { bold: true, size: 72 })], { alignment: AlignmentType.CENTER }),
    A([T('Personenaufzug – Haus Lichtblick', { bold: true, size: 36 })], { alignment: AlignmentType.CENTER }),
    A([T('Liebe Mieterinnen und Mieter,', { size: 32 })]),
    A([T('am Montag ist der Personenaufzug ', { size: 32 }), T('wegen Wartung den ganzen Tag außer Betrieb', { size: 32, bold: true }),
      T('. Die Firma Lift-Service Nord führt die regelmäßige Wartung durch.', { size: 32 })]),
    A([T('Bitte nutzen Sie in dieser Zeit die Treppe. Für schwere Lasten steht Ihnen der Lastenaufzug zur Verfügung.', { size: 32 })]),
    A([T('Wir bitten um Ihr Verständnis.', { size: 32 })]),
    A([T('Bei Fragen wenden Sie sich bitte an:', { size: 32 })]),
    A([T('Thomas Weber, Hausmeister', { size: 28, italics: true }), new TextRun({ break: 1 }), T('thomas.weber@haus-lichtblick.de', { size: 28, italics: true })]),
    A([T('Ihre Koordination Facility Management', { size: 32 })]),
  ], 'Lösungsdatei Block 04 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden');

  await save('Block-04-Uebungsblatt.docx', 'Übungsblatt Block 04 – Texte erstellen, formatieren und speichern', [
    TITLE('Übungsblatt Block 04'),
    SUB('Texte erstellen, formatieren und speichern'),
    P('**Sie brauchen:** einen PC mit Word und die Übungsdatei Block-04-Aushang.docx von der Seite zu Block 04. Die Lösungsdatei Block-04-Loesung-Aushang.docx zeigt den fertigen Aushang – sehen Sie sie erst am Ende an. Ein Drucker ist schön, aber nicht nötig.'),
    P('**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Am Montag wartet Lift-Service Nord den Personenaufzug – er steht den ganzen Tag still. Thomas Weber, der Hausmeister, hat den Text für einen Aushang geschrieben. Sie machen daraus einen Aushang, den man in der Eingangshalle im Vorbeigehen lesen kann.'),
    H1('Aufgabe 1 – Word erkunden'),
    ...STEPS(['Starten Sie Word und klicken Sie auf **„Leeres Dokument“**.',
      'Suchen Sie Titelleiste, Registerkarten, Menüband, Dokument und Statusleiste.',
      'Klicken Sie nacheinander auf die Registerkarten **„Einfügen“**, **„Layout“** und **„Ansicht“** und wieder auf **„Start“**. Was ändert sich?',
      'Blenden Sie das Lineal ein: **„Ansicht“** → Häkchen bei **„Lineal“**.']),
    H1('Aufgabe 2 – Ihr Kursordner und das erste Dokument'),
    ...STEPS(['Schreiben Sie in das leere Dokument: Haus Lichtblick, drücken Sie **Enter** und schreiben Sie in die nächste Zeile: Sonnenallee 45, 10115 Berlin',
      'Drücken Sie **Strg+S**. Klicken Sie auf **„Weitere Speicheroptionen“** und dann auf **„Durchsuchen“**.',
      'Klicken Sie links auf **„Dokumente“**, dann oben auf **„Neuer Ordner“**. Name: Haus-Lichtblick, **Enter**. Öffnen Sie den Ordner mit Doppelklick.',
      'Dateiname: Mein-Test. Klicken Sie auf **„Speichern“**. Prüfen Sie: Steht „Mein-Test“ oben in der Titelleiste?',
      'Schließen Sie Word mit dem **X**.',
      'Starten Sie Word neu und öffnen Sie die Datei über **„Datei“** → **„Öffnen“** → **„Zuletzt verwendet“**.']),
    H1('Aufgabe 3 – Markieren, formatieren, rückgängig'),
    P('Bleiben Sie in Mein-Test.'),
    ...STEPS(['Doppelklicken Sie auf das Wort „Lichtblick“ und machen Sie es **fett**.',
      'Markieren Sie die ganze zweite Zeile mit gedrückter Maustaste und machen Sie sie kursiv – diesmal mit **Strg+Umschalt+K**.',
      'Markieren Sie die erste Zeile und stellen Sie die Schriftgröße auf **20**.',
      'Drücken Sie dreimal **Strg+Z**. Alles ist wieder wie vorher.',
      'Drücken Sie einmal **Strg+Y**. Was kommt zurück?',
      'Speichern Sie mit **Strg+S** und schließen Sie das Dokument.']),
    H1('Aufgabe 4 – Die Übungsdatei unter eigenem Namen speichern'),
    ...STEPS(['Öffnen Sie Block-04-Aushang.docx aus dem Ordner **Downloads**. Erscheint die gelbe Leiste „Geschützte Ansicht“, klicken Sie auf **„Bearbeitung aktivieren“**.',
      'Klicken Sie auf **„Datei“** → **„Speichern unter“** → **„Durchsuchen“**.',
      'Wählen Sie den Ordner Dokumente\\Haus-Lichtblick, Dateiname: Aushang-Aufzug. Klicken Sie auf **„Speichern“**.']),
    P('Ab jetzt arbeiten Sie in Ihrer eigenen Datei. Speichern Sie zwischendurch mit **Strg+S**.', { spacing: { before: 120, after: 120 } }),
    H1('Aufgabe 5 – Leere Absätze aufräumen'),
    ...STEPS(['Klicken Sie auf der Registerkarte **„Start“** in der Gruppe **„Absatz“** auf **¶**. Jetzt sehen Sie die Formatierungszeichen.',
      'Zählen Sie: Wie viele **leere Absätze** (Zeilen, in denen nur ¶ steht) gibt es?',
      'Löschen Sie alle leeren Absätze: Klicken Sie in die leere Zeile und drücken Sie **Entf**.',
      'Markieren Sie den ganzen Text mit **Strg+A**. Stellen Sie auf der Registerkarte **„Layout“** bei **„Abstand“** das Feld **„Nach“** auf **12 pt**. Jetzt haben alle Absätze gleichmäßigen Abstand.']),
    H1('Aufgabe 6 – Den Aushang formatieren'),
    ...STEPS(['Erste Zeile „Aufzug außer Betrieb“: Schriftgröße **36**, **fett**, **zentriert** (Strg+E).',
      'Zweite Zeile „Personenaufzug – Haus Lichtblick“: Schriftgröße **18**, **fett**, **zentriert**.',
      'Den restlichen Text markieren und auf Schriftgröße **16** stellen.',
      'Markieren Sie im ersten Absatz die Worte „wegen Wartung den ganzen Tag außer Betrieb“ und machen Sie sie **fett**.']),
    H1('Aufgabe 7 – Der Kontakt in einem Absatz'),
    P('Name und E-Mail-Adresse des Hausmeisters gehören zusammen. Machen Sie aus den zwei Absätzen einen.'),
    ...STEPS(['Klicken Sie ans Ende der Zeile „Thomas Weber, Hausmeister“ (hinter das ¶).',
      'Drücken Sie **Entf**. Die E-Mail-Adresse rutscht in dieselbe Zeile.',
      'Drücken Sie **Umschalt+Enter**. Die Adresse steht wieder darunter – jetzt mit ↵ statt ¶.',
      'Markieren Sie den Kontakt (beide Zeilen) und machen Sie ihn kursiv in Schriftgröße **14**.']),
    H1('Aufgabe 8 – Prüfen, speichern, drucken'),
    ...STEPS(['Blenden Sie die Formatierungszeichen mit **¶** wieder aus.',
      'Schauen Sie in die Statusleiste: Passt der Aushang auf eine Seite?',
      'Speichern Sie mit **Strg+S**.',
      'Öffnen Sie mit **Strg+P** die Druckvorschau. Drucken Sie den Aushang, wenn ein Drucker angeschlossen ist.',
      'Öffnen Sie zum Vergleich die Lösungsdatei Block-04-Loesung-Aushang.docx.']),
    H1('Selbstcheck'),
    CHECK('Ich habe den Ordner Dokumente\\Haus-Lichtblick angelegt und darin zwei Dateien gespeichert.'),
    CHECK('Ich habe eine Datei über „Zuletzt verwendet“ wieder geöffnet.'),
    CHECK('Ich habe Text markiert und fett, kursiv und größer gemacht.'),
    CHECK('Ich habe einen Schritt mit Strg+Z rückgängig gemacht.'),
    CHECK('Ich habe Formatierungszeichen eingeblendet und leere Absätze gelöscht.'),
    CHECK('Ich habe mit Umschalt+Enter eine neue Zeile im selben Absatz begonnen.'),
    CHECK('Mein Aushang passt auf eine Seite und ist aus der Entfernung lesbar.'),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Lösungen'),
    H2('Aufgabe 3'),
    P('Strg+Y stellt den zuletzt rückgängig gemachten Schritt wieder her: Die erste Zeile ist wieder 20 pt groß.'),
    H2('Aufgabe 5'),
    P('Die Übungsdatei hat **8 leere Absätze**: drei unter dem Untertitel, zwei vor „Wir bitten …“ und je einer vor „Bitte nutzen Sie …“, „Bei Fragen …“ und „Ihre Koordination …“.'),
    H2('Aufgabe 8'),
    P('Ja, der Aushang passt auf eine Seite: In der Statusleiste steht „Seite 1 von 1“. Der fertige Aushang steht in der Lösungsdatei Block-04-Loesung-Aushang.docx.'),
  ], 'Übungsblatt Block 04 · Microsoft 365 im Facility Management');
})();
