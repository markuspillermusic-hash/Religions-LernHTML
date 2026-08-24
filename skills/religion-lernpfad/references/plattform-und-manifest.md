# Plattform, Manifest und Referenz-Repository

## Quellen der Wahrheit

- Autoren-HTML: fachlicher Inhalt, Aufgaben und semantische Präsentationsanker;
- `module-manifest.json`: Lehrplan, Niveaus, Routen, Versionen,
  Klassenraum-/Beamervertrag, Feedbackaufgaben, Datenschutz, Rechte und QA;
- gemeinsames Repository: ausführbarer Klassenraum-/Präsentationskern,
  Plattformreferenz, Starter und Prüftools;
- Skill: didaktische und technische Entscheidungsregeln.

Diese Ebenen nicht vermischen. Eine Fehlerkorrektur an Timer, QR, Freigabe oder
Beamerfolgen gehört in den gemeinsamen Kern und erhält eine SemVer-Version. Ein
religionsspezifischer Text oder eine Aufgabe gehört in die Modulquelle.

## Manifestpflicht

Bei jeder neuen oder grundlegend überarbeiteten produktiven LernHTML vor dem
Layout ein Manifest nach `assets/module-manifest.schema.json` anlegen. Darin
insbesondere registrieren:

- aktuelle Lehrplanfassung und gA/eA;
- eindeutige Modul-ID und drei getrennte Rollenrouten;
- verwendete Core-, Plattform- und Adapterversion;
- Kalenderlaufzeit und benötigte Livefunktionen;
- semantische Freigabestufen und zu spiegelnde Beamerzustände;
- jede KI-Aufgabe mit ID, Operator, AFB und Niveau;
- Datenschutzroute und bestätigte Nichtpersistenz freier Schülertexte;
- Rechteinventar und Publikationsstatus;
- verpflichtende automatische und echte Browserprüfungen.

`scripts/validate_module_manifest.py` vor Rollen-Build und Release ausführen.
`pending` bei den Rechten blockiert eine unbeschränkte öffentliche
Veröffentlichung.

## Repository verwenden

Im Workspace nach dem Repository `Religions-LernHTML` suchen. Den dortigen
Modulstarter und die deklarierten Paketversionen verwenden. Ist es nicht
vorhanden, die mitgelieferten Manifestressourcen nutzen und transparent
benennen, dass der gemeinsame Runtime-Code noch bezogen werden muss. Niemals
Secrets, interne PDF-Sammlungen, private Bildschirmaufnahmen, Raumdaten oder
ungeklärte Originaltexte in ein öffentliches Repository übernehmen.
