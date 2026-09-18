[English](README.md) | [Русский](README.RU.md) | [Українська](README.UK.md) | [Português](README.PT.md) | Deutsch | [Français](README.FR.md)

# 🎬 YouTube Downloader

Lädt **Videos (mp4)**, **Audio (mp3)** und **Texttranskripte** (aus Untertiteln) von YouTube herunter — jedes einzeln oder alle auf einmal. Zwei Oberflächen:

- **CLI** — `download.py`, ein Konsolenwerkzeug in Python;
- **Web-UI** — `web_server.py` (Flask) + `web_ui.html` (JS im Browser): Fortschrittsbalken, Download-Protokoll, Dateiliste mit Download-Links.

![YouTube Downloader](Screeshot/YouTubDownloader.png)

Sprachen der Oberfläche: **English, Русский, Українська, Português, Deutsch, Français**.

Lizenz: **MIT** — kostenlose Nutzung ohne Einschränkungen (siehe [LICENSE](LICENSE)).

## Funktionen

- 🎥 Video in maximaler Qualität (1080p / 1440p / 4K über DASH-Streams, mit ffmpeg zusammengeführt), mittel oder niedrig
- 🎧 Nur Audio, konvertiert zu mp3 (192 kbps) — ideal zum Hören unterwegs
- 📄 Texttranskript aus Untertiteln (bereinigt von Zeitmarken und Markup), gespeichert neben der Mediendatei
- 🌍 Auswahl der Audio- und Untertitelsprache (`--lang ru`, `en`, …); bei mehrsprachigen Videos hat die russische Spur Vorrang
- 🔁 Duplikatschutz: bereits heruntergeladene Videos werden übersprungen (ID-basiertes Protokoll)
- 📝 Download-Protokoll in zwei Formaten: `download_log.txt` und `download_log.html`
- 🖥️ Web-UI: Videoinformationen vor dem Download, Live-Fortschritt, Verlauf, Datei-Downloads direkt aus dem Browser
- 🌐 Sprache der Oberfläche in CLI und Web-UI umschaltbar (6 Sprachen, standardmäßig automatisch erkannt)

## Repository-Struktur

```
├── download.py            # CLI-Downloader (Kernlogik)
├── web_server.py          # Webserver (Flask-API + stellt die UI bereit)
├── web_ui.html            # Weboberfläche (HTML/JS)
├── i18n.py                # Sprach-Engine der Oberfläche
├── locales/               # Übersetzungen: en, ru, uk, pt, de, fr
├── requirements.txt       # Python-Abhängigkeiten
├── Screeshot/             # Screenshot für die READMEs
├── .github/workflows/     # GitHub Actions: Download ohne lokale Installation
├── .devcontainer/         # GitHub-Codespaces-Setup
└── legacy/                # Alte Skriptversionen (Entwicklungsgeschichte)
```

Heruntergeladene Dateien landen in `downloads/`, das Protokoll liegt im Projektstamm. Beide Pfade (und persönliche Dateien) sind über `.gitignore` von git ausgeschlossen.

## Installation (lokal)

### 1. Voraussetzungen

- **Python 3.10+** (getestet mit 3.12)
- **ffmpeg** — erforderlich für das Zusammenführen von DASH-Streams (Qualität über 720p) und die mp3-Konvertierung. Ohne ffmpeg funktioniert das Programm weiterhin, aber Video ist auf 720p (progressiv) begrenzt und Audio bleibt im Originalformat (m4a)

### 2. ffmpeg installieren

| OS | Befehl |
|---|---|
| macOS | `brew install ffmpeg` |
| Ubuntu / Debian | `sudo apt install ffmpeg` |
| Windows | `winget install Gyan.FFmpeg` (oder `choco install ffmpeg`), danach das Terminal neu starten |

Prüfen: `ffmpeg -version`

### 3. Klonen und Abhängigkeiten

```bash
git clone https://github.com/YOUR_LOGIN/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Verwendung: CLI

### Interaktiver Modus

```bash
python download.py
```

Fragt Schritt für Schritt ab: URL → Qualität → Sprache → ob mp3 gespeichert werden soll.

### Mit Argumenten

```bash
python download.py "https://youtu.be/XXXX" max          # Video in bester Qualität + Transkript
python download.py "https://youtu.be/XXXX" audio        # nur mp3 + Transkript
python download.py "https://youtu.be/XXXX" medium --lang en
python download.py "https://youtu.be/XXXX" max --mp3 -o video   # + mp3, Ordner video/
python download.py "https://youtu.be/XXXX" max --ui-lang de     # deutsche Oberfläche
```

| Argument | Bedeutung |
|---|---|
| `url` | Video-URL (ohne sie — interaktiver Modus) |
| `quality` | `max` / `medium` / `low` / `audio` |
| `--lang`, `-l` | Audio- und Transkriptsprache (Standard: `ru`) |
| `--mp3` | zusätzlich eine mp3-Spur neben dem mp4 speichern |
| `-o`, `--output` | Ausgabeordner (Standard: `downloads`) |
| `--ui-lang`, `-u` | Sprache der Oberfläche: `en`/`ru`/`uk`/`pt`/`de`/`fr` |

Die Sprache der Oberfläche wird automatisch anhand der Systemlocale (`LANG`/`LC_ALL`) erkannt; mit `--ui-lang` können Sie sie überschreiben, alternativ die Umgebungsvariable `YTD_LANG` setzen.

Vollständige Hilfe: `python download.py --help`

Ergebnis in `downloads/`:

```
Videotitel.mp4                  # Video (bzw. .mp3 im Audio-Modus)
Videotitel.mp3                  # mit --mp3 oder quality=audio
Videotitel.transcript.txt       # Transkript aus Untertiteln
```

## Verwendung: Web-UI

```bash
python web_server.py
```

Öffnen Sie **http://127.0.0.1:5000** im Browser:

1. Link einfügen → **„Infos abrufen“**: Vorschaubild, Autor, Dauer, verfügbare Auflösungen, Untertitel-Verfügbarkeit, Status („neu“ / „bereits heruntergeladen“)
2. Qualität und Sprache wählen → **„Herunterladen“**: Live-Fortschrittsbalken und Konsolen-Protokoll
3. Darunter — die Liste der fertigen Dateien (direkt aus dem Browser herunterladbar) und das vollständige Download-Protokoll

Die Sprache der Oberfläche wird mit dem 🌐-Auswahlfeld in der oberen rechten Ecke gewählt; die Auswahl wird im Browser gemerkt. Das Download-Protokoll bzw. die Konsolenausgabe folgt ebenfalls der gewählten Sprache.

Host und Port lassen sich über Umgebungsvariablen ändern:

```bash
HOST=0.0.0.0 PORT=8080 python web_server.py
```

## Direkt auf GitHub ausführen

Eine statische Seite (GitHub Pages) funktioniert hier nicht — ein Python-Backend ist erforderlich. Zwei funktionierende Alternativen.

### Option 1: GitHub Actions (ohne lokale Installation)

Das Repository enthält einen manuell auslösbaren Workflow `.github/workflows/download.yml`:

1. Tab **Actions** öffnen → **Download YouTube video** → **Run workflow**
2. URL, Qualität (`max`/`medium`/`low`/`audio`), Inhaltssprache, Sprache der Oberfläche und ob mp3 benötigt wird angeben
3. Auf den Abschluss warten → in der Laufzeit-Zusammenfassung erscheint das **Artefakt `youtube-download`** — Laden Sie das Zip mit Ihren Dateien herunter

Im Repository wird nichts gespeichert: Der Lauf liefert nur die Mediendatei selbst (mp4/mp3) als kurzlebiges Artefakt (1 Tag). Laden Sie das Zip aus der Laufzeit-Zusammenfassung; für Transkripte und Logs führen Sie das Tool lokal aus.

⚠️ **Einschränkungen**: Artefakte werden nur begrenzte Zeit gespeichert (hier 1 Tag), die Größe ist begrenzt, und YouTube blockiert häufig Rechenzentren-IPs (Fehler „Sign in to confirm you're not a bot“). Für regelmäßige Nutzung lokal ausführen.

### Option 2: GitHub Codespaces (vollständige Web-UI in der Cloud)

1. Schaltfläche **Code** → Tab **Codespaces** → **Create codespace on master**
2. Der Container ist über `.devcontainer/devcontainer.json` konfiguriert: Python 3.12, ffmpeg, Abhängigkeiten — alles wird automatisch installiert
3. Im Terminal: `python web_server.py` — Port 5000 wird automatisch weitergeleitet und der Browser öffnet sich von selbst

Zur Orientierung: Das kostenlose Codespaces-Kontingent für persönliche GitHub-Konten beträgt 120 Core-Stunden pro Monat — genug für gelegentliche Nutzung.

## Download-Protokoll

Jeder Download hängt einen Eintrag an:

- `download_log.txt` — maschinenlesbares Protokoll (dient der Erkennung von „bereits heruntergeladen“);
- `download_log.html` — eine gut lesbare Tabelle mit Links.

Um ein Video erneut herunterzuladen, entfernen Sie seine ID aus `download_log.txt` (und die Datei aus `downloads/`).

## Fehlerbehebung

| Problem | Lösung |
|---|---|
| Video wird maximal mit 720p heruntergeladen | ffmpeg nicht gefunden → DASH-Zusammenführung nicht verfügbar. ffmpeg installieren und `ffmpeg -version` prüfen |
| „Sign in to confirm you're not a bot“ | YouTube blockiert Ihre IP (häufig bei VPNs/Rechenzentren). Anderes Netzwerk versuchen oder lokal ausführen |
| Kein mp3, eine `.m4a` bleibt übrig | ffmpeg ist nicht installiert — eine Konvertierung ist unmöglich, der ursprüngliche Audiostream wurde behalten |
| Kein Transkript | Das Video hat keine Untertitel. Automatisch von YouTube erzeugte Untertitel werden ebenfalls unterstützt, sofern vorhanden |
| „Address already in use“ beim Starten der Web-UI | Unter macOS ist Port 5000 oft durch AirPlay (Kontrollzentrum) belegt — anderen Port verwenden: `PORT=8080 python web_server.py` |
| pytubefix funktioniert nach einem YouTube-Update nicht mehr | `pip install -U pytubefix` — die Bibliothek wird aktiv gepatcht, wenn sich YouTube ändert |

## Lizenz

[MIT](LICENSE) — freie Nutzung, Vervielfältigung, Bearbeitung und Verbreitung, auch kommerziell.

⚠️ **Rechtlicher Hinweis**: Dieses Programm ist für das Herunterladen von Inhalten gedacht, an denen Sie Rechte haben (eigene Inhalte, offen lizenzierte Inhalte oder in Ihrer Rechtsordnung erlaubtes Herunterladen). Beachten Sie die Nutzungsbedingungen von YouTube und das Urheberrecht.
