# Setup-Anleitung: YouTube-Daten lokal abrufen

Das Skript `fetch_channel.py` muss **einmalig lokal auf deinem Rechner** ausgeführt werden, da YouTube aus der Cloud-Umgebung nicht erreichbar ist.

---

## Schritt 1 – Voraussetzungen installieren

Öffne ein Terminal (macOS: `Terminal.app` / Windows: `cmd` oder PowerShell) und führe aus:

```bash
pip install yt-dlp youtube-transcript-api
```

> Falls `pip` nicht gefunden wird: `pip3 install yt-dlp youtube-transcript-api`

---

## Schritt 2 – In den input-Ordner wechseln

```bash
cd "/Pfad/zu/Kids Fussball/input"
```

Beispiel macOS:
```bash
cd ~/Documents/Kids\ Fussball/input
```

---

## Schritt 3 – Kanäle abrufen

Führe für jeden Kanal einmal aus:

```bash
python fetch_channel.py --channel https://www.youtube.com/@Mfsfussballtraining
python fetch_channel.py --channel https://www.youtube.com/@trainerkick
python fetch_channel.py --channel https://www.youtube.com/@360Football
python fetch_channel.py --channel https://www.youtube.com/@Soccer_Hartenstein
```

> Optional: `--max 30` um nur die letzten 30 Videos zu holen (Standard: 50)

Das Skript speichert automatisch:
- `channels/<kanal-id>/video_list.md` – alle Videos des Kanals
- `transcripts/<video-id>.md` – Transkript für jedes Video
- `metadata/index.md` – aktualisierter Gesamtindex

---

## Schritt 4 – Ergebnisse zurückbringen

Sobald die Dateien in `transcripts/` und `channels/` liegen, kann Claude:
- Die Transkripte analysieren
- Übungen strukturiert extrahieren und in `exercises/` speichern
- Die Wissensdatenbank aufbauen

**Einfach die neuen Dateien bestätigen und Claude bescheid geben: „Transkripte sind da!"**

---

## Troubleshooting

| Problem | Lösung |
|---------|--------|
| `pip: command not found` | `python3 -m pip install ...` verwenden |
| `yt-dlp: command not found` nach Install | Terminal neu starten oder `python3 -m yt_dlp ...` |
| Kein Transkript verfügbar | Video hat keine Untertitel (wird als ❌ im Index markiert) |
| Rate Limit / Captcha | Kurze Pause einlegen und erneut versuchen |

---

## Kanäle (bereits angelegt)

| Kanal | URL | Status |
|-------|-----|--------|
| MFS Fussballtraining | https://www.youtube.com/@Mfsfussballtraining | ⏳ ausstehend |
| TrainerKick | https://www.youtube.com/@trainerkick | ⏳ ausstehend |
| 360Football | https://www.youtube.com/@360Football | ⏳ ausstehend |
| Soccer Hartenstein | https://www.youtube.com/@Soccer_Hartenstein | ⏳ ausstehend |
