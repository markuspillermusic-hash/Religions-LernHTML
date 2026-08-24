# Design und Interaktionen

## Inhalt

- [Grundsystem](#grundsystem), [eA](#ea-komponente), [Handschrift](#handschrift) und [Beamer-Fernsteuerung](#beamer-fernsteuerung)
- [Timer](#gemeinsamer-timer), [Audiopodcasts](#audiopodcasts-als-geführte-mediensequenz) und [synchronisierte Medien](#synchronisierte-audio--und-videowiedergabe)
- [Karten](#kartenraster-und-abschnittskarten), [Schaubilder](#bilder-und-schrittweise-schaubilder), [Zeitstrahl](#interaktiver-zeitstrahl), [SVG](#svg-schaubilder) und [Bildvergleiche](#bildvergleiche)

## Grundsystem

- Mobile-first, semantisches HTML und native Controls verwenden.
- Grundschrift ungefähr 17–18 px, klare Serifenschrift für Überschriften und Systemschrift für Bedienung nutzen.
- Farbe, Abstand, Radius, Schatten und Stationsfarben als CSS-Variablen definieren.
- Fokus sichtbar machen, Touch-Ziele mindestens 44 px komfortabel halten und `prefers-reduced-motion` respektieren.
- Dunkelmodus, 200-%-Zoom, Druck und schmale Viewports ausdrücklich prüfen.
- Dateinamen ASCII, klein und ohne Leerzeichen halten.

## eA-Komponente

```html
<div class="note niveau-note"><p><b>eA</b> Aufklappbare Kästen enthalten Vertiefungen für das erhöhte Anforderungsniveau.</p></div>
<details class="ea">
  <summary><span class="eatag">eA</span> Titel <span aria-hidden="true">▸</span></summary>
  <div class="ea-body">…</div>
</details>
```

Native `details` verwenden; keine zusätzliche JavaScript-Abhängigkeit einführen. Beim Drucken eA-Inhalte nach Unterrichtsziel offen oder geschlossen abbilden.

## Handschrift

- Unter relevanten Textfeldern optional eine Canvas-Schreibfläche anbieten.
- Pointer Events für Stift und Touch verwenden; Handballen über breite Touchkontakte heuristisch ignorieren.
- Zeichnung als komprimierte Data-URL speichern und gemeinsam mit Texteingaben exportieren.
- Canvas immer mit zugänglicher Textalternative und Löschknopf versehen.

## Beamer-Fernsteuerung

Die Lehrkraft steuert ein zweites Fenster oder ein zweites Gerät, das dauerhaft die Beameransicht zeigt. Sie soll dabei nicht zwischen zwei Ansichten wechseln müssen. Für produktive Live-Seiten gilt ergänzend der [Klassenraumstandard](klassenraum-standard.md).

- Im selben Browser Befehle sofort über `postMessage`, `BroadcastChannel` und einen gemeinsamen `localStorage`-Kanal zustellen. Nicht allein auf den Fenstergriff aus `window.open` vertrauen; er geht beim Neuladen verloren.
- Für getrennte Geräte jeden persistenten Präsentationszustand zusätzlich im Klassenraum auf dem Server speichern und pollen. Damit bleiben PC, Surface und Beamer nach Neuladen gekoppelt.
- Das Beamerfenster schreibt regelmäßig einen serverseitigen Herzschlag; das Lehrergerät prüft dessen Alter und zeigt den Verbindungszustand an. Die Verbindung muss ohne manuellen Handshake wieder entstehen.
- Jede Nachricht mit Zeitstempel, Nonce, Modul- und Raumkennung gegen falsche Zuordnung und Doppelausführung absichern. Raumgebundene Beamer verwerfen ältere oder raumlose Befehle.
- Nicht nur den letzten Einzelbefehl speichern. Theme, Fokus/Fortschritt, Aufklapper, Karten/Stepper, Medien- und Bildzustand als kompakten Snapshot mitsenden, damit ein nachfolgender Scrollbefehl keinen Videostart oder Bildschluss verdrängt.
- Beamerfenster über Adresszusatz **und** Fragment erkennbar machen. Manche Browser verwerfen bei `file://` den Teil hinter dem Fragezeichen.
- Immer einen Knopf anbieten, nicht nur die Adresse erklären.

### Kopplung abschnittsfein, nicht pixelweise

- Die Lehreransicht ist länger als die Schüleransicht; eine Scroll-Kopplung liegt deshalb systematisch daneben.
- Jeden sinnvollen Block automatisch durchnummerieren und die Nummer übertragen. Sonst springt der Beamer nur an Abschnittsanfänge und bleibt innerhalb langer Abschnitte stehen.
- Nur Schritte senden, die nicht in einem Lehrkraftbereich liegen und sichtbar sind; nicht gewählte Sozialform-Varianten fallen damit heraus.
- Einen Pausenschalter vorsehen. Während der Gruppenarbeit blättert die Lehrkraft in ihren Notizen, der Beamer soll dann stehen bleiben.
- Weiterer Befehlsumfang: Verdunkeln mit Leitfrage, Fokus auf einen Abschnitt, Schriftgröße nur am Beamer, Steuerung des Klassenchecks.
- Bedienelemente spiegeln: Regler, Knöpfe in Demonstrationen und Aufklapper. Sonst muss die Lehrkraft mit der Maus ins Beamerfenster fahren.

### Steuerleiste und Schülerfreigabe

- Eine feste Lehrerleiste nur so breit bauen, dass sie auch bei kleinerem Browserfenster vollständig bedienbar bleibt. Gruppen bilden, Beschriftungen kürzen und bei Bedarf horizontal innerhalb der Leiste scrollen; niemals Controls außerhalb des Viewports abschneiden.
- In der Leiste Beamerstatus, Schritt zurück/weiter, „hier zeigen“, Folge/Pause, Fokus/Verdunkeln, Schriftgröße, Schülerfreigabe und Timer logisch gruppieren.
- Automatisches Folgen entprellen. Ein Schritt gilt erst dann als erreicht, wenn sein stabiler Anker tatsächlich in der Beameransicht aktiv ist; Off-by-one-Fehler zwischen Lehrer- und Schülerstruktur mit einem Ende-zu-Ende-Test prüfen.
- Die Schülerfreigabe aus demselben stabilen Schrittmodell ableiten. Nicht die reine Scrollhöhe der längeren Lehreransicht übertragen.

## Gemeinsamer Timer

- Timer als Raumzustand führen, damit Lehrkraft, Beamer und Lernende dieselbe Restzeit sehen.
- Start, Pause/Fortsetzen, `+1`, `+3` und Ausblenden/Zurücksetzen anbieten. Änderungen der Lehrkraft müssen ohne Neuladen in allen Ansichten erscheinen.
- Anzeige kompakt und stets sichtbar, aber nicht über Inhalt oder Navigation legen. Bei null eindeutig „Zeit ist um“ zeigen und den zugehörigen Klassencheck serverseitig schließen.

## Audiopodcasts als geführte Mediensequenz

- Vor dem Player einen knappen Hörauftrag anzeigen. Ein zugängliches Transkript in nativen `details` sowie eine gut lesbare PDF-Fassung zum Herunterladen für Lehrkraft und Lernende anbieten.
- Cue-Zeitpunkte als überprüfbare Konfiguration führen und daran nacheinander kurze Abschnittskarten aufdecken. Der gesprochene Einstieg und die erste sichtbare Karte müssen inhaltlich zusammenpassen.
- Pro Cue genau einen neuen Gedanken oder Entwicklungsschritt hervorheben. Die Karten als stichpunktartige Orientierung schreiben, nicht als paralleles Transkript.
- Im Selbstlernmodus eigenständiges Hören und Mitlesen ermöglichen. Im geführten Unterricht die Lehrkraft steuern lassen und die hörbare Wiedergabe am Beamer ausgeben.
- Für längere Produktionen zusätzlich eine manuelle Weiter-/Zurücksteuerung der Karten vorsehen, ohne die automatische Kopplung unverständlich zu machen.

## Synchronisierte Audio- und Videowiedergabe

- Im geführten Unterricht nur **eine** hörbare Wiedergabequelle verwenden. Bevorzugt startet, pausiert und springt die Lehrkraft das Medium am Beamer; das Lehrergerät zeigt lediglich Steuerknöpfe oder bleibt stumm.
- Medienbefehle mit stabiler Medien-ID, Aktion und optionaler Zeitposition übertragen. Nach einem Neuladen muss die Kopplung wieder funktionieren.
- Browser-Autoplay-Einschränkungen berücksichtigen: Das Beamerfenster früh durch eine Nutzeraktion öffnen und Wiedergabefehler sichtbar melden. Nicht unbemerkt gleichzeitig im Lehrer- und Beamerfenster starten.

## Kartenraster und Abschnittskarten

- Wiederkehrende Karten mit einheitlicher Innenstruktur und innerhalb eines Rasters möglichst gleicher Höhe gestalten: Ordnungszahl, Zeitraum/Kategorie, Titel, wenige Stichpunkte, optionaler Merksatz.
- Die Ordnungszahl unabhängig von Porträt, Karte oder Illustration immer als erstes Element an derselben Position oben links setzen. Medien dürfen diese Orientierung nicht verschieben.
- Porträts und Illustrationen sparsam einsetzen und mit Namen oder Funktion verknüpfen. Eine inhaltlich notwendige Karte oder Übersicht darf ein eigenes Layout erhalten, soll aber visuell zum Raster gehören.
- Karten auf schmalen Viewports stapeln und in Hell- wie Dunkelmodus auf Überlagerung, abgeschnittenen Inhalt und ausreichenden Kontrast prüfen.

## Bilder und schrittweise Schaubilder

- Inhaltliche Bilder per Klick in einer zugänglichen Vollbildansicht unbeschnitten öffnen; Escape, Fokus-Rückgabe und sichtbaren Schließen-Knopf vorsehen. QR-Codes und reine Bediengrafiken davon ausnehmen.
- Komplexe Schaubilder als fortschreitende Erzählung bauen: ein Basisbild oder handgesetztes SVG, nummerierte Stationen, Zurück/Weiter, „Alles zeigen“ und „Von vorn“.
- Jeder Schritt muss fachlich genau einen neuen Zusammenhang sichtbar machen. Textlegende, Schrittzähler und visuelle Hervorhebung synchron halten.
- Auf Mobilgeräten große Schaubilder in einem klar erkennbaren internen Scrollbereich führen, statt die ganze Seite horizontal zu verbreitern.

## Interaktiver Zeitstrahl

Bei historischer Entwicklung eine echte Slider-Steuerung mit folgenden Eigenschaften anbieten:

- Stationen als Buttons, Cursor mit `role="slider"`, `tabindex="0"` und aussagekräftigem `aria-valuetext`
- Pointer/Touch, Klick auf Linie sowie Pfeiltasten
- alternierende Jahreslabels gegen Überlappung
- bewusst gestaffelte statt zwingend linearer Positionen, wenn Daten dicht liegen
- Karte pro Station mit These, Kontext und Frage nach Fortschritt oder Bruch

Zeitleiste nicht nur dekorativ einsetzen. Jahresabstände und nichtlineare Staffelung transparent erklären.

## SVG-Schaubilder

- Verbindungslinien zuerst zeichnen und deckende Knoten danach darüberlegen.
- Text handsetzen; keine KI-Grafik mit eingebauter Beschriftung nutzen.
- SVG zu PNG rendern und visuell prüfen. Symmetrie, unerwartete Formen, abgeschnittenen Text und Dunkelmodus kontrollieren.
- Inhalt nicht allein durch Farbe codieren.
- Bei einem KI-generierten Hintergrund Fachtext, Pfeile und Nummern nachträglich als HTML/SVG auflegen. Erzeugungsdatum und künstlerischen Charakter in einer Bildunterschrift nennen.

## Bildvergleiche

- Deckungsgleiche Bildpaare nur aus derselben Quelle beziehungsweise als Bearbeitung des ersten Bildes erzeugen.
- Bei berechenbaren Transformationen Browserfilter oder Canvas verwenden und Methode nennen.
- Überblendregler mit festem Wertfeld ausstatten, damit das Layout nicht springt.
- Falschfarben, Simulationen und Annäherungen sichtbar kennzeichnen.
