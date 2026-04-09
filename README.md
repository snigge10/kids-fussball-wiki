# Kids Fussball Wiki 🟢⚽

Eine systematische Wissensdatenbank für Kinder- und Jugendfussball-Training, aufgebaut aus 167 TrainerKick-Videos und strukturiert für den schnellen Einsatz im Trainingsalltag.

## Was ist das?

Dieses Repository enthält eine umfangreiche Trainingsübungsdatenbank, die automatisch aus YouTube-Transkripten des TrainerKick-Kanals extrahiert und aufbereitet wurde. Jede Übung ist als Markdown-Datei dokumentiert und nach Trainingskategorien sowie Altersgruppen organisiert.

## Struktur

```
wiki/
├── technik/        – 107 Übungen (Passen, Dribbeln, Schuss, Ballannahme)
├── taktik/         – 102 Übungen (Pressing, Positioning, Spielaufbau)
├── spielformen/    –  93 Übungen (Kleine Spiele, Rondos, 1v1)
├── aufwaermen/     –  53 Übungen (Fun Games, Einstiege, Warm-ups)
├── koordination/   –  46 Übungen (Motorik, Agilität, Schnelligkeit)
├── altersgruppen/  – Übersichten nach Altersklasse (U6–U8, U9–U11, U12–U14, U15+)
├── konzepte/       – Trainingsphilosophie und Methodik
├── index.md        – Vollständiger Index aller Übungen
├── STATISTIK.md    – Zahlen und Fakten zur Datenbank
└── LESENSWERT.md   – Empfohlener Einstieg
input/
├── transcripts/    – Rohe YouTube-Transkripte
├── exercises/      – Extrahierte Übungsdaten
└── metadata/       – Video-Metadaten
```

## Schnelleinstieg

- **Neu hier?** → [`wiki/LESENSWERT.md`](wiki/LESENSWERT.md)
- **Alle Übungen auf einen Blick** → [`wiki/index.md`](wiki/index.md)
- **Zahlen & Fakten** → [`wiki/STATISTIK.md`](wiki/STATISTIK.md)
- **Aufbau einer Übungsseite** → [`wiki/schema.md`](wiki/schema.md)

## Wie ist eine Übung aufgebaut?

Jede Übungsdatei enthält:

- Kategorie, Altersgruppe, Spielerzahl, Material, Dauer
- Klare Beschreibung und Trainingsziel
- Schritt-für-Schritt Ablauf
- Altersgerechte Variationen und Anpassungen
- Coaching-Hinweise für Trainer
- Link zum Originalvideo auf YouTube

## Altersgruppen

| Gruppe | Alter | Schwerpunkt |
|--------|-------|-------------|
| U6–U8  | 5–8 Jahre | Freude am Spiel, Grundmotorik |
| U9–U11 | 9–11 Jahre | Technik, einfache Taktik |
| U12–U14 | 12–14 Jahre | Taktik, Spielverständnis |
| U15+ | ab 15 Jahre | Leistungsorientiertes Training |

## Datengrundlage

- **167 Videos** vom TrainerKick YouTube-Kanal
- **401 Wiki-Seiten** (Mehrfach-Kategorisierung möglich)
- **~2,5 MB** aufbereitete Transkripte
- Sprachen: Deutsch (162 Videos), Englisch (5 Videos)
- Automatische Extraktion via Claude AI

## Lizenz

Dieses Repository dient ausschließlich privaten und nicht-kommerziellen Zwecken im Rahmen der Trainingsplanung. Die Videoinhalte sind Eigentum des jeweiligen Urhebers (TrainerKick).
