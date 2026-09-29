# Changelog

## v3.0 — 2026-09-29

### Duplicate protection per content type

Previously, downloading a video once blocked every other download of it. Now each
type and quality is tracked separately:

- **video** — per resolution: a video saved at 480p can still be fetched at
  1080p/4K (`max`), and vice versa;
- **audio** — per mp3 bitrate;
- **text** — transcript-only downloads;
- attachments of earlier entries (a transcript or mp3 saved alongside a video)
  count as downloaded, so nothing is fetched twice;
- entries whose file was deleted from `downloads/` are re-downloadable;
- the console and the web UI now list exactly what is already downloaded
  for a video (e.g. `video 480p • mp3 192k • transcript`).

### Text-only mode

New `text` quality: downloads just the transcript (subtitles cleaned of
timecodes and markup), without any media.

### mp3 bitrate selection

`--abitrate 128k|192k|320k` (default 192k) for the `audio` mode and `--mp3`.
Non-default bitrates get a ` [320k]` filename suffix so files with different
bitrates never overwrite each other.

### Waiting queue for unavailable videos

- a failed metadata fetch (private, removed, region-locked, bot-check)
  automatically queues the URL in `pending_queue.json` together with its
  quality/language/bitrate and the failure reason;
- the queue is re-checked automatically on every run;
- commands: `--check-queue`, `--watch [MIN]` (keep watching the queue, default
  15 minutes), `--queue-list`, `--queue-remove URL`;
- when a queued video becomes available it is downloaded with the same
  parameters, with a clear notification.

### Web UI

- “Text only” quality option and an mp3 bitrate selector;
- waiting-queue card with a “Check now” button;
- the info badge lists exactly what is already downloaded;
- failed downloads are marked as an error instead of “done”.

### Fixes

- default web-server port changed **5000 → 8080**: on macOS, AirPlay Receiver
  (Control Center) shares port 5000 and randomly answers the browser with
  `403 Access denied`;
- `.DS_Store` and `_tmp_*` files are no longer shown in the downloaded-files list;
- the file-download route's path check was tightened (`out_dir + os.sep`).

## v2.0 — 2026-09-29

Pinned working version (tag `v2.0`, archived as `legacy/download-v2.py`):
video/audio/transcript downloads, per-video duplicate protection, web UI,
6 interface languages.
