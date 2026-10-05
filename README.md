# Acoustic Report Automation

Acoustic Report Automation ist eine kompakte Portfolio-Anwendung für die deterministische Dokumentenautomatisierung. Sie überführt eine kleine synthetische Tabelle in ein validiertes Domain Model, wertet nachvollziehbare schalltechnische Regeln aus und erstellt einen formatierten Word-Bericht.

Dieses Repository ist eine eigenständige, anonymisierte Implementierung für Software-Engineering-Demonstrationen. Es enthält weder Kundendaten noch Unternehmensvorlagen, produktive Berichte, Datenbanken, Logos, Signaturen oder Dateien aus einem operativen System. Sämtliche Beispielwerte und Dokumentenartefakte sind synthetisch und wurden eigens für dieses Projekt erstellt.

## Motivation

Ich arbeite beruflich im Bereich der technischen Akustik und habe dieses
Projekt aus einem realen Bedarf heraus entwickelt: Wiederkehrende Arbeitsschritte
bei der Erstellung technischer Gutachten sollen automatisiert werden, während
fachliche Berechnungen transparent und durch den Gutachter überprüfbar bleiben.

Diese Portfolio-Version bildet die zugrunde liegenden Software-Engineering-
Konzepte in einer eigenständigen Anwendung ab und verwendet ausschließlich
synthetische Daten und neu erstellte Beispielartefakte.

Technische Berichte verbinden häufig strukturierte Berechnungsergebnisse ...

## Datenfluss

```text
Synthetische XLSX-Datei und JSON-Konfiguration
                |
                v
        Eingabevalidierung
                |
                v
       Typisiertes Domain Model
                |
                v
 Deterministische schalltechnische Bewertung
                |
                v
         Report Context
                |
                v
       DOCX Template-Rendering
                |
                v
 Dynamische Tabellennachbearbeitung
                |
                v
        Fertiger Demo-Bericht
```

## Architektur

Die Anwendung verwendet eine kompakte Schichtenarchitektur:

- `domain` enthält Dataclasses, Validierungsregeln, die energetische Pegeladdition und die kaufmännische Rundung.
- Die Schicht `adapters` liest JSON, XLSX und den neutralen Quellenkatalog ein.
- Die Schicht `documents` erstellt den Template Context, rendert das DOCX und fügt die variable Ergebnistabelle ein.
- Die Schicht `application` koordiniert einen vollständigen Anwendungsfall zur Berichtgenerierung.
- `cli.py` ist der Einstiegspunkt der CLI.

Die Dokumentvorlage und das Tabellenschema sind bewusst klein gehalten. Dadurch lässt sich die gesamte Pipeline nachvollziehen, ohne eine produktive Umgebung kennen zu müssen.

## Deterministische Berechnungen

Die Anwendung führt keine probabilistische oder AI-basierte Verarbeitung durch. Sie:

- validiert erforderliche Tabellenblätter, Spalten, Kennungen und Beziehungen;
- kombiniert Dezibelbeiträge durch energetische Addition;
- rundet Beurteilungspegel mit `Decimal` und `ROUND_HALF_UP`;
- vergleicht jeden gerundeten Wert mit dem konfigurierten Tagesrichtwert;
- ermittelt eine Differenz und einen reproduzierbaren Bewertungsstatus.

Die numerischen Regeln sind als reine Funktionen implementiert und durch Unit Tests abgedeckt.

## Schnellstart

Erforderlich ist Python 3.10 oder neuer.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe -m acoustic_report.cli
```

Das erzeugte Dokument wird unter `output/demo_report.docx` gespeichert.

Die vollständig synthetischen Binärartefakte lassen sich mit folgendem Befehl neu erzeugen:

```powershell
.venv\Scripts\python.exe scripts/create_demo_assets.py
```

## Tests

Die Test-Suite auf Basis der Python-Standardbibliothek wird wie folgt ausgeführt:

```powershell
.venv\Scripts\python.exe -m unittest discover -s tests -t .
```

Die Tests decken folgende Bereiche ab:

- Dezimalformatierung und kaufmännische Rundung;
- energetische Addition und Richtwertbewertung;
- Validierung des Tabellenschemas;
- den vollständigen Ablauf vom synthetischen Projekt bis zur DOCX-Datei;
- die Entfernung nicht aufgelöster Template-Marker und personenbezogener Autorenmetadaten.

## Sicherheit des Repositorys

In dieses Repository gehören ausschließlich generierte Demonstrationsartefakte. Die `.gitignore` schließt Datenbanken, lokale Konfigurationen, Logs, Exporte und reguläre Datenordner aus. Vor einer öffentlichen Veröffentlichung sollte der Inhalt dennoch anhand einer ausdrücklichen Allowlist geprüft werden.

## Geplante Erweiterungen

Spätere Versionen können eine JSON-Schema-Validierung, strukturiertes Logging, umfassendere Prüfungen der Barrierefreiheit von Dokumenten und einen zweiten Eingabeadapter ergänzen. Cloud-Dienste, Web APIs und AI-Komponenten sind bewusst nicht Bestandteil von Version 1.
