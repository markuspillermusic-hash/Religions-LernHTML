# Verbindlicher Klassenraum- und Präsentationsstandard

Diese Referenz ist immer zu lesen, sobald eine Religions-LernHTML einen Klassenraum, Live-Abstimmungen, Abschnittsfreigaben oder getrennte Lehrer-, Schüler- und Beameransichten verwendet. Sie beschreibt den gemeinsamen Produktvertrag. Seitenspezifische Sonderlösungen sind nur als Adapter zulässig.

## Eine Quelle, drei Rollen, ein Raum

- Aus einer Autorenquelle drei physisch getrennte Ausgaben bauen: öffentliche Schüleransicht, serverseitig geschützte Lehreransicht und öffentliche Beameransicht.
- Lehrerhinweise und Erwartungshorizonte dürfen weder in Schüler- noch Beamerdatei vorhanden sein. CSS-Verstecken ist kein Zugriffsschutz.
- Genau einen sechsstelligen Stundencode pro Lernseite und Lerngruppe verwenden. Derselbe Raum steuert Freigabe, Abstimmungen, Beamer, Timer und Ablaufzustand.
- Räume bleiben für mehrwöchige Sequenzen standardmäßig 42 Tage erhalten, sind neutral benennbar und gehören serverseitig genau einem persönlichen Lehrerkonto. Nach Anmeldung sind sie auch auf einem zweiten Lehrgerät auffindbar; dadurch kann der Unterricht am PC vorbereitet und am Surface fortgeführt werden. Administratoren dürfen für Supportzwecke alle Räume sehen, normale Lehrkräfte ausschließlich die eigenen. Beim Anlegen wird das Ablaufdatum mit einem Kalenderfeld gewählt; beim aktiven Raum kann es innerhalb der serverseitigen Höchstfrist jederzeit verlängert oder verkürzt werden. Das genaue Datum bleibt sichtbar; ein Raum lässt sich jederzeit bewusst früher beenden.
- Mehrwöchige Raumzustände liegen modulweise in einem persistenten Datenverzeichnis außerhalb von Webroot und Betriebssystem-Tempordnern. Ein täglicher, idempotenter Wartungslauf löscht exakt abgelaufene Zustände und bewahrt aktive Räume; ein Serverneustart darf Räume nicht verlieren.
- Keine Namen oder individuellen Lerntexte serverseitig speichern. Der Server hält nur Raumzustand, anonyme Summen, ausdrücklich moderierte Beiträge, Timer, Freigabe und Präsentationszustand.

## Verbindlicher gemeinsamer Kern

Wenn im Arbeitsbereich `_shared/classroom-v1` vorhanden ist, sind `classroom-core.js`, `presentation-core.js`, `classroom.css` und die lokale QR-Bibliothek daraus die einzige technische Quelle. Jeder Build kopiert diese Dateien unverändert in das jeweilige Modul. Keine zweite Raumverwaltung und keine seitenweise Kopie mit eigenen Fehlerkorrekturen anlegen.

Bei produktiver zentraler Lehrerplattform ergänzt der Build nur einen kleinen Auth-/Raumadapter. Die deklarative Konfiguration enthält mindestens eine stabile `moduleId`, eine weltweit innerhalb der Installation eindeutige `moduleSlug`, Rollen-URLs und – falls vorhanden – den relativen eigenen `feedbackEndpoint`. Persönliche Anmeldung, Organisation, Schlüssel-Tresor, Raumbesitz, Kontingente und Audit liegen ausschließlich im Plattformkern außerhalb des Webroots.

Seitenadapter dürfen fachliche Interaktionen ergänzen, aber nur über dokumentierte Attribute und Befehle:

- stabile Präsentationsanker: `data-beamer-anchor`, `data-step-id` oder `data-beamer-step`;
- spiegelbare Auswahl: `data-classroom-control-group` plus `data-classroom-control-value`;
- spiegelbare Aufklapper erhalten beim Start einen stabilen `data-classroom-details-key`;
- Medien tragen stabile IDs beziehungsweise `data-youtube`/`data-youtube-id`;
- fachliche Adapter hören auf das gemeinsame Präsentationsereignis und müssen idempotent sein.

## Lehreransicht

Die technische Raumverwaltung steht am Anfang der Seite und bleibt so knapp wie möglich. Nach dem Öffnen eines Raums zeigt sie:

- Raumcode, neutralen Raumnamen, Schülerlink und lokal erzeugten QR-Code;
- Kalenderfeld für die anfängliche Gültigkeit sowie ein zweites Kalenderfeld zum nachträglichen Verlängern oder Verkürzen;
- Beamer öffnen, Beitritt zeigen und Verbindungsstatus;
- vorbereitete Räume zum Gerätewechsel;
- gemeinsamen Timer und Ergebnisexport;
- verständliche Lade-, Leer- und Fehlerzustände.

Die Lehrerroute verwendet die zentrale persönliche Anmeldung. Ist noch kein Konto vorhanden, führt sie zur einmaligen Ersteinrichtung beziehungsweise zum Login und kehrt danach zur angeforderten LernHTML zurück. Ein bestehender gemeinsamer Passwortschutz darf nur einmalig den Übergang autorisieren und ist danach kein produktiver Anmeldeweg mehr.

Der QR-Code wird mit einer lokal ausgelieferten, versionierten Bibliothek erzeugt. Bei einem Fehler bleibt immer ein direkter Schülerlink sichtbar. QR-Codes sind keine Unterrichtsbilder und werden nicht von der allgemeinen Bild-Lupe erfasst.

Solange die Raumverwaltung im sichtbaren Lehrer-Lesebereich liegt und ein Raum geöffnet ist, zeigt der Beamer zwingend die Beitrittsansicht mit QR-Code, direktem Link und Raumcode. Automatisches Scrollfolgen darf diesen Zustand nicht durch einen Inhaltsanker überschreiben. Erst beim Verlassen der Raumverwaltung wird wieder der aktuelle semantische Inhaltsanker gesendet. Diese Regel gilt auch nach Neuladen und beim Öffnen eines vorbereiteten Raums.

Die große Kopfzeile der Lehreransicht ist einklappbar. Navigation und aktive Unterrichtssteuerung bleiben erreichbar. Der Zustand darf nicht zu abgeschnittenen oder horizontal scrollenden Hauptnavigationen führen.

Auch die Kopfzeile der Schüleransicht ist einklappbar, sofern sie mehr als die dauerhaft benötigte Navigation enthält. Rollenwahl, Status- oder Markenbereich dürfen verschwinden; die Navigation, Raumverbindung und ein klar beschrifteter Knopf zum Wiedereinblenden bleiben erreichbar. Lehrer- und Schülerzustand werden getrennt lokal gespeichert.

Die feste Präsentationsleiste bleibt auf üblichen Lehrerbildschirmen immer einzeilig und mindestens 58 px hoch. Schaltflächen dürfen weder umbrechen noch ihre Höhe wechseln; die wechselnde Bezeichnung des Präsentationshalts wird in einem begrenzten, mit Ellipse gekürzten Feld dargestellt. Nur auf schmalen Geräten darf die Leiste innerhalb derselben festen Höhe waagerecht bedienbar sein.

## Schüleransicht und Freigabe

- Ohne Raum bleibt die Seite als klar bezeichneter Selbstlernpfad zugänglich.
- Mit Raumlink wird der Code automatisch übernommen; eine zweite Eingabe ist nicht nötig.
- Zu Beginn ist nur die erste Freigabestufe offen. Spätere Abschnitte erhalten eine verständliche Sperrkarte und sind aus Fokus- und assistiver Reihenfolge genommen.
- Die Freigabe wird aus demselben semantischen Präsentationsschritt wie die Beameranzeige abgeleitet. Niemals Pixelhöhen oder bloße Scrollprozente als Freigabestufe verwenden.
- Für verschachtelte Anker bis zum nächsten Vorfahren mit einer bekannten `releaseStage` aufsteigen. Ein Unterelement darf nicht auf einen Fantasie- oder Fallbackabschnitt verweisen.
- Freigaben sind im normalen Unterricht monoton: Zurückscrollen sperrt bereits bearbeitete Abschnitte nicht wieder. Eine Rücksetzung ist eine eigene bewusste Lehreraktion.
- Direkte Navigationssprünge, Pfeilsteuerung, „Hier zeigen“ und automatisches Scrollfolgen müssen denselben Abschnitt freigeben.

## Beameransicht

- Vor dem ersten Unterrichtsbefehl nur Bereitschaft oder Beitritt zeigen.
- Danach genau einen aktuellen Hauptabschnitt anzeigen. Der folgende Abschnitt darf nicht am unteren Rand sichtbar sein.
- Der aktuelle Abschnitt ist ein eigener Viewport mit internem vertikalem Scrollen. Der Beamer folgt der semantischen Leseposition der Lehreransicht, berücksichtigt deren angeheftete Kopfzeile und bleibt innerhalb langer Abschnitte synchron.
- Das kontinuierliche Nachführen wird gedrosselt, zusammengefasst und am Beamer geglättet. Eine Hysterese an Ankergrenzen verhindert A–B–A-Sprünge; nach dem Ende des Lehrer-Scrollens wird die exakte Zielposition persistent gespeichert.
- Der Beamer darf keine Eingabefelder, Lösungen oder Lehrerhinweise enthalten.
- Nach Neuladen oder Gerätewechsel den letzten vollständigen Präsentationszustand aus dem Raum rekonstruieren.

## Persistenter Präsentationszustand

Ein einzelner flüchtiger Befehl reicht nicht: Schnelle Scroll-, Theme- oder Detailbefehle können Medienbefehle sonst vor dem nächsten Serverabruf überschreiben. Jede gespeicherte Präsentationsnachricht enthält deshalb zusätzlich einen kompakten `_classroom`-Snapshot mit:

- Theme;
- aktuellem Fokusanker und Fortschritt innerhalb dieses Ankers;
- Modus `content`, `join` oder `dim`;
- offenen/geschlossenen Details;
- aktiven Karten-, Tab- und Schrittwerten;
- gewünschtem Audio-/Video-/YouTube-Zustand;
- Bild-Vollansicht einschließlich explizitem Schließzustand.

Persistente Serverbefehle werden in Sendereihenfolge geschrieben. Ein späterer Auto-Follow-Befehl trägt den Medienzustand weiter, statt ihn zu verlieren. Wechselt der Fokus fachlich zu einem anderen Anker, wird der alte Medien- oder Bildzustand kontrolliert beendet.

## Spiegelbare Interaktionen

Folgende Lehreraktionen müssen ohne Bedienung im Beamerfenster gespiegelt werden:

- Hell-/Dunkelmodus;
- Öffnen und Schließen gemeinsamer `details`;
- Karten, Tabs, Zeitleistenpunkte, Regler und schrittweise Schaubilder;
- Bild vergrößern und wieder schließen;
- lokales Audio/Video starten, pausieren, fortsetzen, stoppen und positionieren;
- YouTube nach Zwei-Klick-Prinzip ausschließlich am Beamer laden;
- Beitritt, Verdunkelung und aktueller Präsentationshalt.

Die Lehreransicht bleibt bei Medien stumm. Ein Klick auf „Video laden“ sendet den Befehl an den Beamer und erzeugt keinen zweiten lokalen Player. Autoplay-Blockaden werden sichtbar erklärt.

## Gemeinsamer Timer

Der Timer ist Raumzustand, kein lokaler Countdown. Er enthält mindestens Bezeichnung, Dauer, Restzeit, `running`, `startedAt` und `endsAt`. Standardbedienung:

- frei wählbar 1–180 Minuten;
- Start;
- Pause/Fortsetzen;
- `+1` und `+3` Minuten;
- Ausblenden/Zurücksetzen.

Lehrer, Schüler und Beamer berechnen aus demselben Serverzustand dieselbe Restzeit. Der Lehrer sieht die Steuerung in Raumverwaltung und kompakter Präsentationsleiste; am Beamer erscheint nur der große Countdown.

Beide Lehrersteuerungen müssen denselben Raum-API-Adapter zur Laufzeit verwenden. Der Vertragstest bedient ausdrücklich auch Start, Pause/Fortsetzen, Zeitaufschlag und Ausblenden in der festen Präsentationsleiste; ein erfolgreicher Test nur über die große Raumverwaltung genügt nicht.

## Live-Aktivitäten

- Abstimmungen stehen an der fachlich passenden Stelle, nicht gesammelt in der Raumverwaltung.
- Vor dem Start keine Antwortsummen oder Lösungen öffentlich ausliefern.
- Antwortwechsel korrigieren die vorhandene Stimme. Private Begründungen bleiben lokal.
- Ergebnisanzeige ist eine ausdrückliche Lehrerentscheidung und passt vollständig in den Beamer-Viewport.
- Keine Abstimmung einsetzen, wenn die Fachinformation bereits eine eindeutige Begriffsentscheidung vorgegeben hat. Dann eine Diagnose-, Zuordnungs- oder Begründungsaufgabe mit unmittelbarem Erwartungshorizont verwenden.

## Gemeinsame Kartenwände

- Eine lokale Kartenwand ist nur sinnvoll, wenn sie ausdrücklich ein persönliches Sortierwerkzeug ist. Für bloße private Gedanken genügen lokal gespeicherte Textfelder.
- Soll die Klasse Gedanken zusammentragen, wird eine gemeinsame, kategorisierte Kartenwand an der fachlich passenden Stelle verwendet. Sie gehört zum gemeinsamen Klassenraumkern und zum selben sechsstelligen Raum.
- Lernende reichen ausschließlich kurze anonyme Karten ein. Die Oberfläche fordert ausdrücklich dazu auf, keine Namen oder persönlichen Angaben zu verwenden.
- Neue Karten sind zunächst `pending` und werden weder Schülern noch Beamer gezeigt. Die Lehrkraft gibt sie einzeln frei oder verwirft sie; nur `approved` wird öffentlich ausgeliefert.
- Die Lehrkraft kann Einreichungen öffnen/schließen und die Wand bewusst leeren. Vorhandene freigegebene Karten bleiben beim Schließen sichtbar.
- Beamer und Schüleransicht ordnen freigegebene Karten in denselben konfigurierten Kategorien an. Kategorien und stabile Wand-ID stammen aus dem Seitenadapter, Technik und Moderationsvertrag aus dem gemeinsamen Kern.
- Anzahl und Textlänge werden serverseitig begrenzt. Karten werden mit dem Raumende oder Ablauf gelöscht und nicht in individuelle Lernstands- oder Abstimmungsexporte übernommen.

## KI-gestütztes Aufgabenfeedback

Wenn ein solches Feedback vorgesehen ist, gilt zusätzlich [ki-feedback.md](ki-feedback.md). Der Raumzustand enthält höchstens, ob Feedback freigeschaltet ist, ein Kosten-/Nutzungslimit und anonyme Zähler. Weder API-Schlüssel noch individuelle Schülertexte werden dort gespeichert. Ohne serverseitig verfügbaren Schlüssel bleibt der Feedbackknopf deaktiviert und erklärt knapp den Grund.

API-Schlüssel werden nicht in einer einzelnen LernHTML und nicht pro Raum erfasst. Jede Lehrkraft verwaltet ihren persönlichen Schlüssel im zentralen geschützten Lehrerbereich; Administratoren können zusätzlich einen verschlüsselten Organisationsschlüssel hinterlegen. Auf der Lernseite erscheint nur der boolesche Zustand „Schlüssel verfügbar“ sowie ein bewusster Schalter `KI-Feedback für diesen Raum`. Persönlicher Schlüssel hat Vorrang vor Organisationsschlüssel; der Schlüssel selbst wird nach dem Absenden niemals erneut angezeigt oder an den Browser zurückgegeben.

## Kontrast und Zugänglichkeit

- Bedienknöpfe in beiden Themes mindestens WCAG-AA-Kontrast erreichen; normale Schrift 4,5:1.
- Erwartungshorizonte erhalten explizite Vorder- und Hintergrundfarben für Hell und Dunkel, statt auf Vererbung zu vertrauen.
- Alle Controls per Tastatur bedienbar, Fokus sichtbar, Touch-Ziele mindestens 44 px.
- 390 × 844, 1024 × 768, 1280 × 720, 1920 × 1080 und 200-%-Zoom ohne horizontalen Seitenüberlauf prüfen.

## Verbindliche Abnahme

Vor Veröffentlichung mindestens:

1. `validate_learning_html.py` für jede Rolle;
2. `validate_view_bundle.py` für Rollentrennung und Schrittidentität;
3. `validate_classroom_contract.py` für gemeinsamen Kern, API, Kalenderlaufzeit, QR, Kartenwand, beide Timersteuerungen und Cachevertrag;
4. lokalen Browserlauf der Präsentationsadapter;
5. Live-Vertragstest in getrennten Lehrer-, Schüler- und Beamer-Kontexten;
6. Beamer-Neuladen nach Theme-, Karten-, Details- und Medienänderung;
7. Screenshot- und Kontrastprüfung;
8. Löschen aller Testräume;
9. exakte Dateisicherung, dateigenaues Deployment, Hashvergleich und Cacheprüfung.
10. Neustart-/Persistenzprüfung, tägliche Ablaufbereinigung und ein integritätsgeprüftes Backup außerhalb des Webroots.

Ist KI-Feedback aktiviert, kommen Vertragstests für deaktivierten Zustand ohne Schlüssel, persönlichen und Organisationsschlüssel, Raumbesitz und Kontentrennung, serverseitige Aufgabenregistrierung, Rate-Limit, nicht gespeicherte Schülertexte, strukturiertes Ausgabeformat sowie verständliche Fehler- und Kostenlimit-Zustände hinzu.

Ein DOM-Test allein genügt nicht. Der Live-Test muss einen Raum mit gewähltem Ablaufdatum wirklich anlegen, verlängern und verkürzen, über einen zweiten Kontext beitreten, im sichtbaren Klassenraumbereich die unverdrängbare Beitrittsansicht prüfen, mindestens einen Folgeabschnitt freigeben, den Timer über Raumverwaltung und Präsentationsleiste prüfen, eine moderierte Karte einreichen/freigeben/verwerfen, eine einzeilige Werkzeugleiste und monotones Nachführen kontrollieren sowie QR und einen Präsentationszustand nach Neuladen wiederherstellen. Geänderte gemeinsame JS-/CSS-Dateien erhalten immer eine neue Cache-Version in allen Build-Skripten; gemischte Kernversionen sind ein Abnahmefehler.
