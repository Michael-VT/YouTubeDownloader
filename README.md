English | [Русский](README.RU.md) | [Українська](README.UK.md) | [Português](README.PT.md) | [Deutsch](README.DE.md) | [Français](README.FR.md)

# 🎬 YouTube Downloader

Downloads **video (mp4)**, **audio (mp3)** and **text transcripts** (from subtitles) from YouTube — any of them, or all at once. Two interfaces:

- **CLI** — `download.py`, a console tool written in Python;
- **Web UI** — `web_server.py` (Flask) + `web_ui.html` (JS in the browser): progress bar, download log, file list with download links.

![YouTube Downloader](Screeshot/YouTubDownloader.png)

Interface languages: **English, Русский, Українська, Português, Deutsch, Français**.

License: **MIT** — free to use without restrictions (see [LICENSE](LICENSE)).

## Features

- 🎥 Video at maximum quality (1080p / 1440p / 4K via DASH streams merged with ffmpeg), medium or low
- 🎧 Audio only, converted to mp3 (192 kbps) — great for listening on the go
- 📄 Text transcript from subtitles (cleaned of timecodes and markup) saved next to the media file
- 🌍 Audio track and subtitle language selection (`--lang ru`, `en`, …); Russian track gets priority on multi-language videos
- 🔁 Duplicate protection: already downloaded videos are skipped (an ID-based log is kept)
- 📝 Download log in two formats: `download_log.txt` and `download_log.html`
- 🖥️ Web UI: video info before downloading, live progress, history, file downloads straight from the browser
- 🌐 Interface language switchable in both CLI and Web UI (6 languages, auto-detected by default)

## Repository structure

```
├── download.py            # CLI downloader (core logic)
├── web_server.py          # Web server (Flask API + serves the UI)
├── web_ui.html            # Web interface (HTML/JS)
├── i18n.py                # Interface language engine
├── locales/               # Translations: en, ru, uk, pt, de, fr
├── requirements.txt       # Python dependencies
├── Screeshot/             # Screenshot used in the READMEs
├── .github/workflows/     # GitHub Actions: download without a local install
├── .devcontainer/         # GitHub Codespaces setup
└── legacy/                # Old script versions (development history)
```

Downloaded files go to `downloads/`, the log lives in the project root. Both paths (and personal files) are excluded from git via `.gitignore`.

## Installation (local)

### 1. Requirements

- **Python 3.10+** (tested on 3.12)
- **ffmpeg** — required for merging DASH streams (quality above 720p) and mp3 conversion. Without it the program still works, but video is limited to 720p (progressive) and audio stays in its original format (m4a)

### 2. Installing ffmpeg

| OS | Command |
|---|---|
| macOS | `brew install ffmpeg` |
| Ubuntu / Debian | `sudo apt install ffmpeg` |
| Windows | `winget install Gyan.FFmpeg` (or `choco install ffmpeg`), then restart the terminal |

Verify: `ffmpeg -version`

### 3. Cloning and dependencies

```bash
git clone https://github.com/YOUR_LOGIN/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Usage: CLI

### Interactive mode

```bash
python download.py
```

Asks step by step: URL → quality → language → whether to save mp3.

### With arguments

```bash
python download.py "https://youtu.be/XXXX" max          # best-quality video + transcript
python download.py "https://youtu.be/XXXX" audio        # mp3 only + transcript
python download.py "https://youtu.be/XXXX" medium --lang en
python download.py "https://youtu.be/XXXX" max --mp3 -o video   # + mp3, folder video/
python download.py "https://youtu.be/XXXX" max --ui-lang de     # German interface
```

| Argument | Meaning |
|---|---|
| `url` | video URL (without it — interactive mode) |
| `quality` | `max` / `medium` / `low` / `audio` |
| `--lang`, `-l` | audio and transcript language (default: `ru`) |
| `--mp3` | additionally save an mp3 track next to the mp4 |
| `-o`, `--output` | output folder (default: `downloads`) |
| `--ui-lang`, `-u` | interface language: `en`/`ru`/`uk`/`pt`/`de`/`fr` |

The interface language is auto-detected from your system locale (`LANG`/`LC_ALL`); use `--ui-lang` to override, or set the `YTD_LANG` environment variable.

Full help: `python download.py --help`

Result in `downloads/`:

```
Video title.mp4                  # video (or .mp3 in audio mode)
Video title.mp3                  # with --mp3 or quality=audio
Video title.transcript.txt       # transcript from subtitles
```

## Usage: Web UI

```bash
python web_server.py
```

Open **http://127.0.0.1:5000** in your browser:

1. Paste a link → **“Get info”**: thumbnail, author, duration, available resolutions, subtitle availability, status (“new” / “already downloaded”)
2. Pick quality and language → **“Download”**: live progress bar and console log
3. Below — the list of ready files (download right from the browser) and the full download log

The interface language is chosen with the 🌐 selector in the top-right corner; the choice is remembered in the browser. The download log/console output follows the selected language too.

Host and port can be changed with environment variables:

```bash
HOST=0.0.0.0 PORT=8080 python web_server.py
```

## Running directly on GitHub

A static site (GitHub Pages) won't work here — a Python backend is required. Two working options instead.

### Option 1: GitHub Actions (no local install needed)

The repository includes a manually triggered workflow `.github/workflows/download.yml`:

1. Open the **Actions** tab → **Download YouTube video** → **Run workflow**
2. Provide the URL, quality (`max`/`medium`/`low`/`audio`), content language, interface language, and whether mp3 is needed
3. Wait for completion → the run summary shows **artifact `youtube-download`** — download the zip with your files

Nothing is stored in the repository: the run delivers only the media file itself (mp4/mp3) as a short-lived artifact (1 day). Download the zip from the run summary; for transcripts and logs, run the tool locally.

⚠️ **Limitations**: artifacts are stored for a limited time (1 day here), size is capped, and YouTube often blocks datacenter IPs (the “Sign in to confirm you're not a bot” error). For regular use, run locally.

### Option 2: GitHub Codespaces (full web UI in the cloud)

1. **Code** button → **Codespaces** tab → **Create codespace on master**
2. The container is configured via `.devcontainer/devcontainer.json`: Python 3.12, ffmpeg, dependencies — installed automatically
3. In the terminal: `python web_server.py` — port 5000 is forwarded automatically and the browser opens by itself

For reference: the free Codespaces quota for personal GitHub accounts is 120 core-hours per month — enough for occasional use.

## Download log

Every download appends an entry:

- `download_log.txt` — machine-readable log (used to detect “already downloaded”);
- `download_log.html` — a human-friendly table with links.

To re-download a video, remove its ID from `download_log.txt` (and the file from `downloads/`).

## Troubleshooting

| Problem | Solution |
|---|---|
| Video downloads at 720p max | ffmpeg not found → DASH merging unavailable. Install ffmpeg and check `ffmpeg -version` |
| “Sign in to confirm you're not a bot” | YouTube blocks your IP (often on VPNs/datacenters). Try another network or run locally |
| No mp3, a `.m4a` remains | ffmpeg is not installed — conversion impossible, the original audio stream was kept |
| No transcript | The video has no subtitles. YouTube auto-generated captions are also supported when available |
| “Address already in use” when starting the Web UI | On macOS port 5000 is often taken by AirPlay (Control Center) — run on another port: `PORT=8080 python web_server.py` |
| pytubefix breaks after a YouTube update | `pip install -U pytubefix` — the library is actively patched as YouTube changes |

## License

[MIT](LICENSE) — free use, copying, modification and distribution, including commercial use.

⚠️ **Legal note**: this program is intended for downloading content you have the rights to (your own content, openly licensed content, or downloading permitted in your jurisdiction). Respect YouTube's Terms of Service and copyright.
