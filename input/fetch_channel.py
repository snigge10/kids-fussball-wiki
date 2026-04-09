#!/usr/bin/env python3
"""
fetch_channel.py – YouTube-Kanal-Daten & Transkripte für Kinder Fussball Training

Verwendung:
    python fetch_channel.py --channel https://www.youtube.com/@KanalName
    python fetch_channel.py --channel https://www.youtube.com/@KanalName --max 20
    python fetch_channel.py --video https://www.youtube.com/watch?v=VIDEO_ID

Voraussetzungen:
    pip install yt-dlp

Ausgabe:
    - channels/<kanal-name>/channel_info.md
    - channels/<kanal-name>/video_list.md
    - transcripts/<video-id>.md
    - metadata/index.md  (wird aktualisiert)
    - metadata/processing_log.md
"""

import argparse
import os
import re
import sys
import tempfile
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
CHANNELS_DIR  = BASE_DIR / "channels"
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
EXERCISES_DIR = BASE_DIR / "exercises"
METADATA_DIR  = BASE_DIR / "metadata"

def ensure_dirs():
    for d in [CHANNELS_DIR, TRANSCRIPTS_DIR, EXERCISES_DIR, METADATA_DIR]:
        d.mkdir(parents=True, exist_ok=True)

def sanitize(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|@]', "_", name).strip("_").strip()

def videos_url(channel_url: str) -> str:
    """Hängt /videos an Channel-URL, damit yt-dlp echte Videos liefert."""
    url = channel_url.rstrip("/")
    if not url.endswith("/videos"):
        url += "/videos"
    return url

# ─────────────────────────────────────────────
# 1. Video-Liste holen
# ─────────────────────────────────────────────
def fetch_channel_info(channel_url: str, max_videos: int = 50):
    try:
        import yt_dlp
    except ImportError:
        print("❌ yt-dlp nicht installiert. Bitte: pip install yt-dlp")
        sys.exit(1)

    url = videos_url(channel_url)
    print(f"📡 Lade Video-Liste: {url}")

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "playlist_items": f"1:{max_videos}",
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    # Kanal-Name ermitteln
    channel_name = info.get("channel") or info.get("uploader") or info.get("title") or "Unbekannt"
    if channel_name == "null" or not channel_name:
        channel_name = channel_url.split("@")[-1].split("/")[0]

    entries = [e for e in (info.get("entries") or []) if e.get("id") and not e["id"].startswith("UC")]
    folder_name = sanitize(channel_name)
    channel_dir = CHANNELS_DIR / folder_name
    channel_dir.mkdir(parents=True, exist_ok=True)

    # channel_info.md
    with open(channel_dir / "channel_info.md", "w", encoding="utf-8") as f:
        f.write(f"# Kanal: {channel_name}\n\n")
        f.write(f"**URL:** {channel_url}\n\n")
        f.write(f"**Abgerufen am:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
        f.write(f"**Anzahl Videos abgerufen:** {len(entries)}\n")

    # video_list.md
    with open(channel_dir / "video_list.md", "w", encoding="utf-8") as f:
        f.write(f"# Video-Liste: {channel_name}\n\n")
        f.write("| Nr | Video-ID | Titel | URL |\n")
        f.write("|----|----------|-------|-----|\n")
        for i, e in enumerate(entries, 1):
            vid_id = e.get("id", "")
            title  = (e.get("title") or "").replace("|", "-")
            yt_url = f"https://www.youtube.com/watch?v={vid_id}"
            f.write(f"| {i} | {vid_id} | {title} | {yt_url} |\n")

    print(f"✅ {channel_name}: {len(entries)} Videos → channels/{folder_name}/")
    return folder_name, channel_name, entries

# ─────────────────────────────────────────────
# 2. Transkript via yt-dlp (zuverlässiger als youtube-transcript-api)
# ─────────────────────────────────────────────
def fetch_transcript(video_id: str, title: str = "", delay: float = 2.0) -> bool:
    try:
        import yt_dlp
        import time
    except ImportError:
        return False

    out_path = TRANSCRIPTS_DIR / f"{video_id}.md"
    if out_path.exists():
        print(f"  ⏭️  bereits vorhanden: {video_id}")
        return True

    video_url = f"https://www.youtube.com/watch?v={video_id}"

    def try_download(langs: list, tmpdir: str) -> list:
        """Versucht Untertitel für eine Sprachliste herunterzuladen."""
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": langs,
            "subtitlesformat": "vtt",
            "outtmpl": os.path.join(tmpdir, "%(id)s.%(ext)s"),
            # Ratenlimit-Schutz
            "sleep_interval": 1,
            "max_sleep_interval": 3,
            "retries": 3,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except Exception:
            pass
        return list(Path(tmpdir).glob(f"{video_id}*.vtt"))

    with tempfile.TemporaryDirectory() as tmpdir:
        # 1. Versuch: nur Deutsch
        vtt_files = try_download(["de"], tmpdir)

        # 2. Versuch: nur Englisch (falls kein Deutsch vorhanden)
        if not vtt_files:
            time.sleep(delay)
            vtt_files = try_download(["en"], tmpdir)

        if not vtt_files:
            print(f"  ⚠️  Keine Untertitel verfügbar: {video_id}")
            return False

        # Deutschen bevorzugen, falls beide vorhanden
        de_files = [f for f in vtt_files if ".de." in f.name]
        vtt_path = de_files[0] if de_files else vtt_files[0]
        lang = "de" if ".de." in vtt_path.name else "en"

        # VTT → sauberen Text konvertieren
        raw = vtt_path.read_text(encoding="utf-8", errors="ignore")
        lines = []
        seen = set()
        for line in raw.splitlines():
            line = line.strip()
            if not line or line.startswith("WEBVTT") or line.startswith("NOTE") or "-->" in line:
                continue
            # HTML-Tags entfernen
            line = re.sub(r"<[^>]+>", "", line)
            line = re.sub(r"&amp;", "&", line)
            line = re.sub(r"&nbsp;", " ", line)
            if line and line not in seen:
                seen.add(line)
                lines.append(line)

        if not lines:
            print(f"  ⚠️  Transkript leer nach Bereinigung: {video_id}")
            return False

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# Transkript: {title or video_id}\n\n")
            f.write(f"**Video-ID:** {video_id}\n")
            f.write(f"**URL:** {video_url}\n")
            f.write(f"**Sprache:** {lang}\n")
            f.write(f"**Extrahiert am:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write("---\n\n")
            f.write("## Inhalt\n\n")
            f.write("\n".join(lines))
            f.write("\n")

        print(f"  ✅ Transkript gespeichert: {video_id}.md ({len(lines)} Zeilen, {lang})")
        return True

# ─────────────────────────────────────────────
# 3. Index aktualisieren
# ─────────────────────────────────────────────
def update_index(video_id: str, title: str, channel_name: str, has_transcript: bool):
    index_path = METADATA_DIR / "index.md"
    date = datetime.now().strftime("%Y-%m-%d")
    url  = f"https://www.youtube.com/watch?v={video_id}"
    t_status = "✅" if has_transcript else "❌"
    new_row = f"| [{video_id}]({url}) | {title[:60]} | {channel_name} | {date} | – | {t_status} | ❌ |\n"

    if index_path.exists():
        content = index_path.read_text(encoding="utf-8")
        # Platzhalter entfernen
        content = content.replace(
            "| –        | –     | –     | –     | –            | –          | –                  |\n", "")
        # Kein Duplikat einfügen
        if video_id not in content:
            content += new_row
        index_path.write_text(content, encoding="utf-8")
    else:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write("# Index – Verarbeitete Videos\n\n")
            f.write("| Video-ID | Titel | Kanal | Datum | Altersgruppe | Transkript | Übungen extrahiert |\n")
            f.write("|----------|-------|-------|-------|--------------|------------|--------------------|\\n")
            f.write(new_row)

def log(msg: str):
    log_path = METADATA_DIR / "processing_log.md"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')} – {msg}\n")

# ─────────────────────────────────────────────
# main
# ─────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="YouTube Kinder Fussball – Daten sammeln")
    parser.add_argument("--channel", help="URL eines YouTube-Kanals")
    parser.add_argument("--video",   help="URL eines einzelnen Videos")
    parser.add_argument("--max",     type=int,   default=50,  help="Max. Videos pro Kanal (Standard: 50)")
    parser.add_argument("--delay",   type=float, default=2.0, help="Pause in Sekunden zwischen Videos (Standard: 2.0)")
    parser.add_argument("--list-only", action="store_true",   help="Nur Video-Liste, keine Transkripte")
    args = parser.parse_args()

    ensure_dirs()

    if args.channel:
        folder_name, channel_name, entries = fetch_channel_info(args.channel, args.max)
        log(f"Kanal geladen: {channel_name} ({len(entries)} Videos)")

        if args.list_only:
            print(f"\n✅ Video-Liste gespeichert. Transkripte übersprungen (--list-only).")
            return

        print(f"\n📄 Starte Transkript-Extraktion ({len(entries)} Videos, Pause: {args.delay}s) …\n")
        ok_count = 0
        for entry in entries:
            vid_id = entry.get("id", "")
            title  = entry.get("title", "")
            if not vid_id:
                continue
            ok = fetch_transcript(vid_id, title, delay=args.delay)
            update_index(vid_id, title, channel_name, ok)
            if ok:
                ok_count += 1

        log(f"Transkripte: {ok_count}/{len(entries)} erfolgreich")
        print(f"\n✅ Fertig! {ok_count}/{len(entries)} Transkripte gespeichert.")

    elif args.video:
        match = re.search(r"[?&]v=([a-zA-Z0-9_-]+)", args.video)
        if not match:
            print("❌ Konnte Video-ID nicht extrahieren.")
            sys.exit(1)
        vid_id = match.group(1)
        ok = fetch_transcript(vid_id)
        update_index(vid_id, vid_id, "manuell", ok)

    else:
        parser.print_help()
        print("\n💡 Beispiele:")
        print("  python fetch_channel.py --channel https://www.youtube.com/@trainerkick")
        print("  python fetch_channel.py --channel https://www.youtube.com/@trainerkick --list-only")
        print("  python fetch_channel.py --video https://www.youtube.com/watch?v=ABC123")

if __name__ == "__main__":
    main()
