# TRIPLA Compiler und Control Flow Graph Generator

Matthias Janßen - 1871808

## Überblick

Dieses Projekt implementiert einen Compiler für die TRIPLA Programmiersprache mit folgenden Funktionen:

1. **Parser**: Erzeugt Abstract Syntax Trees (AST) aus TRIPLA Quellcode
2. **Code Generator**: Generiert TRAM Assembly Code
3. **Control Flow Graph (CFG) Generator**: Erzeugt Kontrollflussgraphen aus TRIPLA Programmen


## Verwendung

### Interaktiver Modus (Empfohlen)

Starten Sie das Programm ohne Argumente für den interaktiven Modus:

```bash
python main.py
```

Das Programm führt Sie durch folgende Schritte:
1. **Dateiauswahl**: Wählen Sie eine TRIPLA-Datei aus der Liste oder geben Sie einen Pfad ein
2. **Output-Auswahl**: Wählen Sie, was generiert werden soll:
   - `1` - AST (Abstract Syntax Tree)
   - `2` - TRAM Code (Assembly)
   - `3` - CFG (Control Flow Graph)
   - `4` - Alles (AST + TRAM + CFG)

Beispiel-Session:
```
TRIPLA Compiler und CFG Generator
==================================================

Verfügbare TRIPLA Programme:
  1. argsParamsExample.tripla
  2. complex.tripla
  3. condition.tripla
  ...

Dateinummer eingeben (oder vollständiger Pfad): 2

Verarbeite: triplaprograms/complex.tripla

Was soll generiert werden?
  1. AST (Abstract Syntax Tree)
  2. TRAM Code
  3. CFG (Control Flow Graph)
  4. Alles (AST + TRAM + CFG)

Auswahl [1-4]: 4

Verarbeitung läuft...

✓ AST exported to: dotFiles/complex.ast.dot
✓ TRAM code exported to: tram_out/complex.tram
✓ CFG exported to: cfg_out/complex.cfg.dot

✓ Verarbeitung abgeschlossen!
```

### Kommandozeilen-Modus

Für automatisierte Verarbeitung können Sie Kommandozeilenargumente verwenden:

```bash
# Alles generieren
python main.py --file triplaprograms/complex.tripla --all

# Nur AST generieren
python main.py --file triplaprograms/complex.tripla --ast

# Nur TRAM Code generieren
python main.py --file triplaprograms/complex.tripla --tram

# Nur CFG generieren
python main.py --file triplaprograms/complex.tripla --cfg

# AST und CFG generieren
python main.py --file triplaprograms/complex.tripla --ast --cfg

# Ohne Flags: generiert alles (AST + TRAM + CFG)
python main.py --file triplaprograms/complex.tripla
```

### Separates CFG-Tool (optional)

Alternativ können Sie das separate CFG-Tool verwenden:

```bash
python dfa_main.py <input.tripla> [--out <output.dot>]
```

Beispiel:
```bash
python dfa_main.py cfg_examples/complex.tripla
```


### Visualisierung mit Graphviz

Nachdem DOT-Dateien generiert wurden, können Sie diese mit Graphviz visualisieren:

```bash
# AST visualisieren
dot -Tpng dotFiles/complex.ast.dot -o dotFiles/complex.ast.png

# CFG visualisieren
dot -Tpng cfg_examples/complex.cfg.dot -o cfg_examples/complex.cfg.png
```

## Ausgabedateien

Das Programm erzeugt folgende Dateien:

- **`dotFiles/*.ast.dot`** - Abstract Syntax Trees im DOT-Format
- **`tram_out/*.tram`** - TRAM Assembly Code
- **`cfg_examples/*.cfg.dot`** - Control Flow Graphs im DOT-Format

## Projektstruktur

```
├── main.py                 # Hauptprogramm für AST und TRAM
├── cfg_main.py            # Hauptprogramm für CFG
├── graphbuilder.py        # CFG Implementierung
├── compiler.py            # TRAM Code Generator
├── triplalex.py           # Lexer
├── triplayacc.py          # Parser
├── syntax.py              # AST Definitionen
├── triplaprograms/        # TRIPLA Beispielprogramme
├── cfg_examples/          # CFG DOT-Dateien
├── dotFiles/              # AST DOT-Dateien
└── tram_out/              # TRAM Assembly Dateien
```


## Anforderungen

- Python 3.10+
- PLY (Python Lex-Yacc)
- Graphviz (für Visualisierung)

## Installation

```bash
pip install ply
```

Graphviz Download: https://graphviz.org/download/
