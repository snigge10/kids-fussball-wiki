# Wissensdatenbank Kinder Fussball Training – Datenbasis

## Zweck

Dieser Ordner enthält alle **Rohdaten** (Input), die aus YouTube-Kanälen zu Kinder- und Jugendfussball-Training extrahiert wurden. Die Daten bilden die Grundlage für die Wissensdatenbank.

---

## Ordnerstruktur

```
input/
├── channels/         # Kanal-Metadaten & Video-Listen
│   └── [kanal-id]/
│       ├── channel_info.md       # Kanalname, Beschreibung, Statistiken
│       └── video_list.md         # Liste aller Videos mit URL, Titel, Datum
│
├── transcripts/      # Rohe Transkripte / Untertitel
│   └── [video-id].md             # Ein Transkript pro Video
│
├── exercises/        # Strukturierte Übungen (extrahiert aus Transkripten)
│   └── [video-id]_exercises.md   # Übungen mit Kategorie, Alter, Beschreibung
│
└── metadata/         # Verarbeitungsstatus & Indexdateien
    ├── index.md                  # Gesamtübersicht aller verarbeiteten Videos
    └── processing_log.md         # Was wurde wann verarbeitet
```

---

## Workflow

### Schritt 1 – Kanäle definieren
Trage gewünschte YouTube-Kanäle in `channels/` ein. Nutze das Skript `fetch_channel.py` um die Video-Liste automatisch abzurufen.

### Schritt 2 – Transkripte extrahieren
Für jedes Video in der Video-Liste wird das Transkript (Untertitel) mit `yt-dlp` heruntergeladen und in `transcripts/` als Markdown gespeichert.

### Schritt 3 – Übungen strukturieren
Claude analysiert die Transkripte und extrahiert strukturierte Trainingsübungen nach folgendem Schema:
- **Übungsname**
- **Altersgruppe** (z.B. U6–U8, U9–U11, U12+)
- **Kategorie** (Technik, Taktik, Koordination, Spielform, Aufwärmen, etc.)
- **Teilnehmerzahl**
- **Material**
- **Beschreibung** & **Ablauf**
- **Coaching-Hinweise**

### Schritt 4 – Index aktualisieren
Nach jeder Verarbeitung wird `metadata/index.md` automatisch aktualisiert.

---

## Qualitätskriterien für Quellen

Bevorzuge Kanäle / Videos mit folgenden Merkmalen:
- Lizenzierte Trainer oder DFB/UEFA-zertifizierte Coaches
- Klare Sprache (Deutsch bevorzugt, Englisch sekundär)
- Altersangabe und methodischer Aufbau erkennbar
- Transkripte / Untertitel verfügbar

---

## Nächste Schritte

1. [ ] YouTube-Kanäle in `channels/` eintragen (s. `fetch_channel.py`)
2. [ ] Skript ausführen: `python fetch_channel.py --channel [URL]`
3. [ ] Transkripte extrahieren: `python extract_transcripts.py`
4. [ ] Übungen strukturieren lassen (via Claude)
