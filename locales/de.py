"""Deutsche UI-Texte."""

STRINGS = {
    # ---------- CLI: argparse ----------
    "app_desc": "Videos, Audio und Transkripte von YouTube herunterladen.",
    "help_url": "YouTube-Video-URL",
    "help_quality": "Qualität: max / medium / low / audio",
    "help_lang": "Audio-/Transkriptsprache (Standard: {default})",
    "help_mp3": "Zusätzlich eine mp3-Spur speichern",
    "help_output": "Ausgabeordner (Standard: downloads)",
    "help_ui_lang": "Sprache der Oberfläche: en/ru/uk/pt/de/fr (Standard: automatisch)",

    # ---------- CLI: interactive ----------
    "choose_quality": "Qualität wählen:",
    "q_max": "  1 — maximal (1080p+ via DASH)",
    "q_medium": "  2 — mittel",
    "q_low": "  3 — niedrig",
    "q_audio": "  4 — nur Audio (mp3)",
    "prompt_quality": "Nummer (1/2/3/4) [1]: ",
    "prompt_url": "🔗 YouTube-URL: ",
    "prompt_lang": "Audio-/Transkriptsprache [{default}]: ",
    "prompt_mp3": "Zusätzlich eine mp3-Spur speichern? (y/N): ",

    # ---------- CLI: extended help ----------
    "extended_help": """YouTube Downloader — erweiterte Hilfe

QUALITÄTSMODI:
  max     — beste verfügbare Qualität (1080p, 1440p, 4K via DASH)
  medium  — mittel
  low     — niedrigste (144p–360p)
  audio   — nur Audio als mp3 (ideal zum Hören unterwegs)

ZUSÄTZLICHE OPTIONEN:
  --mp3            zusätzlich eine mp3-Spur neben dem mp4 speichern
  --lang ru|en|…   Audio- und Transkriptsprache (Standard: ru)
  --ui-lang LL     Sprache der Oberfläche: en/ru/uk/pt/de/fr (Standard: automatisch)
  -o DIR           Ausgabeordner (Standard: downloads)

BEISPIELE:
  python download.py "https://youtu.be/XXXX" max
  python download.py "https://youtu.be/XXXX" audio
  python download.py "https://youtu.be/XXXX" medium --lang en
  python download.py "https://youtu.be/XXXX" max --mp3 -o video
  python download.py "https://youtu.be/XXXX" max --ui-lang de

OHNE ARGUMENTE läuft das Tool im interaktiven Modus und fragt Schritt für Schritt ab.""",

    # ---------- Fetch / info ----------
    "info_log_entries": "ℹ️  Das Protokoll enthält bereits {count} Einträge.",
    "err_get_video": "❌ Fehler beim Abrufen des Videos: {error}",
    "warn_already_downloaded": "⚠️  Wurde bereits früher heruntergeladen. Wird übersprungen.",
    "already_id": "   ID: {id}",
    "already_title": "   Titel: {title}",
    "video_title": "🎬 Titel: {title}",
    "video_author": "👤 Autor: {author}",
    "video_duration": "⏱  Dauer: {duration}",
    "video_id": "🆔 ID: {id}",

    # ---------- Streams ----------
    "err_no_video_stream": "❌ Kein passender Videostream gefunden",
    "err_no_audio_stream": "❌ Audiospur konnte nicht ausgewählt werden",
    "audio_tracks_available": "🎧 Verfügbare Audiospuren:",
    "audio_track_line": "   • {track} | {abr} | itag={itag} | ext={ext}{default}",
    "audio_selected": "✅ Gewählte Audiospur: {track} ({abr})",
    "audio_using_default": "ℹ️  Keine Spur in der angeforderten Sprache, es wird die Standardspur verwendet ({abr})",
    "audio_using_best": "ℹ️  Es wird die Spur mit der höchsten Qualität verwendet ({abr})",
    "audio_header": "🎧 Audio: {name} ({abr})",
    "video_stream_info": "🎞  Video: {res} ({mode})",
    "merge_label": "🔧 Merge: {value}",
    "word_yes": "ja",
    "word_no": "nein",
    "audio_lang_embedded": "eingebettet",

    # ---------- ffmpeg ----------
    "warn_no_ffmpeg_dash": "⚠️  ffmpeg nicht gefunden — DASH (1080p+) ist nicht verfügbar.",
    "warn_fallback_progressive": "   Rückfall auf progressiv (maximal 720p).",
    "err_no_progressive": "❌ Progressiver Stream nicht verfügbar. Bitte ffmpeg installieren.",
    "dl_video_stream": "⬇️  Videostream wird heruntergeladen...",
    "dl_audio_stream": "⬇️  Audiostream wird heruntergeladen...",
    "downloaded": "⬇️  Heruntergeladen: {path}",
    "err_tmp_corrupt": "❌ Temporäre Datei beschädigt oder leer: {path}",
    "merging": "🔗 Video und Audio werden zusammengeführt...",
    "merge_cmd": "🔗 ffmpeg-Merge: {cmd}",
    "err_ffmpeg_code": "❌ ffmpeg wurde mit Code {code} beendet",
    "stderr_tail": "   stderr: {stderr}",
    "err_output_missing": "❌ Ausgabedatei fehlt oder ist verdächtig klein.",
    "err_no_audio_track_out": "❌ Keine Audiospur in der Ausgabedatei gefunden.",
    "warn_merge_failed": "⚠️  Merge fehlgeschlagen. Fallback wird versucht: progressiv.",
    "ok_saved_fallback": "✅ Gespeichert (Fallback): {path}",

    # ---------- mp3 ----------
    "converting_mp3": "🎵 Konvertierung zu mp3...",
    "ok_audio_saved": "✅ Audio gespeichert: {path}",
    "warn_mp3_failed": "⚠️  mp3-Konvertierung fehlgeschlagen, die Originaldatei wird behalten",
    "err_mp3_convert": "❌ Fehler bei der mp3-Konvertierung: {stderr}",
    "extra_mp3": "🎵 Zusätzlich wird eine mp3-Spur gespeichert...",
    "ok_mp3_saved": "✅ mp3 gespeichert: {path}",
    "warn_mp3_kept_source": "⚠️  mp3 nicht konvertiert, die Quelldatei wurde behalten: {path}",

    # ---------- Result ----------
    "ok_video_saved": "✅ Video gespeichert: {path}",
    "err_download": "❌ Downloadfehler: {error}",
    "ok_log_entry": "📝 Eintrag zu {txt} und {html} hinzugefügt",

    # ---------- Transcript ----------
    "info_no_captions": "ℹ️  Untertitel/Transkript nicht verfügbar.",
    "info_available_subs": "📄 Verfügbare Untertitel: {codes}",
    "info_transcript_lang": "📄 Transkriptsprache: {code}",
    "ok_transcript": "✅ Transkript: {path}",
    "warn_transcript_error": "⚠️  Transkriptfehler: {error}",
    "tr_title": "# Transkript: {title}",
    "tr_author": "# Autor: {author}",
    "tr_lang": "# Sprache: {lang}",
    "tr_source": "# Quelle: {url}",

    # ---------- HTML log ----------
    "html_title": "Protokoll heruntergeladener Videos",
    "html_total": "Einträge gesamt: {count}",
    "html_empty": "Noch keine Einträge",
    "html_col_date": "Datum",
    "html_col_type": "Typ",
    "html_col_title": "Titel",
    "html_col_author": "Autor",
    "html_col_quality": "Qualität",
    "html_col_audio_lang": "Audiosprache",
    "html_col_duration": "Dauer",
    "html_col_size": "Größe",
    "html_col_audio_file": "Audiodatei",

    # ---------- Web server ----------
    "srv_url_missing": "URL fehlt",
    "srv_bad_quality": "Ungültige Qualität",
    "srv_ui_missing": "web_ui.html wurde nicht neben web_server.py gefunden",
    "srv_open_browser": "🌐 Im Browser öffnen: {url}",
    "srv_task_starting": "Wird gestartet…",
    "srv_task_done": "Fertig",

    # ---------- Web UI ----------
    "web_app_title": "🎬 YouTube Downloader",
    "web_subtitle": "Video, Audio und Transkripte — direkt aus dem Browser",
    "web_lang": "🌐 Sprache",
    "web_url_label": "Video-URL",
    "web_url_placeholder": "https://www.youtube.com/watch?v=...",
    "web_quality_label": "Qualität",
    "web_q_max": "Maximal (1080p+ DASH)",
    "web_q_medium": "Mittel",
    "web_lang_audio": "Audio-/Transkriptsprache",
    "web_q_audio": "Nur Audio (mp3)",
    "web_extra_label": "Extras",
    "web_save_mp3": "mp3 zusätzlich neben dem mp4 speichern",
    "web_btn_info": "🔍 Infos abrufen",
    "web_btn_download": "⬇️ Herunterladen",
    "web_btn_loading": '<span class="spinner"></span>Wird geladen…',
    "web_info_title": "Videoinformationen",
    "web_author": "Autor",
    "web_duration": "Dauer",
    "web_id": "ID",
    "web_status": "Status",
    "web_resolutions": "Verfügbare Auflösungen",
    "web_captions_yes": "  •  Untertitel verfügbar",
    "web_captions_no": "  •  keine Untertitel",
    "web_badge_new": "Neu",
    "web_badge_downloaded": "Bereits heruntergeladen",
    "web_progress_title": "Download-Fortschritt",
    "web_files_title": "📁 Heruntergeladene Dateien",
    "web_log_title": "📊 Download-Protokoll",
    "web_col_file": "Datei",
    "web_col_size": "Größe",
    "web_col_date": "Datum",
    "web_col_type": "Typ",
    "web_col_title": "Titel",
    "web_col_author": "Autor",
    "web_col_quality": "Qualität",
    "web_col_audio_file": "Audiodatei",
    "web_download_link": "herunterladen",
    "web_empty_files": "Noch keine Dateien",
    "web_empty_log": "Noch keine Einträge",
    "web_err_no_url": "Bitte eine Video-URL eingeben",
    "web_err_server": "Serverfehler",
    "web_err_prefix": "Fehler: ",
    "web_error_prefix": "❌ Fehler: ",
    "web_launching": "Wird gestartet…",
    "web_done": "✅ Fertig",
}
