# QA vor der Abgabe

## Programmatisch

`python scripts/validate_learning_html.py <datei.html>` ausführen. Für eine bereits bereinigte öffentliche Schülerdatei zusätzlich `--public`, für die Beamerdatei `--beamer` verwenden.

Nach einem Drei-Ansichten-Build zusätzlich ausführen:

```text
python scripts/validate_view_bundle.py schueler.html lehrer.php beamer.html
```

Das prüft Rollentrennung, Antwortfelder am Beamer und identische stabile Schrittmengen.

Für einen produktiven Klassenraum-Build danach ausführen:

```text
python scripts/validate_classroom_contract.py schueler.html lehrer.php beamer.html --api live.php --classroom-js live.js --presentation-js presentation.js --qr-js qrcode-generator.js
```

Der statische Vertragstest ersetzt den Browserlauf nicht. Wenn im Projekt `_shared/classroom-v1/qa-classroom-contract-live.js` vorhanden ist, diesen anschließend gegen die veröffentlichte Zielroute in getrennten Lehrer-, Schüler- und Beamer-Kontexten ausführen und die Testräume automatisch beenden.

Prüfen:

- HTML-Grundstruktur, doppelte IDs und fehlende Fragmentziele
- fehlende Alt-Texte
- Inline-Handler ohne passende Funktion
- JavaScript-Syntax, soweit Node.js verfügbar ist
- Remote-Medien und verdächtige Klartextpasswörter
- lokale Mediendateien
- inerte `<template>`-Inhalte getrennt von der aktiven DOM-Fassung; nach Instanziierung zusätzlich im Browser prüfen

## Manuell

- Schüleransicht enthält keine Lehrkraftinformationen.
- Tastaturreihenfolge, sichtbarer Fokus, Dialoge, Escape und Fokus-Rückgabe funktionieren.
- 375 px, Tabletbreite, Desktop, Beamerformat sowie 200-%-Zoom ohne horizontales Scrollen prüfen.
- Dunkelmodus, reduzierte Bewegung und Druckansicht prüfen.
- Jede Eingabe speichern, neu laden, exportieren, löschen und wieder importieren.
- Selbstcheck vollständig lösen; genau eine richtige Antwort und verständliche Rückmeldung je Frage prüfen.
- Beamerfenster öffnen und von Lehrkraftinhalten trennen.
- Beamer neu laden und prüfen, dass Theme, Abschnitt, Scrollposition, Aufklapper, aktive Karte und laufender Medienzustand aus dem Raum rekonstruiert werden.
- Alle Bilder laden; SVG, Bildpaare und Regler visuell gegenlesen.
- Voll- und Kompaktmodus jeweils neu laden, umschalten und auf eindeutige aktive IDs, erhaltene Eingaben und gebundene Controls prüfen.
- Schrittweise Schaubilder von 0 bis Ende sowie zurück durchlaufen; „Alles zeigen“ und Neustart testen. Mobil darf nur der Schaubildbereich horizontal scrollen.
- Eigene Videos: Dauer und Auflösung aus den geladenen Metadaten prüfen; Start, Pause und Neustart vom Lehrgerät auslösen und sicherstellen, dass nur der Beamer Ton wiedergibt.
- Audiopodcasts vollständig von Beginn bis Ende prüfen: Hörauftrag, aufklappbares Transkript, PDF-Link, Metadaten, Pause/Fortsetzen, Neustart und die zeitlich richtigen Begleitkarten.
- Kartenraster in allen Ansichten prüfen: gleiche Ordnungsposition oben links, keine Verschiebung durch Porträts, keine Überlagerung im Dunkelmodus und sinnvolle Stapelung auf Tablets.
- Bild-Vollansicht mit Maus, Tastatur, Escape und Fokus-Rückgabe prüfen; QR-Codes dürfen nicht versehentlich als Unterrichtsbild behandelt werden.

## Geführter Live-Unterricht

- Schüler ohne Raum: sichtbare Beitrittsmöglichkeit und verständlicher Hinweis auf die Sperrlogik.
- Schüler mit Raumlink: richtiger Code ohne zweite Eingabe, richtiger Ablaufmodus und genau bis zum freigegebenen Abschnitt sichtbar.
- Lehrer scrollt/springt von Abschnitt zu Abschnitt: Beamer folgt korrekt und Schülerfreigabe bleibt ohne Vor- oder Nachlauf synchron.
- Direkte Sprünge über die obere Navigation ebenso wie schrittweises Scrollen prüfen. Zusammengehörige Mediensequenzen müssen als vollständiger Abschnitt freigegeben werden, nicht nur einzelne Unterelemente.
- Abstimmung wird an ihrer fachlichen Stelle gestartet: derselbe Inline-Kasten erscheint dort bei Schülern; Code/QR und Ergebnisstatus sind am Beamer vollständig im Viewport.
- Vor Freigabe dürfen öffentliche Statusantworten weder Summen noch richtige Antworten oder Erwartungshorizonte enthalten.
- Antwortwechsel vor dem Schließen muss Summen korrigieren, nicht eine zusätzliche Stimme erzeugen. Private Begründungen dürfen nicht im Serverzustand erscheinen.
- Timer start/pause/fortsetzen/Zeit hinzufügen/Ende in allen drei Ansichten prüfen.
- QR-Bereich wirklich aufklappen, SVG und eingebetteten Raumlink prüfen; bei absichtlich blockierter QR-Bibliothek muss der direkte Schülerlink als Fallback bedienbar bleiben.
- Gebündelten Klassencheck testen: alle Fragen gleichzeitig, Fortschrittsanzeige, genau ein Abgabeknopf, Korrektur vor Ende, automatische Schließung und kompakte Beamerauswertung.
- Falls KI-Feedback vorgesehen ist: ohne konfigurierten Serverschlüssel ist der Knopf deaktiviert; mit Testschlüssel werden nur freigegebene Aufgaben akzeptiert. Schülertext darf weder im Raumstatus noch in Inhaltslogs erscheinen. Mindestlänge, Rate-Limit, Kostenlimit, strukturierte Antwort, Anbieterfehler und erneuter Versuch sind zu testen.

## Inhaltlich

- Kompetenzziel und roter Faden erkennbar
- gA ohne eA-Kasten vollständig verständlich
- Materialquellen und Fachbegriffe vorhanden
- Positionen fair, Zitate und Datierungen verifiziert
- Musterlösungen begründen statt nur benennen
- offene Rechts- und Lizenznachweise ausdrücklich übergeben

Automatische Prüfungen sind kein Nachweis vollständiger Barrierefreiheit oder fachlicher Richtigkeit.

## Abnahmebelege

- Bei komplexen Änderungen mindestens je einen Screenshot der entscheidenden Schüler-, Lehrer- und Beamerzustände sichern und visuell ansehen.
- Browserfehler und fehlgeschlagene Netzwerkaufrufe sammeln; ein optisch plausibler Screenshot ersetzt keine Konsolen- und API-Prüfung.
- Nach Veröffentlichung lokale und öffentlich ausgelieferte Hashes vergleichen. Cache-Version und tatsächlich geladene Medien-URL im Browser prüfen.
