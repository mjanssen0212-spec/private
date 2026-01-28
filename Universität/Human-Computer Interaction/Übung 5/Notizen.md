# Diskussion: Ergebnisse und Bewertung der Arbeit

**Schmidt et al. (UIST 2024)**
*Natural Expression of a Machine Learning Model’s Uncertainty Through Verbal and Non-Verbal Behavior of Intelligent Virtual Agents*

---

## 1. Ziel der Arbeit

* Untersuchung, wie Unsicherheit eines Machine-Learning-Modells über virtuelle Agenten kommuniziert werden kann
* Fokus auf natürliche, soziale Vermittlung statt numerischer oder explizit erklärender Darstellungen
* Betrachtung von Unsicherheit als kommunikatives Signal in der Mensch‑KI‑Interaktion
* Abgrenzung von der reinen Unsicherheitsberechnung hin zur Wahrnehmung durch Nutzer:innen

---

## 2. Methodischer Kern

* Mehrstufiger Pipeline-Ansatz zur kontrollierten Analyse

* Erhebung menschlicher Unsicherheitsausdrücke:

  * Beantwortung von Fragen mit unterschiedlichem Schwierigkeitsgrad
  * Aufzeichnung verbaler und non‑verbaler Reaktionen

* Annotation der wahrgenommenen Unsicherheit:

  * Mehrere Rater:innen
  * Bewertung der Unsicherheitsstärke
  * Inter- und Intra-Rater-Reliabilität im niedrigen bis mittleren Bereich

* Übertragung auf virtuelle Agenten:

  * Synthetische Erzeugung verbaler Unsicherheitsmarker
  * Parametrische Abbildung non‑verbaler Signale auf einen 3D-Agenten
  * Verzicht auf überzeichnete oder emotionale Darstellung

* Machine-Learning-Modell:

  * Input: kontinuierlicher Konfidenzwert des Systems
  * Output: zeitlich koordinierte verbale und non‑verbale Verhaltenssequenzen

* Nutzerstudie:

  * Bewertung der wahrgenommenen Unsicherheit
  * Analyse von Varianz, Stabilität und Generalisierbarkeit

---

## 3. Zentrale Ergebnisse

### Wahrnehmbarkeit von Unsicherheit

* Wahrgenommene Unsicherheit steigt mit modellierter Unsicherheit
* Zusammenhang insgesamt monoton, aber nicht linear
* Sehr hohe und sehr niedrige Unsicherheitswerte werden nur eingeschränkt differenziert
* Kommunikation vermittelt eher die Richtung als die exakte Stärke von Unsicherheit

---

### Rolle der Multimodalität

* Kombination aus verbalen und non‑verbalen Signalen deutlich wirksamer als Einzelmodalitäten
* Subtile non‑verbale Hinweise (Blick, Mimik) besonders einflussreich
* Bestätigung multimodaler Verarbeitung sozialer Signale

---

### Subjektivität der Wahrnehmung

* Hohe Varianz in den Bewertungen der Teilnehmenden
* Nur moderate Übereinstimmung zwischen verschiedenen Rater:innen
* Deutliche Schwankungen auch innerhalb einzelner Personen
* Wahrnehmung stark abhängig von individuellen Erwartungen und Interpretationen

---

### Generalisierbarkeit über Agenten hinweg

* Keine signifikanten Unterschiede zwischen verschiedenen Agenten
* Agentenmerkmale wie Geschlecht, Stimme oder Erscheinung ohne systematischen Effekt
* Unsicherheitsverhalten nicht an spezifische Agenten gebunden

---

## 4. Einordnung der Ergebnisse

* Unsicherheit kann sozial und natürlich vermittelt werden
* Nutzer:innen reagieren sensibel auf subtile multimodale Signale
* Präzise Kalibrierung der wahrgenommenen Unsicherheit nicht möglich
* Keine Differenzierung unterschiedlicher Unsicherheitsarten

---

## 5. Stärken der Arbeit

* Klar formulierte Fragestellung
* Methodisch stringenter, transparenter Aufbau
* Kontrollierbarer Pipeline-Ansatz statt Black-Box-Lösung
* Subjektive Wahrnehmung als zentraler Untersuchungsgegenstand
* Hohe Relevanz für Trust-in-AI, HCI und virtuelle Agenten

---

## 6. Schwächen und Kritikpunkte

* Relativ kleine und kulturell homogene Stichproben

* Starke Abhängigkeit von subjektiven Ratings mit hoher Varianz

* Fehlender Vergleich mit bestehenden Systemen oder Praxis-Baselines

* Konzeptionelle Einschränkungen:

  * Unsicherheit als eindimensionale Größe modelliert
  * Keine Unterscheidung zwischen epistemischer und aleatorischer Unsicherheit
  * Keine Kommunikation der Ursachen von Unsicherheit

* Eingeschränkte Übertragbarkeit:

  * Labor-Setting
  * Kurze, isolierte Interaktionen
  * Keine Aussagen zu Langzeiteffekten auf Vertrauen oder Nutzung

---

## 7. Diskussionsfragen

* Reicht es aus, Unsicherheit ausschließlich über ihre Stärke zu kommunizieren?
* Sollten unterschiedliche Arten von Unsicherheit unterschiedlich ausgedrückt werden?
* Ist die hohe Varianz in den Bewertungen ein Modellproblem oder eine Eigenschaft menschlicher Wahrnehmung?
* Wie viel Unsicherheit ist in interaktiven KI-Systemen sinnvoll oder wünschenswert?
* Welche ethischen Risiken entstehen durch die soziale Inszenierung von Unsicherheit?

---

## 8. Fazit

* Unsicherheit lässt sich wirkungsvoll über soziale Signale vermitteln
* Wahrnehmung von Unsicherheit ist subjektiv und nur begrenzt steuerbar
* Starker HCI- und Designbeitrag
* Offene Fragen zur erklärbaren und differenzierten Unsicherheitskommunikation
