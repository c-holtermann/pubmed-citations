# PubMed-Skripte

## Anforderungen

- Python 3
- Requests-Bibliothek (`pip install requests`)
- BeautifulSoup-Bibliothek (`pip install beautifulsoup4`)

Diese Skripte ermitteln für eine Liste von PubMed-Publikationen, wie häufig dieses zitiert werden und geben eine Mediawiki-Tabelle mit diesen Informationen aus. Intermediär wird eine XML-Datei erstellt, die die Liste der zitierenden Arbeiten für jede Veröffentlichung enthält. Es wird die PubMed E-Utilities API genutzt, um Zitationsdaten abzurufen.

Autor: Christoph Holtermann  
Datum: 2023-12-21  
Lizenz: GNU GENERAL PUBLIC LICENSE Version 3 

## Verwendung

Als Grundlage muss eine Datei vorliegen, die eine Literaturliste enthält, Beispiel siehe unten.

### Schritt 1 - Skript: `pubmed_citation_retrieval.py`

#### Eingabe
- Das Skript extrahiert die PubMed-IDs direkt aus einer Vorlagendatei mit dem Namen `zotero_export.txt`. Stelle sicher, dass diese Datei vorhanden ist und die benötigten Informationen enthält.

#### Ausgabe
- Das Skript generiert eine XML-Datei mit dem Namen `pubmed_results.xml`, die Informationen zu PubMed-Veröffentlichungen und ihren zitierenden Arbeiten enthält.

#### Verwendung
1. Installiere die erforderlichen Bibliotheken: `pip install requests beautifulsoup4`.
2. Führe das Skript aus: `python pubmed_citation_retrieval.py`.

## Beispiel

- Für ein Beispiel zum Format der Vorlage siehe das bereitgestellte Beispiel:

```plaintext
{{Literatur| DOI = 10.1016/j.jclinepi.2017.04.026| ISSN = 1878-5921| Band = 89| Seiten = 218-235| Autor=David S. Riley, Melissa S. Barber, Gunver S. Kienle, Jeffrey K. Aronson, Tido von Schoen-Angerer, Peter Tugwell, Helmut Kiene, Mark Helfand, Douglas G. Altman, Harold Sox, Paul G. Werthmann, David Moher, Richard A. Rison, Larissa Shamseer, Christian A. Koch, Gordon H. Sun, Patrick Hanaway, Nancy L. Sudak, Marietta Kaszkin-Bettag, James E. Carpenter, Joel J. Gagnier| Titel = CARE guidelines for case reports: explanation and elaboration document| Sammelwerk = Journal of Clinical Epidemiology| Sprache = eng| Datum = 2017-09| undefined = 28529185}}
```

### Schritt 2 - Skript zur Erstellung einer MediaWiki-Tabelle

Dieses Skript liest die Ergebnisse des PubMed-Zitationsabfrage-Skripts und erstellt eine MediaWiki-Tabelle mit den erhaltenen Informationen.

#### Verwendung:

Führe das Skript aus: python create_mediawiki_table.py.

#### Eingabe:

Das Skript erwartet die Existenz der Datei pubmed_results.xml (vom PubMed-Zitationsabfrage-Skript generiert) und der Vorlagendatei zotero_export.txt.

#### Ausgabe:

Das Skript erstellt eine MediaWiki-Tabelle und schreibt sie in eine Datei namens mediawiki_table_output.txt.

#### Beispiel:

Das Beispiel der Ausgabe sieht wie folgt aus:

```
{| class="wikitable"
|+ Publikationen und Rezeption H. Kiene
|-
! Nummer !! Publikation !! Anzahl zitierende Publikationen !! Zitierende Publikationen (begrenzt auf zehn)
|-
| 1 || {{Literatur| DOI = 10.1016/j.jclinepi.2017.04.026| ... }} || [https://pubmed.ncbi.nlm.nih.gov/?linkname=pubmed_pubmed_citedin&from_uid=28529185 5] ... || [https://pubmed.ncbi.nlm.nih.gov/12345678 1], [https://pubmed.ncbi.nlm.nih.gov/23456789 2], ... [https://pubmed.ncbi.nlm.nih.gov/34567890 10]
|}
```
