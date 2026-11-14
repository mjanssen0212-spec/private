# Report

## KI Auswahl

* Claude:

  * state of the art
  * für viele der Standard von Code Generierung
* Gemini:

  * verbreitet bei nicht technischen Nutzern
* Deepseek

  * Chinesisches Unternehmen
  * Vergleich USA vs China
* Jetbrains

  * Integriert in IDE
  * Convenience

## 

## Findings



### Claude



* Detaillierte Erklärung der Dateistruktur
* teilweise Erklärung der Regeln



* Error Handling falls tkinter failed
* auch ohne gui verwendbar



* Datei durch Kommentare unterteilt



* Erklärung aller Klassen und Methoden



* Ausgearbeitete GUI, optisch ansprechend
* Zug Historie
* Übersicht verbleibender Figuren
* Anzeigen möglicher Züge nach Figurauswahl
* Erklärung von illegalen Zügen
* Spielbrett rotiert



* Keine Rückfrage bezüglich Positionierung von Fahnen und Bomben (rein zufällig)
* Gibt Empfehlungen bei Rückfragen



* Keine Möglichkeit Spiel frühzeitig zu beenden (außer Anwendung schließen)



* Kurze Erklärung des Spiels bei Anfrage
* Tests







### Gemini



* Wenige Kommentare
* Weniger offensichtlich strukturiert



* Minimalistisches GUI
* Kein Anzeigen Möglicher Züge
* Kein Hinweis bei illegalen Zügen
* Keine Angabe über Zug des gegnerischen Spielers
* Spielbrett starr



* Keine Rückfragen vor Generierung, erst als weitere Schritte



* Kurze Übersicht der Regeln







### Deepseek



* Kommentar zur Erklärung der Datei
* Verweis auf Regeldatei (Besonderheit Regeln nicht als PDF übergeben sondern als Link
* Datei durch Kommentare strukturiert



* Methoden Kommentiert
* Sonderregeln für Aufklärer Kommentiert
* Erklären von Methoden / if-else Zweigen



* GUI minimalistisch (Quadrate)
* Hervorheben von möglichen Feldern nach Figuren Auswahl
* Kein Erklären von Illegalen Zügen
* Zugübersicht auf Zwischenbildschirm
* Figuren "verlieren" nach Zug ihre Farbe
* Spielbrett starr



* Keine Fragen vor erster Version, als offene Punkte nachgefragt







### Jetbrains (openai-gpt-5-5)





* Erste Version nicht ausführbar (Möglicherweise user error inkorrektes kopieren des Ergebnisses?)
* Keine Kommentare



* Code generiert trotz nachfragen



* Minimalistische GUI
* Legale Züge hervorgehoben
* Kein Hinweis über letzten Zug des Gegners
* Zwischenfenster als seperates Fenster, lässt sich verschieben
* Spielbrett starr





## Code Review



### Judge Claude



#### Claude



Gesamt 7.75/10

* sauber strukturiert und gut lesbar
* Abzüge für große UI-Klasse, kleine Überbleibsel und mehrfach hinterlegtes Wissen

Code Smells 7/10

* positiv:

  * Logik und UI getrennt
  * Enums
  * custom exception
* negativ

  * God Class
  * Extrem Lange Regelprüfung (12 return werte)
  * toter Code
  * weggeworfenes Objekt
  * Doppeltes Rendering
  * Magic Numbers

Duplikate 7.5/10

* Seen-Geometrie
* hin-und-her Regel
* UI Texte
* Kleinere Duplikate

  * cover\_text
  * draw\_selection
  * set\_hint
  * Splaten
  * canvas.delete

Lesbarkeit 8.5/10

* positiv

  * sprechende Namen
  * kurze Methoden
  * Annotationen schlüssig
* negativ

  * Datei Länge

    * Aufteilen in game und ui sinnvoll
  * Überlange Zeilen
  * viele Parameter
  * alte Syntax

Kommentare 8/10

* positiv

  * modul docstring
  * Kommentare erklären warum
  * kein auskommentierter Code / TODOs
* negativ

  * Fehlende Erklärungen
  * Fehlende Docstrings
  * Unpräzise Kommentare
  * Unerklärte Konstanten

Logikfehler

* Keine genannt
* Geprüft mit pyflakes, pylint, radon und vulture
* 300 simulierte Zufallspartien endeten regulär und ohne Absturz
* Oberfläche nur gelesen, nicht ausgeführt



#### Gemini



Gesamt 6/10

* für Prototyp gut lesbar und übersichtlich
* Spiellogik und UI stark vermischt
* dadurch schwer testbar und erweiterbar

Code Smells 5/10

* negativ

  * God Class
  * Zu lange Methode (execute\_move)
  * Magic Strings
  * Uneinheitlicher Rangtyp
  * Magic Numbers
  * Namenskollision (self.state)
  * Flag-Variablen (win, draw)
  * Kleinere Punkte

    * verschachtelte Funktion (get\_random\_pieces)
    * self.lakes besser als set

Duplikate 6/10

* Figuren zeichnen
* Koordinaten
* Auswahlprüfung
* Aufstellung
* Gegner bestimmen
* Figur bewegen
* Spielende

Lesbarkeit 7/10

* positiv

  * klare Methodennamen
  * logischer Aufbau
  * moderate Verschachtelung
  * knappe Variablennamen im Kontext verständlich
* negativ

  * Kampflogik schwer zu überblicken
  * Einzeiler gegen PEP 8
  * Sprachen gemischt (englische Bezeichner, deutsche Werte)
  * Fehlende Type Hints

Kommentare 6/10

* positiv

  * Legende der Ränge am Dateianfang
  * Kommentare erklären Fachregeln
* negativ

  * Fehlende Docstrings
  * Redundante Kommentare
  * Versteckte Lücke in has\_movable\_pieces
  * Liegen gebliebene Notiz

Logikfehler

* Spiel kann hängen bleiben (kein Spielende bei blockiertem Spieler)
* Falscher Sieger möglich
* Verteidiger erfährt nichts vom Kampf



#### Deepseek



Gesamt 6/10

* solide Struktur
* Spiellogik weitgehend von GUI getrennt
* Abzüge für String-basierte Logik, zu lange Methoden und drei Fehler

Code Smells 5/10

* positiv:

  * Logik und GUI weitgehend getrennt
* negativ

  * Stringly-typed Logik
  * Untypisiertes Ergebnis (\_resolve\_attack)
  * Unnötige Zustandsänderung (\_has\_movable\_pieces)
  * Vermischte Verantwortlichkeiten
  * Lange Methoden (\_on\_cell\_click, move, \_refresh\_board)
  * Toter Code
  * Magic Values
  * Stilles Abschneiden (zip)
  * Schwer testbar

Duplikate 7/10

* Bewegungslogik
* Zugausführung
* Gegnerermittlung
* GUI-Zustand
* Validierung
* Statustexte

Lesbarkeit 7/10

* positiv

  * klare Gliederung der Datei
  * aussagekräftige Namen
  * verständliches Datenmodell (Dataclasses, PIECE\_DEFS)
* negativ

  * Knappe Koordinaten (fr, fc, tr, tc)
  * Irreführender Name (\_has\_movable\_pieces)
  * Verschachtelte Ternary-Kette
  * Lückenhafte Type Hints

Kommentare 6/10

* positiv

  * Dateikopf (Zweck, Regelquelle, Startbefehl)
  * Kommentare erklären warum
* negativ

  * Fehlende Docstrings
  * Irreführender Kommentar
  * Uneinheitliche Begriffe
  * Redundante Kommentare

Logikfehler

* Zwei-Felder-Regel greift nie
* Gegner erfährt verdeckte Figuren
* Figuren des nächsten Spielers werden sichtbar
* grab\_set() kann unter Linux/X11 abbrechen



#### Jetbrains



Gesamt ca. 6/10

* solide Struktur
* Logik und UI getrennt
* Methoden überwiegend klein
* Typannotationen konsequent
* Schwächen bei Kommentaren, totem Code und Rängen / Spielern als Strings

Code Smells 6/10

* positiv:

  * Logik und UI getrennt
* negativ

  * Toter Code (\_create\_piece\_set)
  * Wirkungslose Logik (\_strategic\_bomb\_positions)
  * Unnötiges Mischen
  * Primitive Obsession
  * Temporäre Zustandsänderung (has\_any\_legal\_move)
  * Vermischte Verantwortung
  * Zu lange Methoden (\_place\_strategic\_army, \_on\_cell\_clicked, \_refresh\_board)
  * Magic Values
  * Umständliche Verzweigung

Duplikate 6/10

* Doppelte Zugregeln
* Doppelte Vorprüfungen
* Kleinere Duplikate

  * Bewegungsrichtungen
  * Spielerwechsel
  * Figur bewegen
  * free\_positions
  * Auswahl zurücksetzen
  * Board-Initialisierung
  * Figurennamen

Lesbarkeit 8/10

* positiv

  * sprechende Namen
  * einheitliche Formatierung und Typannotationen
  * Early Returns halten Verschachtelung niedrig
* negativ

  * \_refresh\_board nicht kompakt
  * \_is\_clear\_straight\_line unnötig lang
  * Ränge nur mit Blick in Tabelle verständlich
  * Fehlender Typalias (Position)

Kommentare 3/10

* negativ

  * Keine Docstrings
  * Einzige Kommentare wiederholen PIECE\_NAMES
  * Fehlende Erklärungen

    * Sonderregeln
    * Strategie der Aufstellung
    * Verhalten bei fehlenden Zugmöglichkeiten

Logikfehler

* Geheime Figuren werden aufgedeckt
* Kampfergebnisse fehlen beim Gegner



#### Vergleich



| KI | Code Smells | Duplikate | Lesbarkeit | Kommentare | Schnitt (berechnet) | Gesamt (Review) |
| --- | --- | --- | --- | --- | --- | --- |
| Claude | 7 | 7.5 | 8.5 | 8 | 7.75 | 7.75 |
| Gemini | 5 | 6 | 7 | 6 | 6 | 6 |
| Deepseek | 5 | 7 | 7 | 6 | 6.25 | 6 |
| Jetbrains | 6 | 6 | 8 | 3 | 5.75 | ca. 6 |

Auffälligkeiten

* Claude in allen vier Kategorien vorne

  * Judge ist selbst Claude, Bias möglich
  * Gegenprobe mit anderem Judge sinnvoll
* Gesamtnoten fast identisch

  * Gemini, Deepseek und Jetbrains jeweils um 6/10
  * Stärken und Schwächen unterscheiden sich trotzdem deutlich
  * Claude mit 7.75/10 klar darüber
* Größte Spanne bei Kommentaren (3 bis 8)

  * Jetbrains: Lesbarkeit 8/10 trotz Kommentare 3/10, gute Benennung fängt einiges auf
  * Deepseek gleich bewertet wie Gemini (6/10), obwohl laut Findings deutlich mehr kommentiert
* Modellierung

  * nur Claude nutzt Enums
  * Gemini, Deepseek und Jetbrains arbeiten mit Strings
* Trennung von Logik und UI

  * bei Claude, Deepseek und Jetbrains vorhanden
  * bei Gemini stark vermischt
  * Claude trotz Trennung mit God Class
* Gemeinsame Schwächen in allen vier Reviews

  * Magic Numbers / Magic Values
  * Lange Methoden
  * Fehlende Docstrings
* Gleiche Duplikate bei Gemini, Deepseek und Jetbrains

  * Gegner bestimmen
  * Figur bewegen
* Ähnliche Logikfehler

  * Gemini und Jetbrains: Verteidiger erfährt nichts vom Kampf
  * Deepseek und Jetbrains: geheime Figuren werden sichtbar
  * Claude: keine genannt
* Einschränkungen der Bewertung

  * Logikfehler uneinheitlich gewertet: bei Deepseek Abzug in der Gesamtnote, bei Gemini und Jetbrains außerhalb der Wertung
  * Prüfung uneinheitlich: nur das Claude-Review nennt Tools und 300 simulierte Partien
  * Claude-Oberfläche nicht ausgeführt, Fehler im GUI-Ablauf dadurch nicht ausgeschlossen
  * Gesamtnote bei Claude als genauer Schnitt, bei Deepseek und Jetbrains gerundet
  * Deepseek-Review: Code nur gelesen, nicht ausgeführt, Fehler also nicht durch Ausführen bestätigt
  * Nur Claude mit halben Punkten bewertet





## Code Erklärung



### Claude



* Kurze Einordnung vorab

  * Zweck der Methode (\_draw\_token zeichnet einzelnen Spielstein auf Tkinter-Canvas)
  * Stratego-artiges Spiel aus dem Code erkannt (Bombe, Fahne, Spion, Stärkewerte)



* Erklärung aller Parameter

  * Forward Reference bei "tk.Canvas" erklärt
  * rank = None bedeutet verdeckter Stein



* Schritt für Schritt in 6 Abschnitten mit Codeausschnitten

  * Stil und Maße bestimmen
  * Stein mit 3D-Effekt zeichnen
  * Mittelpunkt berechnen
  * Verdeckten Stein zeichnen
  * Symbol oder Zahl zeichnen
  * Kurznamen darunter schreiben



* Erklärt auch das Warum

  * Maße hängen von size ab, Stein skaliert mit
  * Zeichenreihenfolge erzeugt den 3D-Effekt
  * Mindest-Linienstärke durch max(2, ...)



* Erklärt allgemeine Konzepte

  * Guard Clause / Early Return
  * Enum-Vergleich mit is



* Tabelle zur Darstellung je Rang
* Rechenbeispiel für size = 100
* ASCII-Skizze des Steins



* Annahmen gekennzeichnet

  * "vermutlich" bei x, y und dem True in \_font
  * rounded\_rect, draw\_sabres, COLOR\_STYLES und \_font nicht sichtbar, aus Namen und Verwendung abgeleitet



* Kleine Ungenauigkeit: Text nennt drei Fälle, Tabelle zeigt vier Zeilen







### Gemini



* Kurze Einordnung vorab

  * Zweck der Methode (\_draw\_token rendert einzelnen Spielstein auf Tkinter-Canvas)
  * Stratego als Beispiel genannt



* Erklärung aller Parameter

  * rank = None bedeutet verdeckter Stein
  * Forward Reference nicht erklärt



* Gliederung nach Themen statt nach Codeablauf

  * Parameter und Funktionskopf
  * Geometrie und 3D-Optik
  * Verdeckt vs. aufgedeckt



* Keine Codeausschnitte, nur einzelne Ausdrücke im Text
* Kein Rechenbeispiel
* Keine Skizze oder Tabelle



* Abschließende Key Takeaways zu Clean Code

  * Vollständige Skalierbarkeit
  * Separation of Concerns
  * Guard Clauses



* Annahmen nicht gekennzeichnet

  * gekreuzte Säbel, dunklere Kantenfarbe und fette Schrift als Tatsache beschrieben
  * Beispielwerte für rank.short ("B", "F", "Sp") nicht aus dem Code ableitbar



* Ungenauigkeiten

  * Oberseite laut Antwort nach oben versetzt, tatsächlich nur unterer Rand um size \* 0.01 gekürzt
  * "vollständig relative Maße", aber Mindest-Linienstärke max(2, ...) ist fester Wert und wird nicht erwähnt
  * Tippfehler ("Dictionairy", "Zielsfeldes")







### Deepseek



* Kurze Einordnung vorab

  * Zweck der Methode (\_draw\_token zeichnet einzelnen Spielstein auf tk.Canvas)
  * Stratego-ähnliches Brettspiel genannt



* Erklärung aller Parameter als Tabelle

  * inklusive Rückgabewert
  * rank = None bedeutet unbekannte Figur
  * Forward Reference nicht erklärt



* Gliederung in 9 Abschnitte, Code Schritt für Schritt mit Ausschnitten

  * Signatur und Parameter
  * Farb-Styling nachschlagen
  * Geometrie
  * 3D-Effekt durch zwei Schichten
  * Zentrum berechnen
  * Fall 1: unbekannte Figur
  * Fall 2: bekannter Rang
  * Didaktische Takeaways
  * Kleine Schwachstellen



* Erklärt auch das Warum

  * Maße relativ zu size, Stein bleibt bei jeder Größe gleich
  * 3D-Effekt als 2D-Trick ("fake extrusion")
  * Mindest-Linienstärke durch max(2, ...)
  * Oberseite unten gekürzt, damit Kante sichtbar bleibt



* Erklärt allgemeine Konzepte

  * Early Return
  * Enum-Vergleich mit is
  * Delegation
  * Single Source of Truth



* 7 didaktische Takeaways
* Kein Rechenbeispiel
* Keine Skizze



* Kritische Einordnung des Codes (Schwachstellen / Diskussionspunkte)

  * Unbenannte Magic Numbers
  * x, y als Ecke nicht offensichtlich, Docstring fehlt
  * String-Keys in style statt TypedDict oder dataclass



* Annahmen nur teilweise gekennzeichnet

  * "vermutlich" bei den Keys von COLOR\_STYLES und dem True in \_font
  * gekreuzte Säbel und Parameter von draw\_sabres als Tatsache beschrieben



* Ungenauigkeiten

  * Takeaway "Guard-Clauses für Schriftgrößen", max(2, size \* 0.04) ist aber Linienstärke und keine Guard Clause
  * x, y und size als Maße des Tokens bezeichnet, tatsächlich des Felds (Stein um inset kleiner)
  * "Farben kommen aus COLOR\_STYLES", Textfarbe kommt aber aus TEXT







### Jetbrains



* Hinweis: Agent greift auf Dateien im Ordner zu, Resultat daher verzerrt

  * Antwort kennt Details außerhalb der Methode (z. B. Key "hover" in COLOR\_STYLES)
  * Nicht direkt mit den anderen drei Antworten vergleichbar



* Kurze Einordnung vorab

  * Zweck der Methode (\_draw\_token zeichnet einzelnen Stratego-Spielstein auf tkinter.Canvas)
  * Rolle im Programm: nur Darstellung, keine Spiellogik



* Erklärung aller Parameter als Tabelle

  * rank = None bedeutet verdeckte Figur
  * Forward Reference nicht erklärt



* Sehr ausführlich, kleinteilig Schritt für Schritt in 10 Abschnitten mit Codeausschnitten

  * Farbstil auswählen
  * Innenabstand und Koordinaten berechnen
  * Stein mit Schatten / Kante zeichnen
  * Mittelpunkt berechnen
  * Verdeckte Figur
  * Position für Rangsymbol
  * Bombe
  * Fahne
  * Zahl oder S für Spion
  * Kurzname
* Einzelne Zeilen und Argumente werden teils mehrfach wiederholt



* Zusätzliche Abschnitte

  * Gesamtbild als Pseudocode
  * Warum rank: Optional[Rank] wichtig ist (statt visible: bool)
  * Durchlauf für sichtbare und verdeckte Figur
  * Übersicht der verwendeten Methoden
  * Kurzes Fazit



* Mehrere Tabellen (Parameter, Style-Keys, Variablen, Anzeige je Rang, rank.short)
* Kleines Rechenbeispiel (inset für size = 60)
* ASCII-Skizze des Steins



* Allgemeine Konzepte kaum benannt

  * Early Return nicht als Muster benannt
  * Enum-Vergleich mit is nicht erklärt
  * Keine Kritik am Code



* Annahmen nur bei rank.short gekennzeichnet ("vermutlich")

  * Durch Dateizugriff nicht beurteilbar, was abgeleitet und was gelesen ist



* Ungenauigkeit: rounded\_rect, draw\_sabres, \_draw\_bomb und \_draw\_flag als "tkinter-Methoden" gelistet, sind aber eigene Hilfsfunktionen







### Vergleich



| Merkmal | Claude | Gemini | Deepseek | Jetbrains |
| --- | --- | --- | --- | --- |
| Wörter | 705 | 411 | 1038 | 1419 |
| Codeblöcke | 7 | 0 | 9 | 34 |
| Tabellen | 2 | 0 | 1 | 6 |
| Rechenbeispiel | ja (size = 100) | nein | nein | klein (size = 60) |
| Skizze | ja | nein | nein | ja |
| Forward Reference erklärt | ja | nein | nein | nein |
| max(2, ...) erklärt | ja | nein | ja | ja |
| Early Return benannt | ja | ja | ja | nein |
| Enum-Vergleich mit is erklärt | ja | nein | ja | nein |
| Annahmen gekennzeichnet | ja | nein | teilweise | nur rank.short |
| Kritik am Code | nein | nein | ja | nein |

Auffälligkeiten

* Kernaussage bei allen gleich

  * Methode zeichnet einzelnen Spielstein
  * 3D-Effekt durch zwei übereinanderliegende Rechtecke
  * rank = None führt zur verdeckten Darstellung
  * Stratego von allen erkannt, obwohl der Name im Code nicht vorkommt
* Umfang stark unterschiedlich

  * Jetbrains rund 3.5-mal so lang wie Gemini
  * Mehr Text bedeutet nicht mehr Inhalt, Jetbrains wiederholt Zeilen und Argumente mehrfach
* Unterschiedliche Zielgruppen

  * Gemini: kompakter Überblick für Erfahrene
  * Claude: Mittelweg aus Erklärung und Konzepten
  * Deepseek: didaktisch, mit Takeaways und Kritik
  * Jetbrains: Einsteiger, erklärt jedes Argument einzeln
* Aufbau

  * Claude, Deepseek und Jetbrains folgen dem Code Schritt für Schritt
  * Gemini gliedert nach Themen und verzichtet auf Codeblöcke
* Alleinstellungsmerkmale

  * Claude: Forward Reference, vollständiges Rechenbeispiel, Grenzen der Antwort offen benannt
  * Gemini: Einordnung in Clean-Code-Prinzipien
  * Deepseek: benennt Schwachstellen des Codes
  * Jetbrains: Pseudocode-Überblick, Durchlauf für sichtbare und verdeckte Figur
* Umgang mit Unsicherheit

  * Nicht sichtbare Hilfsfunktionen nur bei Claude klar als abgeleitet gekennzeichnet
  * Gemini beschreibt Annahmen durchgehend als Tatsachen
* Erfundene Beispielwerte widersprechen sich

  * Major hat bei Claude 8, bei Deepseek 7
  * rank.short: "Major" (Claude), "Sp" (Gemini), "MAJ" (Deepseek), "Hauptm." (Jetbrains)
  * Aus dem Code allein nicht ableitbar
* Fehler sind eher Details

  * Claude: Text und Tabelle uneinheitlich
  * Gemini: 3D-Effekt ungenau, Mindest-Linienstärke fehlt
  * Deepseek: falscher Begriff Guard Clause, Feld und Stein vermischt
  * Jetbrains: eigene Hilfsfunktionen als tkinter-Methoden gelistet
* Einschränkung: Jetbrains hatte Zugriff auf Dateien im Ordner, Ergebnis nicht direkt vergleichbar
