### A Context-Aware Assistance Framework for Implicit Interaction with an Augmented Human



#### Primäres Thema / Fragen

Entwicklung eines prozessorientierten context aware Unterstützungs Systems das implizite Interaction mit Menschen ermöglicht

Allgemeine verschachtelte Architektur um Kontext zu erfassen und verwalten 

Context Aware Simulationssystem um beim Autobau zu unterstützen

Erweiterung um ein AR System

Generelles Framework zur Entwicklung weiterer Prozess orientierter Systeme



#### Methoden

Studie mit 6 Teilnehmern

Vergleich von traditionellem System mit Context Aware

jeweils gleiche Aufgaben

einziger Unterschied Context awareness

Labor Tür Zusammenbau

Teilnehmer wurden mit dem System vertraut gemacht

Keine Fragen während des Experiments erlaubt

Teilnehmer ohne Erfahrung mit den Gestellten Aufgaben

&nbsp;	



#### Zentrale Ergebnisse

Context Interpretation Units

&nbsp;	Generic Black boxes

&nbsp;	preliminary context -> final context

&nbsp;	standardisierter in und Output

&nbsp;	final context Kann optional hinzugefügt werden

&nbsp;	

General Context Model

&nbsp;	interpretiert Ergebnisse der CIU

&nbsp;	speichern und zur verfügung stellen von diversen Context Informationen



Technical Framework

&nbsp;	3 Teile

&nbsp;		Context Acquisition

&nbsp;		Context Management

&nbsp;		Context Aware assistance application



Context Acquisition

&nbsp;	Sensoren, Übertragung von Daten und CIUs

&nbsp;	MQTTT

&nbsp;	JSON Daten

&nbsp;	=>

&nbsp; 	Microsoft Kinect 2

 		Tiefen Sensoren

 	Microsoft Holo Lense

 		Positions- und Rotationsdaten

 	Spezielle POIs im Kontext System definiert





Context Management

&nbsp;	Context Receiving

&nbsp;	Context Handling

&nbsp;	Context provison

&nbsp;	=>

&nbsp;	Adapter

&nbsp;	Maßstabsgetreue Simulation der Umgebung

&nbsp;	AR Mapping Entity

&nbsp;	

&nbsp;		

Context Aware assistance application

&nbsp;	Client Server Architektur

&nbsp;	Erhält finalen Kontext

&nbsp;	integriert Modell Logik

&nbsp;	Generiert Anweisungen

&nbsp;	=>

&nbsp;	Head Mounted Display für Instruktionen

&nbsp;	Universelle Windows Anwendung entwickelt

&nbsp;	Visibilty Control

&nbsp;		Avatar darf nichts verdecken

&nbsp;		Avatar wird je nach Distanz unsichtbar

&nbsp;	Progress Control

&nbsp;		Avatar darf nicht zu weit voraus sein (örtlich und zeitlich)

&nbsp;		Position von Avatar und User werden abgeglichen

&nbsp;		Daten der POIs		

&nbsp;	Attention Control

&nbsp;		Avatar zeigt in Richtung relevanter Orte wenn Nutzer in die falsche Richtung schauen

&nbsp;	Feedback Control

&nbsp;		Avatar zeigt User wenn eine Aufgabe abgeschlossen wurde (Daumen hoch Geste)

&nbsp;		

**Ergebnisse der Studie**

Statistischer Vergleich

UEQ-S Score

Likert Scale

Shapiro-Wilk Test

Levene's Test

Normalverteilt

User Experience:

 	Adaptive Simulation besser bewertet

 	Ergebnisse nicht signifikant aber starker Effekt messbar

Context-Aware Feature Ranking:

 	Progress Control am besten für Fehlervermeidung

 	Attention Control am besten für Zeitersparnis

 	Cognitive Load Reduction und Error Reduction => Progress Control

 	Feedback Gesture für Motivation



&nbsp;	



#### Fragen und Kommentare



#### Punkte zur kritischen Auseinandersetzung

