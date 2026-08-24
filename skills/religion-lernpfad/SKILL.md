---
name: religion-lernpfad
description: Erstellt, überarbeitet und prüft interaktive deutschsprachige Lern-HTMLs für den katholischen oder allgemeinen Religionsunterricht, besonders Sekundarstufe II und bayerischen LehrplanPLUS. Verwenden bei Lernpfaden, interaktiven Unterrichtseinheiten, vollständigen und kompakten Unterrichtsmodi, Selbstlernseiten, digitalen Hefteinträgen, Live-Klassenchecks, Audio-/Podcast-Lernsequenzen, religiösen Oberstufenthemen, „gleiches Format wie letztes Mal“ sowie bei der Weiterentwicklung vorhandener Religions-Lernseiten. Deckt Didaktik, gA/eA, Prüfungsvorbereitung, Lehrer-/Schüler-/Beamerrollen, zentrale Lehrerkonten, geräteübergreifende Kursräume, abschnittsgebundene Freigabe, lokale Mitschrift, optionale operatorengestützte KI-Rückmeldung, Medienkonzept und fachliche QA ab. Für produktive Servertrennung, Kontoplattform, synchronen Live-Unterricht oder Deployment zusätzlich lernseite-server-portierung verwenden.
---

# Religion-Lernpfad

Eine fachlich belastbare, zugängliche und im Unterricht tragfähige Lernseite erstellen. Bestehende Entscheidungen respektieren und vorhandene Vorlagen weiterentwickeln.

## Zuerst prüfen

1. Projektordner vollständig sichten: vorhandene Lernpfad-HTML, `vorlage-*.html`, `BRIEFING.md`, Jahresplan, Medien und frühere Korrekturen.
2. Bestehende Vorlage bevorzugen. Layout, Speicherformat, IDs und Interaktionsmuster nur ändern, wenn die Aufgabe es verlangt oder ein belegter Fehler vorliegt.
3. Fehlende Angaben nur erfragen, wenn sie das Ergebnis wesentlich verändern: Thema, Jahrgangsstufe, Bundesland/Lehrplan, Stundenumfang, Ausgangsmaterial und zentraler Fall.
4. Keine Plattform, Serverarchitektur oder Integration erfinden. Genannte Systeme und Zielpfade exakt verwenden; bei unklarer Infrastruktur erst prüfen oder fragen.

## Referenzen gezielt laden

- Für Modulmanifest, Referenz-Repository, Versionsbindung und die Grenze zwischen Skill und ausführbarem Code [references/plattform-und-manifest.md](references/plattform-und-manifest.md) lesen.
- Für Lernlogik, Jahrgangsstufen, gA/eA, Aufgaben und fachliche Sorgfalt [references/pedagogik.md](references/pedagogik.md) lesen.
- Für Abschnitte, Rollen, lokale Mitschrift, Selbstcheck und ByCS-Übergabe [references/struktur-und-rollen.md](references/struktur-und-rollen.md) lesen.
- Für Gestaltung, Voll-/Kompaktmodus, Handschrift, Audio-/Podcast-Lernsequenzen, schrittweise Schaubilder, Beamer-Fernsteuerung, Timer und Mediensteuerung [references/design-und-interaktionen.md](references/design-und-interaktionen.md) lesen.
- Sobald Klassenraum, Live-Abstimmung, Freigabe oder getrennte Lehrer-/Schüler-/Beameransichten vorkommen, [references/klassenraum-standard.md](references/klassenraum-standard.md) vollständig lesen und den gemeinsamen Kern statt einer seitenspezifischen Neuentwicklung verwenden.
- Sobald KI-gestütztes Aufgabenfeedback geplant, eingebaut oder geprüft wird, [references/ki-feedback.md](references/ki-feedback.md) vollständig lesen. Das Feedback bleibt formativ, operatoren- und materialgebunden; API-Schlüssel und Bewertungsraster gehören ausschließlich auf den Server.
- Vor Bildproduktion oder Medienübernahme [references/medien-und-rechte.md](references/medien-und-rechte.md) lesen.
- Vor Abgabe oder nach größeren Änderungen [references/qa.md](references/qa.md) lesen und `scripts/validate_learning_html.py` ausführen.

## Arbeitsablauf

1. **Rahmen und Modulvertrag klären.** Zielgruppe, Kompetenzziel, verfügbare Zeit, Geräte und spätere Nutzung festhalten; bei produktionsnahen Modulen das Manifest zu Beginn anlegen und fortlaufend pflegen.
2. **Fakten prüfen.** Datierungen, Zitate, Lehrplanbezüge, populäre Beispiele und strittige Aussagen anhand aktueller Primärquellen oder belastbarer Fachliteratur verifizieren.
3. **Didaktischen Faden bauen.** Mit einem konkreten irritierenden Fall beginnen, ihn in drei bis fünf Stationen erschließen und in Bilanz und Transfer wieder aufnehmen.
4. **Umfang modellieren.** Zuerst eine vollständige Fassung erhalten. Redundanz innerhalb der Stationen entfernen; zentrale Erfahrungen, tragende Materialien und notwendige Denkerstimmen nicht ausdünnen. Bei Bedarf zusätzlich einen ausdrücklich bezeichneten Kompaktmodus aus derselben Quelle erzeugen.
5. **Inhalt vor Oberfläche schreiben.** Materialien, kurze Arbeitsaufträge, Gesprächsimpulse, Musterlösungen, Selbstcheck und Abschluss zuerst inhaltlich fertigstellen.
6. **Unterrichtsregie entwerfen.** Vorbereitung, Raumöffnung und konkrete Aktivitäten trennen. Sozialform und Alternativweg vorab wählen; Abstimmung, Kommentar oder Klassencheck erst an der fachlich passenden Stelle anbieten. Bei Live-Unterricht genau einen Raum und den verbindlichen Klassenraumkern konfigurieren.
7. **Niveaus differenzieren.** Bei LehrplanPLUS gA als selbstständig verständlichen Grundtext führen; ausschließlich eA-relevante Vertiefungen sichtbar gekennzeichnet in native `details.ea` auslagern.
8. **Rollen sauber markieren.** Lehrkraftinhalte im Autorenentwurf mit `data-rolle="lehrer"` auszeichnen. Einen clientseitigen Schalter nie als echten Zugriffsschutz darstellen.
9. **Interaktionen zweckgebunden umsetzen.** Jede Interaktion muss Beobachtung, Entscheidung, Sicherung oder Rückmeldung leisten. Native HTML-Elemente vor Spezialkomponenten verwenden.
10. **Lernstand sichern.** Eingaben lokal speichern, klar auf Verlustmöglichkeiten hinweisen und Lernstand als versionierte portable Datei exportier- und wieder importierbar machen.
11. **Medien konzipieren.** Erst Medienfunktion, Stil und Rechte klären, dann erzeugen oder übernehmen. Längere Audioangebote mit fokussiertem Hörauftrag, knappen Begleitkarten und zugänglichem Transkript planen; komplexe Schaubilder schrittweise aufbauen und Beschriftungen als HTML/SVG handsetzen.
12. **Prüfen.** Syntax, aktive und inerte Template-IDs, Sprungziele, Rollen, Voll-/Kompaktmodus, Speicher-/Exportpfad, Selbst- und Klassencheck, Tastatur, Mobilansicht, Beamer, Dunkelmodus, Druck und fachliche Aussagen testen. Bei Drei-Rollen-Builds zusätzlich `scripts/validate_classroom_contract.py` und einen echten Live-Vertragstest in getrennten Browserkontexten ausführen.
13. **Produktionsvertrag registrieren.** Stabile `moduleSlug`, Rollen-URLs, Paketversionen, Freigabestufen, Rechteinventar und Feedback-Aufgaben im Manifest sowie serverseitig registrieren. Der Seitenadapter enthält nur öffentliche IDs; Konto, Besitz, Schlüssel, Raster, Kontingente und Protokollierung bleiben im geschützten Plattformkern.

## Entwurfs- und Produktionsmodus unterscheiden

- **Lokaler Entwurf:** Eine einzelne offlinefähige HTML darf Lehrer- und Schülerrollen enthalten. Klar ausweisen, dass ein JavaScript-Passwort oder verstecktes HTML keinen Schutz bietet.
- **Produktive Veröffentlichung:** Lehrerinhalt aus der öffentlichen Datei entfernen und serverseitig schützen; Beamer- und Schülerroute getrennt erzeugen. Ist die zentrale Lehrerplattform vorhanden, muss die Lehrerroute deren persönliche Anmeldung und Kontobesitz verwenden; kein neues gemeinsames Seitenpasswort bauen. Dafür `lernseite-server-portierung` verwenden.
- Niemals ein echtes Passwort, Token, Schülerdaten oder serverbezogene Zugangsdaten in HTML, JavaScript, Skill oder Repository schreiben.

## Unverhandelbare Qualitätsregeln

- Didaktik erleben lassen, nicht als Methode beschriften.
- Sinnoffenheit nicht mit Beliebigkeit verwechseln; Positionen fair und argumentativ darstellen.
- Primärtexte bevorzugen und Quellen sichtbar nennen; Urheber- und Nutzungsrechte nicht aus „Unterrichtsgebrauch“ ableiten.
- Musterlösungen als Begründungskette schreiben, nicht nur als Stichwort.
- Fachbegriffe bei der ersten Verwendung knapp definieren und, wenn hilfreich, etymologisch erschließen.
- Aufgaben an konkrete Beobachtungen, Materialien, Vorhersagen oder Unterrichtserfahrungen binden; reine generische Essayfragen vermeiden.
- Keine Behauptung oder Fehlvorstellung erst einführen, nur um sie anschließend zu widerlegen; an tatsächlichem Vorwissen, Material oder plausiblen Schülerfragen ansetzen.
- Einzelne Arbeitsphasen normalerweise auf höchstens sieben Minuten anlegen; knapp planen und Bonuszeit bewusst nachgeben.
- Lehrerskript, Hinweise und Erwartungshorizonte als Vorschläge und fachliche Orientierung formulieren, nicht als bevormundende Regieanweisung.
- Vorbereitung kompakt oder einklappbar halten; im Unterricht muss der Übergang von Planung zu konkreter Durchführung optisch eindeutig sein.
- Keine KI-Bilder mit eingebautem Fachtext verwenden. KI-Inhalte kennzeichnen und menschlich prüfen.
- Schüleransicht ohne Lehrerblöcke gesondert prüfen.
- Gemeinsamen Klassenraumkern nie seitenweise forken: Fachspezifika als kleine deklarative Adapter bauen; technische Korrekturen zuerst im Kern, dann in alle Builds ausrollen und per Live-Vertragstest absichern.
- Ausführbaren gemeinsamen Code im Referenz-Repository versionieren. Der Skill enthält Regeln und Prüfverfahren, nicht die heimliche zweite Kopie der Laufzeit.
- KI-Feedback nie direkt aus der Schülerseite an einen Modellanbieter senden. Keine API-Schlüssel, Erwartungshorizonte oder internen Bewertungsraster in öffentliche Dateien oder Raumzustände schreiben.
- Lehrerkonten, Organisationen, API-Schlüssel und Kursraumbesitz nie seitenspezifisch nachbauen. Die LernHTML bindet den zentralen Plattformadapter deklarativ ein; der Raum enthält lediglich technische Freigaben und anonyme Zustände.
- Keine Live-Schaltung oder Serveränderung ohne ausdrücklichen Auftrag.

## Übergabe

Zuerst den erreichten Unterrichtsnutzen nennen. Danach Dateien verlinken, offene fachliche oder rechtliche Nachweise benennen und nur wirklich nötige nächste Schritte aufführen.
