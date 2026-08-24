# KI-gestütztes Aufgabenfeedback

Diese Referenz gilt, sobald eine Religions-LernHTML individuelle KI-Rückmeldung zu Schülerlösungen anbieten soll. Ziel ist formative Hilfe zur Überarbeitung einer bereits erarbeiteten Antwort – keine automatische Benotung und kein Ersatz für die Lehrkraft.

## Didaktische Eignung

Feedback nur für Aufgaben anbieten, wenn alle folgenden Bedingungen erfüllt sind:

- Die Lernenden erstellen eine eigene, zusammenhängende Lösung zu einem konkreten Material, Fall oder Argument.
- Operator, Anforderungsbereich und erwartete Denkbewegung sind eindeutig bestimmt.
- Ein serverseitiges fachliches Raster nennt Mindestbestandteile, mögliche starke Wege, typische Fehlschlüsse und zulässige Alternativen.
- Die Aufgabe profitiert von Rückmeldung zu Inhalt, Begründung, Textbezug oder Urteil – nicht nur von einer eindeutigen Richtig/Falsch-Auswertung.
- Die Antwort verlangt keine privaten Glaubensbekenntnisse, Gesundheitsdaten, Familienangaben oder andere sensible Selbstauskünfte.

Geeignet sind besonders materialgebundenes Zusammenfassen, Analysieren, Erläutern, Vergleichen, Erörtern und Beurteilen in Q12/Q13. Nicht geeignet sind spontane Stimmungsbilder, persönliche Reflexionsfelder, Brainstormings, reine Beobachtungsnotizen, Live-Abstimmungen, deterministische Zuordnungen und Selbstchecks. In Jahrgangsstufe 5 bis 11 standardmäßig kein individuelles KI-Korrekturangebot einbauen, sofern es nicht ausdrücklich fachlich und datenschutzbezogen beauftragt ist.

## Urteile, Stellungnahmen und christliche Perspektiven

- Eine Position oder ein Ergebnis wird nicht danach bewertet, ob es mit der
  persönlichen Meinung der Lehrkraft, des Modells oder einer vermuteten
  Mehrheitsmeinung übereinstimmt. Rückgemeldet werden ausschließlich
  Sachrichtigkeit, Materialbezug, offengelegte Maßstäbe, Argumentaufbau,
  Einwände, Abwägung und Folgerichtigkeit.
- Gegensätzliche Urteile müssen bei vergleichbarer Begründungsqualität
  gleichwertig rückmeldbar sein. Das serverseitige Raster nennt deshalb
  zulässige Alternativen und darf keine gewünschte Schlussposition verstecken.
- Persönliche Stellungnahmen sind nur feedbackgeeignet, wenn keine sensible
  Selbstauskunft nötig ist. Die Aufgabenformulierung weist sichtbar darauf hin,
  dass die Überzeugung selbst nicht bewertet wird.
- Wo es zum Lehrplan und Material passt, kann statt einer privaten Meinung ein
  Sachverhalt „aus christlicher Sicht“ beurteilt werden. Dann prüft das Feedback
  die fachlich korrekte Anwendung benannter biblischer, theologischer oder
  sozialethischer Maßstäbe, ohne den Lernenden persönlichen Glauben zu
  unterstellen.

## Verbindlicher Aufgabenvertrag

Die öffentliche HTML enthält nur nicht vertrauliche Metadaten, beispielsweise:

```html
<div class="task"
     data-feedback-task="plessner-zusammenfassung"
     data-feedback-operator="zusammenfassen"
     data-feedback-afb="I">
  …
</div>
```

Die serverseitige Aufgabenregistrierung führt unter derselben stabilen ID:

- Modul- und Lehrplanbezug einschließlich Stand/Version;
- Niveau `gA` oder `eA`;
- exakten Operator und Anforderungsbereich;
- Materialauszug oder sichere Materialreferenz;
- fachliche Kriterien, Mindestbestandteile, typische Fehler und erlaubte Alternativen;
- maximale Eingabelänge, Mindestlänge und Ausgabeumfang;
- Prompt- und Rasterversion.

Erwartungshorizonte, Musterlösungen und vollständige Bewertungsraster niemals in die Schülerdatei schreiben. Bei mehreren Eingabefeldern entscheidet der Vertrag ausdrücklich, ob jedes Feld einzeln oder die Aufgabe als zusammengehöriges Antwortbündel rückgemeldet wird.

## Sichere Architektur

```text
Schülerbrowser ── Raumcode + Aufgaben-ID + Antwort ──> eigener PHP-Endpunkt
                                                        │
                                                        ├─ Raum offen und Feedback freigegeben?
                                                        ├─ Raum gehört einem aktiven Lehrerkonto?
                                                        ├─ Aufgaben-ID serverseitig registriert?
                                                        ├─ Länge, Rate- und Kostenlimit eingehalten?
                                                        ├─ persönlicher oder Organisationsschlüssel?
                                                        ├─ Raster + Operator + Material ergänzen
                                                        └─ serverseitiger Modellaufruf
                                                                  │
Schülerbrowser <── validiertes strukturiertes Feedback ────────────┘
```

- Lehrkräfte verwenden persönliche Konten. Der eigene Schlüssel wird einmal im zentralen Lehrerbereich hinterlegt und mit einem separaten serverseitigen Master-Secret verschlüsselt. Administratoren können zusätzlich einen Organisationsschlüssel für freigeschaltete schulinterne Konten hinterlegen. Bei einem Aufruf gilt die feste Priorität: persönlicher Schlüssel der Raumbesitzerin/des Raumbesitzers, sonst Organisationsschlüssel, sonst deaktiviert.
- Schlüssel nie pro LernHTML oder pro Raum duplizieren. Ein zweites Lehrgerät benötigt nur dieselbe geschützte Anmeldung. Die Oberfläche liefert ausschließlich boolesche Zustände wie „persönlich eingerichtet“, „Schulzugang verfügbar“ und „für diesen Raum freigegeben“ – nie Schlüsseltext oder entschlüsselbares Material.
- Schlüssel niemals in HTML, JavaScript, `localStorage`, URL, Export, Log, Repository oder Raumdatei speichern. Verschlüsselter Tresor, Master-Key, SQLite-Datenbank und serverseitige Aufgabenraster liegen außerhalb des Webroots mit minimalen Dateirechten.
- Der öffentliche Raumstatus enthält nur `feedbackEnabled`, Limits und anonyme Nutzungszähler. Er enthält keinen Schlüssel, keine Musterlösung und keinen individuellen Antworttext.
- Schülerantworten nur für den einzelnen Aufruf verarbeiten und in der eigenen Anwendung nicht persistieren. Inhaltslogging deaktivieren; technische Logs enthalten höchstens Zeit, Raum, Aufgaben-ID, Status, Token-/Kostenwert und eine zufällige Anfrage-ID.
- Den Modellaufruf serverseitig über die aktuelle Responses API mit `store: false` ausführen. Offizielle Datenaufbewahrungsbedingungen vor der Veröffentlichung erneut prüfen und in der Speicherinformation transparent erklären.
- Antworttexte als nicht vertrauenswürdige Nutzdaten behandeln. Anweisungen innerhalb einer Schülerantwort dürfen Systemvorgaben, Raster oder Ausgabeformat nicht verändern.

## Konten, Organisationen und Zugriff

- Ein Kursraum erhält beim Anlegen unveränderlich die ID des angemeldeten Lehrerkontos und optional dessen Organisation. Normale Lehrkräfte können nur eigene Räume auflisten, verändern, verlängern, für Feedback freigeben oder beenden; Administration darf unterstützend alle Räume sehen.
- Schulinterne Lehrkräfte können einen gemeinsamen, vom Administrator hinterlegten Organisationsschlüssel nutzen. Externe Lehrkräfte hinterlegen ihren eigenen Schlüssel. Der Plattformbetreiber kann Konten sperren; die geänderte Auth-Version beendet bestehende Sitzungen.
- Neue Lehrkräfte verwenden eine öffentliche, spamgebremste Zugriffsanfrage. Name, Schule, Fächer, Region und Nutzungsgrund werden moderiert; eine Annahme erzeugt eine einmalige, zeitlich begrenzte Einladung. Ohne funktionierenden Mailversand bleibt der Einladungslink genau einmal im Administratorbereich kopierbar.
- Die produktive Lehreranmeldung setzt Argon2id, sichere Cookies, CSRF, Login-Bremse und persönliche Passwörter ein. Ein früheres gemeinsames Lehrerpasswort darf ausschließlich die einmalige Ersteinrichtung autorisieren.

## Aktivierung und Raumdauer

- Ohne serverseitig erreichbaren Schlüssel bleibt der Knopf `KI-Feedback generieren` deaktiviert; ein kurzer Hinweis erklärt: „Für diesen Raum nicht freigeschaltet.“
- Die Lehrkraft schaltet Feedback bewusst pro Raum ein und sieht Modell, Kostenlimit, verbleibendes Kontingent und Datenschutzhinweis. Ohne im Konto oder in der Organisation verfügbaren Schlüssel kann die Freigabe nicht aktiviert werden.
- Der Schalter verlinkt eine dauerhaft erreichbare, modulspezifisch zutreffende Datenschutzinformation. Vor schulischer Aktivierung werden Verantwortlichkeit, Rechtsgrundlage, Betroffeneninformation, Anbieter-/Transferbeziehung und schulische Freigabe dokumentiert; die technische Verfügbarkeit eines Schlüssels ersetzt diese Prüfung nicht.
- Der Raum darf eine mehrwöchige Sequenz begleiten; Standard sind 42 Tage. Das Ablaufdatum wird per Kalender gewählt und kann innerhalb der serverseitigen Höchstfrist verlängert oder verkürzt werden. Die längere Raumdauer verlängert nicht die Speicherung von Schülerantworten – diese bleiben transient.
- Beim Ablauf oder Beenden des Raums wird Feedback sofort gesperrt. Kontoschlüssel bleiben vom Raum getrennt und werden niemals mit ihm exportiert.
- Die Lehrkraft kann den persönlichen Schlüssel jederzeit ersetzen oder entfernen. Ein Administrator kann den Organisationsschlüssel ersetzen oder entfernen. Danach liefern betroffene Räume beim nächsten Verfügbarkeitscheck den deaktivierten Zustand, ohne den übrigen Klassenraum zu beenden.

## Rückmeldeformat

Mit Structured Outputs ein festes Schema erzwingen, zum Beispiel:

- `aufgabenbezug`: kurze Bestätigung, welche Aufgabe und welcher Operator geprüft wurden;
- `staerken`: zwei konkrete, belegte Stärken der vorliegenden Antwort;
- `naechster_schritt`: höchstens drei priorisierte Verbesserungen;
- `operator_feedback`: Rückmeldung zur geforderten Denkbewegung;
- `fachliche_hinweise`: Korrekturen oder fehlende Differenzierungen ohne vollständige Musterlösung;
- `ueberarbeitungsimpuls`: eine konkrete Aufforderung zur nächsten Fassung;
- `unsicherheit`: Kennzeichnung, wenn Materialbezug oder Antwort für ein belastbares Feedback nicht ausreichen.

Keine Note, Punktzahl oder behauptete amtliche Bewertung ausgeben. Die Oberfläche bezeichnet das Ergebnis als „formative KI-Rückmeldung nach dem hinterlegten Lehrplanraster“ und weist sichtbar darauf hin, dass Fehler möglich sind.

## Missbrauchs-, Kosten- und Datenschutzgrenzen

- Pro Raum, Aufgabe und Browser nur eine kleine Zahl von Versuchen innerhalb eines Zeitfensters zulassen; zusätzlich Tages- und Raumkostenlimit setzen.
- Zusätzlich stündlich pro Lehrerkonto und monatlich pro Organisation begrenzen. Der öffentliche Endpunkt erhält eine grobe IP-Bremse und akzeptiert bei gesetztem `Origin` nur dieselbe Website.
- Eingabe- und Ausgabelänge begrenzen, Parallelaufrufe drosseln und bei ausgeschöpftem Kontingent einen verständlichen Zustand anzeigen.
- Keine Namen verlangen. Vor dem Absenden knapp auffordern, keine personenbezogenen oder sensiblen Angaben einzutragen.
- Feedback nicht für Benotung, Prüfungsentscheidungen, Anwesenheit oder Profile verwenden. Keine langfristigen Antwortverläufe oder Leistungsprofile bilden.
- Speicherinformation, Verantwortlichkeit, Rechtsgrundlage, Auftrags-/Anbieterverhältnis und schulische Freigabe vor Produktivbetrieb gesondert klären; nicht als automatisch rechtssicher bezeichnen.

## Qualitätssicherung

1. Jede freigegebene Aufgabe mit schwacher, mittlerer, starker, leerer, fachlich falscher und prompt-injizierender Beispielantwort testen.
2. Prüfen, ob das Feedback tatsächlich Operator, Material und Niveau trifft und alternative vertretbare Lösungen akzeptiert.
3. Gegen Erwartungshorizont und Lehrplanraster durch eine Lehrkraft gegenlesen; „lehrplanorientiert“ nicht mit „amtlich zertifiziert“ verwechseln.
4. Ohne Schlüssel, bei ungültigem Raum, unbekannter Aufgaben-ID, zu kurzer Antwort, Rate-Limit, Anbieterfehler und Kostenlimit klare Zustände testen.
5. Öffentlichen Raumstatus, Serverdateien, Exporte, Browserstorage und Logs auf Schlüssel, Schülertext und Erwartungshorizont prüfen.
6. Modell-, Prompt-, Raster- und Lehrplanversion protokollieren, ohne den Schülertext zu speichern. Stichproben nach Änderungen erneut durchführen.
7. Mit zwei Lehrerkonten prüfen, dass Raumlisten, Freigaben und Schlüssel strikt getrennt sind; anschließend Organisationsschlüssel-Fallback und Kontosperre testen.
8. Jede Urteilsaufgabe mit zwei fachlich vertretbaren, gegensätzlichen
   Ergebnissen testen. Bei vergleichbarer Argumentationsqualität darf keines
   allein wegen seines Ergebnisses besser oder schlechter rückgemeldet werden.
