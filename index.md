---
title: Start
nav_order: 1
permalink: /
---

# Microsoft 365 im Facility Management

Kurs für Einsteigerinnen und Einsteiger: Outlook, Word und Excel im Arbeitsalltag. Alle Übungen spielen im **Haus Lichtblick**, einem Berliner Bürogebäude, das die Teilnehmenden als Koordination des Facility Managements betreuen. Namen, Firmen und Adressen sind erfunden.

## Kursaufbau

| Teil | Inhalt | Dauer |
|---|---|---|
| [Grundkurs]({{ "/Grundkurs/" | relative_url }}) | Block 01–12: Orientierung, Outlook (E-Mail, Kalender), Word (Texte, Struktur), Excel (Eingabe, Formeln, Auswertung, Diagramme), Programme verknüpfen, Abschluss | 2 Tage |
| Aufbaumodul Word | Absätze, Bilder, Tabellen, Felder, Kopf- und Fußzeilen, Formatvorlagen, Dokumentvorlagen, Geschäftsbrief nach DIN 5008 | 1 Tag |
| Aufbaumodul Excel | WENN, SUMMEWENN, XVERWEIS, Text verbinden, Sortieren und Filtern, bedingte Formatierung, Pivot-Tabellen | 1 Tag |
| Aufbaumodul Verknüpfung | Kassenbuch mit Datenüberprüfung, Excel-Tabellen in Word, Serien-E-Mail | ½ Tag |
| Materialien | Nachschlagen und Vertiefen: Oberflächen, Befehle, Zellbezüge, Diagramme, Pivot-Tabellen | – |

**Für Lehrkräfte:** Jeder Block des Grundkurses hat eine eigene Seite mit Leitfaden, Handout, Folientexten und Übungsdateien. Die Daten des Szenarios stehen in der [Referenzliste Haus Lichtblick]({{ "/referenz/" | relative_url }}).

## Für Teilnehmende: Handouts und Übungsdateien

Datei anklicken – sie wird heruntergeladen. Speichern Sie die Übungsdateien in den Ordner, den Ihre Lehrkraft nennt (im Kursraum `C:\Kurs\Uebungen`). Lösungen erst öffnen, wenn Sie die Übung selbst probiert haben.

{% for m in site.module %}
{%- assign ordnerpfad = m.ordner | append: "/" -%}
{%- assign handouts = site.pages | where_exp: "p", "p.path contains ordnerpfad" | where_exp: "p", "p.name contains 'Handout'" | sort: "path" -%}
<h3>{{ m.titel }}{% if m.dauer != "" %} <small>({{ m.dauer }})</small>{% endif %}</h3>
{%- if handouts.size > 0 %}
<p><strong>Handouts:</strong>
{%- for p in handouts %} <a href="{{ p.url | relative_url }}">{% if p.title == "Handout" and p.parent %}{{ p.parent }}{% else %}{{ p.title | default: p.name }}{% endif %}</a>{% unless forloop.last %} ·{% endunless %}{% endfor %}</p>
{%- endif %}
{% include downloads.html ordner=m.ordner %}
{% endfor %}
