---
title: Downloads
---

# Microsoft 365 im Facility Management

Hier finden Sie die Handouts und Übungsdateien zum Kurs. Alle Übungen spielen im **Haus Lichtblick**, einem Berliner Bürogebäude. Namen, Firmen und Adressen sind erfunden.

**So geht's:** Datei anklicken – sie wird heruntergeladen. Speichern Sie die Übungsdateien in den Ordner, den Ihre Lehrkraft nennt (im Kursraum `C:\Kurs\Uebungen`). Lösungen erst öffnen, wenn Sie die Übung selbst probiert haben.

{% comment %}
Diese Seite füllt sich selbst:
- Handouts: alle Markdown-Dateien eines Modulordners mit „Handout“ im Namen.
- Downloads: alle Dateien in _resources/<Modul>/, im Grundkurs gruppiert nach Unterordner Block-NN.
Reihenfolge und Titel der Module stehen in _config.yml unter „module“.
{% endcomment %}
{% for m in site.module %}
{% assign prefix = "_resources/" | append: m.ordner | append: "/" %}
{% assign ordnerpfad = m.ordner | append: "/" %}
{% assign dateien = site.static_files | where_exp: "f", "f.path contains prefix" | sort: "path" %}
{% assign handouts = site.pages | where_exp: "p", "p.path contains ordnerpfad" | where_exp: "p", "p.name contains 'Handout'" | sort: "path" %}
<h2>{{ m.titel }}{% if m.dauer != "" %} <small>({{ m.dauer }})</small>{% endif %}</h2>
{% if handouts.size > 0 %}
<h3>Handouts</h3>
<ul>
{% for p in handouts %}<li><a href="{{ p.url | relative_url }}">{{ p.name | remove: ".md" }}</a></li>
{% endfor %}</ul>
{% endif %}
{% if dateien.size > 0 %}
<h3>Übungsdateien</h3>
{% assign gruppen = dateien | group_by_exp: "f", "f.path | split: prefix | last | split: '/' | first" %}
<table>
<thead><tr><th>Block / Thema</th><th>Datei</th><th>Programm</th></tr></thead>
<tbody>
{% for g in gruppen %}{% for f in g.items %}
{% assign teile = f.path | split: prefix | last | split: "/" %}
{% if teile.size > 1 %}{% assign gruppe = teile.first | replace: "-", " " %}{% else %}{% assign gruppe = "" %}{% endif %}
{% case f.extname %}{% when ".docx" %}{% assign art = "Word" %}{% when ".dotx" %}{% assign art = "Word-Vorlage" %}{% when ".xlsx" %}{% assign art = "Excel" %}{% when ".xltx" %}{% assign art = "Excel-Vorlage" %}{% else %}{% assign art = f.extname | remove: "." %}{% endcase %}
{% assign anfang = f.basename | slice: 0, 7 %}
<tr><td>{% if forloop.first %}{{ gruppe }}{% endif %}</td><td><a href="{{ f.path | relative_url }}" download>{{ f.name }}</a>{% if anfang == "Loesung" %} <em>(Lösung)</em>{% endif %}</td><td>{{ art }}</td></tr>
{% endfor %}{% endfor %}
</tbody>
</table>
{% endif %}
{% if handouts.size == 0 and dateien.size == 0 %}
<p><em>Noch keine Dateien.</em></p>
{% endif %}
{% endfor %}
