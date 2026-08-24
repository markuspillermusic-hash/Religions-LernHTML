# Medien, Illustration und Rechte

## Konzept vor Produktion

Vor jeder Bildgenerierung eine kurze Bildliste abstimmen:

1. Funktion: Hero, Fall, Station, Porträt, Vergleich oder Atmosphäre
2. gewünschte Aussage und angrenzender Text
3. Stil für die ganze Einheit
4. Seitenverhältnis und Zielgröße
5. Herkunft, Rechte und notwendige Kennzeichnung

Echte Materialien des Nutzers für den zentralen Fall bevorzugen. Wissenschaftliche oder historische Aussage nicht durch rein dekorative Bilder vortäuschen.

## KI-Illustrationen

- Prompt mit konkretem Motiv, Perspektive, Licht und konsistentem Stil schreiben.
- `no text, no lettering, no watermark` verlangen.
- Farbpalette an die CSS-Tokens der Seite koppeln, wenn das Modell Farbvorgaben unterstützt.
- Bildpaare als Bearbeitung derselben Ausgangsdatei erzeugen.
- KI-Ursprung sichtbar nennen; historische Personen als idealisierte Darstellung kennzeichnen.
- Modell, Datum, Prompt, Referenzbilder und Nutzungsbedingungen als Provenienznachweis sichern.

Kein bestimmtes Bildtool voraussetzen. Nur vorhandene, freigegebene Werkzeuge verwenden; fehlende Tools nicht durch ungefragte externe Dienste ersetzen.

## Higgsfield, falls verfügbar

- Wenn Higgsfield ausdrücklich verfügbar oder gewünscht ist, für Recraft `recraft_v4_1` die `colors`-Palette aus den CSS-Tokens der Lernseite ableiten. Bewährte Ausgangspalette: `#d8b96a`, `#7a2e2e`, `#54497e`, `#2a6f6c`, `#f2ecdf`, `#3a2c26`; projektspezifisch anpassen.
- Den Prompt mit `no text, no lettering, no words, no watermark` abschließen und Beschriftungen anschließend als HTML oder SVG handsetzen.
- Ergebnis-URL und Job-ID aus der verfügbaren Jobanzeige sichern. Ist der CDN-Download durch eine Sandbox oder Allowlist blockiert, die Blockade offen benennen und den vorgesehenen lokalen Dateinamen angeben.
- Einen Remote-Fallback höchstens im Autorenentwurf verwenden. Vor öffentlichem Serverbetrieb das Bild lokal ablegen oder den fehlenden Zustand sichtbar lassen; keine dauerhafte Abhängigkeit von einer flüchtigen Ergebnis-URL verschleiern.
- Bildunterschrift bei historischen Motiven beispielsweise: „Künstlerische Deutung (KI-generiert), keine historische Abbildung.“

## Lokal zuerst

- Medien vor Veröffentlichung lokal speichern und relative Pfade verwenden.
- Remote-Fallback nur als vorübergehende Produktionshilfe zulassen und vor Serverbetrieb entfernen.
- Wenn ein CDN-Download blockiert ist, die fehlende Datei und den vorgesehenen Dateinamen klar ausweisen; keinen scheinbar offlinefähigen Zustand behaupten.
- Aussagekräftige Alt-Texte schreiben; rein dekorative Bilder mit leerem Alt-Text behandeln.
- Bei ersetzten Dateien unter stabilem Webpfad eine neue Query-Version in allen Ansichten setzen. Medienmanifeste müssen Query und Fragment vor der Dateisuche entfernen.

## Eigene lokale Videos

- Nur Videos lokal veröffentlichen, für die der Nutzer die nötigen Rechte besitzt. Herkunft und Freigabe knapp dokumentieren.
- Vor der Übernahme Container, Codecs, Dauer, Auflösung, Bildrate, Audiostream und Dateigröße beispielsweise mit `ffprobe` prüfen. Für breite Browserunterstützung H.264/AAC in MP4 bevorzugen, wenn keine andere Vorgabe besteht.
- Quelldatei, lokales Medienziel, Buildkopie und Serverdatei per SHA-256 vergleichen. Ein erfolgreicher Dateikopiervorgang allein reicht nicht.
- Metadaten und erstes Abspielen in Schüler- und Beameransicht testen. HTTP-Range-Anfragen müssen kontrolliert beantwortet werden, damit Springen im Video funktioniert.
- Bei einer Beamerkopplung nur eine hörbare Wiedergabe starten; ein Echo aus Lehrer- und Beamerfenster ist ein Abnahmefehler.

## Fremde Videos und Tonaufnahmen

Fremde audiovisuelle Werke nie als lokale Kopie ausliefern, sobald die Seite öffentlich erreichbar ist. Die Unterrichtsschranke deckt das nicht.

- Zwei-Klick-Lösung verwenden: vor der bewussten Nutzeraktion existiert kein `iframe` und es wird keine Verbindung zum Anbieter aufgebaut.
- Erst der Knopf lädt das Werk von der datensparsamen Variante der Anbieterdomain, möglichst mit Zeitmarke auf die relevante Stelle.
- Daneben einen sichtbaren Direktlink zum Original setzen.
- In der bereichsbezogenen Datenschutzseite erläutern, welche Daten beim Aktivieren an den Anbieter fließen können.
- Eigene Arbeitskopien nur im nicht veröffentlichten Ordner behalten und beim Build gegen ihr Auftauchen im Auslieferungsstand prüfen.

## Rechteprüfung

Für jedes Asset mindestens festhalten: Quelle, Urheber/Rechteinhaber, Abruf- oder Erzeugungsdatum, Lizenz, Bearbeitungsrecht, Namensnennung und Beleg.

- „Im Unterricht verwendet“ bedeutet nicht automatisch „öffentlich im Internet zulässig“.
- § 60a UrhG nicht als pauschale Freigabe für frei zugängliche Websites behandeln.
- Bei Minderjährigen und erkennbaren Personen Einwilligung und Veröffentlichungsumfang gesondert prüfen.
- Zitate kurz, belegt und zweckgebunden halten; vollständige fremde Lehrwerkstexte vermeiden.
- Fonts und Open-Source-Komponenten einschließlich Lizenzdateien dokumentieren.
- Bei lokal eingebundenen QR-, Diagramm- oder UI-Bibliotheken die zugehörige Lizenzdatei mit veröffentlichen und im Medieninventar führen.
