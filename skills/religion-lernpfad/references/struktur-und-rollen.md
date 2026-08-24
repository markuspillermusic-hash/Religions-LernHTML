# Struktur, Rollen und Lernstand

## Empfohlene Seitenstruktur

| ID | Funktion |
|---|---|
| `top` | Hero, Kernfrage, Orientierung |
| `vorbereitung` | Sozialformen, Lehrerplanung, Beamerstart |
| `einstieg` | irritierender Fall und erste Deutung |
| `st1`…`stN` | drei bis fünf Erarbeitungsstationen |
| `sicherung` | jahresübergreifende Sicherung oder Überblick |
| `bilanz` | Rückkehr zur ersten Deutung und Fehlschlüsse |
| `transfer` | zwei bis vier neue Fälle |
| `heute` | Gegenwarts- und Positionsbezug |
| `ueberblick` | druckbare handgesetzte Übersicht |
| `check` | Selbstcheck, Zusammenfassung, Hefteintrag |
| `training` oder `weiterdenken` | abhängig von der Jahrgangsstufe |

Jede Station nach Möglichkeit mit Leitfrage, Material, Arbeitsauftrag, eigener Eingabe, Sicherung, Musterlösung und Lehrerimpuls ausstatten.

## Vorbereitung und konkrete Durchführung trennen

Den Lehrkraftbereich in drei klar erkennbare Ebenen gliedern:

1. **Didaktische Auswahl:** Voll- oder Kompaktmodus, Sozialformen, optionale Vertiefungen und zulässige Alternativwege.
2. **Technische Vorbereitung:** Unterrichtsraum bereitstellen, Beamer öffnen, externe Lehrkraftlinks eintragen und den späteren Schülerzugang prüfen.
3. **Konkrete Durchführung:** Abstimmungen, Timer, Medien und Freigaben direkt beim jeweiligen Unterrichtsabschnitt steuern.

Die ersten beiden Ebenen einklappbar machen. Ihr Ende mit einer deutlich anders gestalteten Übergabekarte markieren: aktiver Raumcode, Beitrittslink/QR, Knopf zur Beameransicht und Hinweis, dass nun die konkrete Unterrichtsseite folgt. Keine Abstimmungsfrage bereits beim bloßen Erstellen eines Raums auswählen lassen.

## Rollen

- Standardansicht als Schüleransicht gestalten.
- Alle Lehrkraftinhalte im Autorenentwurf mit `data-rolle="lehrer"` markieren.
- Gesprächsimpulse, Verlaufsplanung, Lösungen zum direkten Vorlesen und Vorbereitungswerkzeuge nicht öffentlich ausliefern, wenn eine Produktionsportierung erfolgt.
- Beameransicht ohne Lehrkraftinhalte und ohne Passwort gestalten; große Schrift, ruhige Oberfläche und eindeutigen Fenstertitel verwenden.
- Clientseitige Sichtbarkeit nie mit Zugriffsschutz verwechseln.

### Abschnittsfreigabe für Lernende

Bei produktivem Live-Unterricht gelten zusätzlich Architektur, Zustandsmodell und Abnahme aus dem [verbindlichen Klassenraumstandard](klassenraum-standard.md).

- Zu Beginn der Schülerseite einen sichtbaren Beitritt zum Unterrichtsraum anbieten; ein Raumlink darf den Code bereits enthalten.
- Noch nicht behandelte Abschnitte in der geführten Stunde sperren, aber außerhalb eines Live-Raums einen ausdrücklich wählbaren Selbstlernzugang erhalten.
- Freigaben an stabile Abschnitts- oder Schritt-IDs koppeln, nicht an Pixelpositionen. Der sichtbare Beamerfortschritt darf jeweils genau den vorgesehenen nächsten Schülerabschnitt öffnen.
- Fachlich zusammengehörige Medienbausteine wie Hörauftrag, Transkript, Audio, Begleitkarten und Sicherungsaufgabe derselben semantischen Freigabestufe zuordnen, damit der Abschnitt vollständig und nicht elementweise zufällig erscheint.
- Freigaben monoton behandeln: im normalen Unterricht nicht versehentlich wieder sperren. Eine bewusste Rücksetzung als eigene Lehrkraftaktion ausweisen.
- In der Schülernavigation knapp erklären, was gesperrt ist, wodurch freigegeben wird und wie die Navigation den aktuellen Unterrichtsstand zeigt.

## Sozialformen und Stundencode

Für zentrale Stationen vier echte Varianten anbieten:

1. didaktisch stärkste Leitform
2. Partnerarbeit
3. kurzes Unterrichtsgespräch
4. alternatives Setting oder Hausaufgabe

Varianten müssen Ablauf, Zeit und Ergebnisform verändern. Einen kompakten Code mit Präfix und Prüfbuchstaben erzeugen. Ohne Code eine sinnvolle Standardvariante anzeigen. Konfiguration lokal im Lehrerbrowser speichern.

Für den Live-Unterricht nur **einen** sechsstelligen Stundencode verwenden. Er verbindet Raum, gewählten Ablauf, Abschnittsfreigabe, Abstimmungen und Timer. Ein separater Planungs- oder Abstimmungscode erhöht die Fehlergefahr. Falls eine rein lokale Offline-Konfiguration zusätzlich codiert werden muss, diese nicht als zweiten Beitrittscode präsentieren.

Mehrere vorbereitete Räume dürfen parallel offen bleiben. Auf dem Lehrgerät eine lokale Liste mit Code, neutraler Raumbezeichnung, optionalem Lehrerkürzel und Ablaufzeit anzeigen; abgeschlossene Räume einzeln schließen können.

## Lokale Mitschrift

- Getippte Antworten, Auswahlentscheidungen, Checkfortschritt und Handschrift lokal im Browser speichern.
- `localStorage`-Fehler abfangen; bei Speichergrenze zum Export auffordern.
- Einen sichtbaren Speicherstatus anzeigen: lokal gespeichert, nicht synchronisiert.
- Hefteintrag als eigenständige Offline-HTML und optional als Text exportieren.
- Einen Importweg für den Gerätewechsel anbieten und Dateiformat versionieren.
- „Alle Eingaben löschen“ mit klarer Bestätigung versehen.
- Live-Auswahlen und private Kurzbegründungen im persönlichen Lernstand sichern. Der Server erhält nur die anonyme Auswahl, nicht die private Begründung.
- Kommentare oder Musterlösungen, die eine endgültige Eigenleistung voraussetzen, erst nach Text- **oder** Handschrifteingabe freigeben. Vor einer irreversiblen Sperre bestätigen lassen und beide Eingabewege danach konsistent sperren.
- Für die Lehrkraft ein lokales Auswertungswerkzeug für abgegebene Lernstandsdateien anbieten, wenn die Exportstruktur maschinenlesbar ist. Importversion, leere Felder und ältere Formate robust behandeln.

## ByCS

ByCS zunächst als Übergabe- und Sicherungskanal verwenden:

1. Lernende arbeiten lokal ohne Konto in der Lernseite.
2. Am Stunden- oder Einheitenende Hefteintrag herunterladen.
3. Datei in einer vorbereiteten ByCS-Aufgabe abgeben.
4. Für Weiterarbeit Datei wieder herunterladen und in die Lernseite importieren.

Keine tiefe ByCS-Integration behaupten, solange API, SSO, Rollen und schulischer Auftrag nicht konkret geklärt sind. Keine Namen in Exportdateien verlangen, wenn die Plattform die Zuordnung bereits übernimmt.

## Selbstcheck

- Genau eine richtige Antwort je geschlossener Frage vorsehen.
- Antwortreihenfolge je Durchgang mischen. Sonst steht die richtige Antwort dauerhaft an derselben Position und wird geraten statt gelesen. Startwert der Mischung gemeinsam ablegen, damit Schüler-, Lehrer- und Beameransicht dieselbe Reihenfolge zeigen.
- Rückmeldung unmittelbar und begründet geben.
- Falschantworten fachlich plausibel gestalten, nicht albern.
- Lernfortschritt lokal halten; Selbstcheck nicht als benotete Prüfung darstellen.
- Druckzusammenfassung optional nach nachvollziehbarer Leistung freischalten.

## Vollfassung und Kompaktmodus

- Beide Modi aus derselben Autorenquelle erzeugen und einen sichtbaren Moduswechsel anbieten.
- Speicherkeys und fachliche IDs stabil halten, damit der Lernstand beim Wechsel nicht verloren geht. DOM-IDs müssen in jedem **aktiven** Modus eindeutig sein.
- Alternative Markup-Bäume in `<template>` inert halten und vor der Instanziierung die nicht benötigte aktive Fassung entfernen. Danach im Browser erneut auf doppelte IDs und fehlende Ereignisbindungen prüfen.
- Vollfassung nicht stillschweigend durch den kürzeren Modus ersetzen. Der Modusname muss für Lehrkraft und Lernende erkennbar sein.
