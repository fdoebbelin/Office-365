---
title: Start
nav_order: 1
permalink: /
---

# Microsoft 365 im Facility Management

Kurs für Einsteigerinnen und Einsteiger: Outlook, Word und Excel im Arbeitsalltag – zum Selbststudium oder im Einzelcoaching, ohne festen Zeitplan. Alle Übungen spielen im **Haus Lichtblick**, einem Berliner Bürogebäude, das die Teilnehmenden als Koordination des Facility Managements betreuen. Namen, Firmen und Adressen sind erfunden.

## Kursaufbau

| Teil | Inhalt |
|---|---|
| [Grundkurs]({{ "/Grundkurs/" | relative_url }}) | Block 01–12: Orientierung, Outlook (E-Mail, Kalender), Word (Texte, Struktur), Excel (Eingabe, Formeln, Auswertung, Diagramme), Programme verknüpfen, Abschluss |
| Aufbaumodul Word | Absätze, Bilder, Tabellen, Felder, Kopf- und Fußzeilen, Formatvorlagen, Dokumentvorlagen, Geschäftsbrief nach DIN 5008 |
| Aufbaumodul Excel | WENN, SUMMEWENN, XVERWEIS, Text verbinden, Sortieren und Filtern, bedingte Formatierung, Pivot-Tabellen |
| Aufbaumodul Verknüpfung | Kassenbuch mit Datenüberprüfung, Excel-Tabellen in Word, Serien-E-Mail |
| Materialien | Nachschlagen und Vertiefen: Oberflächen, Befehle, Zellbezüge, Diagramme, Pivot-Tabellen |

**So arbeiten Sie damit:** Jeder Block des Grundkurses ist eine Lerneinheit auf einer Seite – Erklärungen mit Abbildungen, Schritt-für-Schritt-Anleitungen, Selbstcheck und Hinweise für Coaching. Dazu gehören ein Übungsblatt und Übungsdateien zum Herunterladen. Nach und nach werden alle Blöcke so umgestellt; die übrigen haben noch Leitfaden und Handout getrennt. Die Daten des Szenarios stehen in der [Referenzliste Haus Lichtblick]({{ "/referenz/" | relative_url }}).

## Übungsblätter, Handouts und Übungsdateien

Datei anklicken – sie wird heruntergeladen. Speichern Sie die Übungsdateien in den Ordner, den Ihre Lehrkraft nennt (im Kursraum `C:\Kurs\Uebungen`). Lösungen erst ansehen, wenn Sie die Übung selbst probiert haben.

{% for m in site.module %}
{%- assign ordnerpfad = m.ordner | append: "/" -%}
{%- assign modulseiten = site.pages | where_exp: "p", "p.path contains ordnerpfad" -%}
{%- assign blaetter = modulseiten | where_exp: "p", "p.name contains 'Uebungsblatt'" -%}
{%- assign handouts = modulseiten | where_exp: "p", "p.name contains 'Handout'" -%}
{%- assign blaetter = blaetter | concat: handouts | sort: "path" -%}
<h3>{{ m.titel }}</h3>
{%- if blaetter.size > 0 %}
<ul>
{%- for p in blaetter %}<li><a href="{{ p.url | relative_url }}">{% if p.parent and p.title == "Handout" or p.parent and p.title == "Übungsblatt" %}{{ p.parent }} – {{ p.title }}{% else %}{{ p.title | default: p.name }}{% endif %}</a></li>{% endfor %}
</ul>
{%- endif %}
{% include downloads.html ordner=m.ordner %}
{% endfor %}
