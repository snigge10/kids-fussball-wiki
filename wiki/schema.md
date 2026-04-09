# Wiki Schema – Kinder Fussball Training

Dieses Dokument definiert Struktur, Seitentypen und Regeln für das Kinder-Fussball-Trainings-Wiki.
Der LLM-Agent schreibt und pflegt das Wiki; Menschen lesen und stellen Fragen.

---

## Ordnerstruktur

```
wiki/
├── schema.md          ← Dieses Dokument (Regeln für den Agenten)
├── index.md           ← Inhaltsverzeichnis (wird automatisch aktualisiert)
├── log.md             ← Append-only Operationsprotokoll
├── technik/           ← Ballkontrolle, Dribbling, Passen, Schuss, Kopfball
├── taktik/            ← Positionsspiel, Pressing, Übergänge, Spielaufbau
├── koordination/      ← Beweglichkeit, Gleichgewicht, Motorik, Reaktion
├── spielformen/       ← Kleine Spiele, Turnierformen, Rondos, 1v1
└── aufwaermen/        ← Aufwärmspiele, Bewegungsspiele, Einstieg
```

---

## Seitentypen

### 1. Übungsseite (`uebung-[name].md`)
Einzelne konkrete Trainingsübung aus einem oder mehreren Videos.

**Pflichtfelder:**
- `# Übungsname`
- `**Kategorie:**` (Technik / Taktik / Koordination / Spielform / Aufwärmen)
- `**Altersgruppe:**` (U6–U8 / U9–U11 / U12–U14 / U15+ / Alle)
- `**Spielerzahl:**` (z.B. 4–8, ab 6, beliebig)
- `**Material:**` (Hütchen, Bälle, Tore, etc.)
- `**Dauer:**` (Minuten oder "variabel")
- `## Beschreibung` – Kurze Zusammenfassung (2–4 Sätze)
- `## Ablauf` – Nummerierte Schritt-für-Schritt-Anleitung
- `## Coaching-Hinweise` – Worauf der Trainer achten soll
- `## Variationen` – Schwerer/leichter, andere Spielerzahlen (optional)
- `## Quellen` – Mindestens eine Quellenangabe (s. Zitierregeln)

### 2. Konzeptseite (`konzept-[name].md`)
Übergreifendes Trainingskonzept oder -methodik (z.B. "Rondos", "Spielformen", "1v1-Training").

**Pflichtfelder:**
- `# Konzeptname`
- `**Kategorie:**`
- `## Was ist das?` – Definition und Zweck
- `## Warum wichtig?` – Methodischer Nutzen
- `## Typische Übungen` – Links zu Übungsseiten
- `## Quellen`

### 3. Altersgruppen-Seite (`altersgruppen/[gruppe].md`)
Überblick über entwicklungsgerechtes Training einer Altersgruppe.

**Pflichtfelder:**
- `# Altersgruppe: [Bezeichnung]`
- `## Entwicklungsstand` – Was können Kinder in diesem Alter?
- `## Trainingsschwerpunkte`
- `## Geeignete Übungen` – Links zu Übungsseiten
- `## Quellen`

---

## Zitierregeln

Jede Seite muss mindestens eine Quelle haben:
```
## Quellen
- [Videotitel](https://www.youtube.com/watch?v=VIDEO_ID) – Kanalname
```

Mehrere Quellen erlaubt und erwünscht. Keine URLs ohne Titel.

---

## Ingest-Workflow (für den Agenten)

1. Transkript aus `input/transcripts/[id].md` lesen
2. Video-ID und Kanal aus Metadaten entnehmen
3. Übungen und Konzepte identifizieren
4. Passende Kategorie und Altersgruppe bestimmen
5. Übungsseite(n) erstellen oder bestehende ergänzen
6. `index.md` aktualisieren (neue Seite eintragen)
7. `log.md` Eintrag anfügen

---

## Query-Workflow (für den Agenten)

Bei Fragen wie "Zeig mir Dribbling-Übungen für U10":
1. `index.md` und `wiki/technik/` durchsuchen
2. Passende Übungsseiten zurückgeben
3. Quellenlinks mitliefern

---

## Lint-Regeln

- Alle Links müssen funktionieren (auf existierende Seiten zeigen)
- Keine Seite ohne `## Quellen`
- Jede Übung in `index.md` eingetragen
- `log.md` immer am Ende anfügen, nie überschreiben

---

## Qualitätsstandards

- Sprache: Deutsch
- Ton: Professionell, präzise, für Trainer geschrieben
- Keine Wertungen über Kanäle oder Trainer
- Bei widersprüchlichen Infos aus verschiedenen Videos: beide Varianten nennen
- Übungsnamen: aussagekräftig, keine Video-Titel übernehmen
