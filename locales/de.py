"""Deutsche UI-Texte."""

STRINGS = {
    # ---------- CLI: argparse ----------
    "app_desc": "Videos, Audio und Transkripte von YouTube herunterladen.",
    "help_url": "YouTube-Video-URL",
    "help_quality": "Qualität: max / medium / low / audio / text",
    "help_lang": "Audio-/Transkriptsprache (Standard: {default})",
    "help_mp3": "Zusätzlich eine mp3-Spur speichern",
    "help_output": "Ausgabeordner (Standard: downloads)",
    "help_ui_lang": "Sprache der Oberfläche: en/ru/uk/pt/de/fr (Standard: automatisch)",
    "help_abitrate": "mp3-Bitrate für die Modi audio/--mp3 (128k/192k/320k, Standard 192k)",
    "help_check_queue": "Warteschlange prüfen (ob etwas verfügbar wurde) und beenden",
    "help_queue_list": "Warteschlange anzeigen",
    "help_queue_remove": "Link aus der Warteschlange entfernen",
    "help_watch": "Warteschlange überwachen: alle N Minuten prüfen (Standard 15)",

    # ---------- CLI: interactive ----------
    "choose_quality": "Qualität wählen:",
    "q_max": "  1 — maximal (1080p+ via DASH)",
    "q_medium": "  2 — mittel",
    "q_low": "  3 — niedrig",
    "q_audio": "  4 — nur Audio (mp3)",
    "q_text": "  5 — nur Text (Transkription)",
    "prompt_quality": "Nummer (1/2/3/4/5) [1]: ",
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
  text    — nur Text (Transkription aus den Untertiteln)

ZUSÄTZLICHE OPTIONEN:
  --mp3            zusätzlich eine mp3-Spur neben dem mp4 speichern
  --abitrate RATE  mp3-Bitrate: 128k/192k/320k (Standard 192k)
  --lang ru|en|…   Audio- und Transkriptsprache (Standard: ru)
  --ui-lang LL     Sprache der Oberfläche: en/ru/uk/pt/de/fr (Standard: automatisch)
  -o DIR           Ausgabeordner (Standard: downloads)
  --check-queue    Warteschlange prüfen und Verfügbares herunterladen
  --queue-list     Warteschlange anzeigen
  --queue-remove U Link aus der Warteschlange entfernen
  --watch [MIN]    Warteschlange überwachen: Prüfung alle MIN Minuten (Standard 15)

BEISPIELE:
  python download.py "https://youtu.be/XXXX" max
  python download.py "https://youtu.be/XXXX" audio
  python download.py "https://youtu.be/XXXX" text
  python download.py "https://youtu.be/XXXX" audio --abitrate 320k
  python download.py "https://youtu.be/XXXX" medium --lang en
  python download.py "https://youtu.be/XXXX" max --mp3 -o video
  python download.py "https://youtu.be/XXXX" max --ui-lang de

OHNE ARGUMENTE läuft das Tool im interaktiven Modus und fragt Schritt für Schritt ab.""",

    # ---------- Fetch / info ----------
    "info_log_entries": "ℹ️  Das Protokoll enthält bereits {count} Einträge.",
    "err_get_video": "❌ Fehler beim Abrufen des Videos: {error}",
    "err_bad_url": "❌ Ungültiger Link: {error}",
    "already_summary": "📦 Für dieses Video bereits geladen: {items}",
    "sum_video": "Video {res}",
    "sum_audio": "Audio {value}",
    "sum_transcript": "Transkription",
    "already_video_quality": "⚠️  Video in {res} bereits heruntergeladen. Wird übersprungen.",
    "already_audio_quality": "⚠️  Audio mp3 {bitrate} bereits heruntergeladen. Wird übersprungen.",
    "already_transcript": "⚠️  Transkription bereits heruntergeladen: {path}",
    "info_transcript_exists": "ℹ️  Transkription ist bereits vorhanden — wird nicht erneut geladen.",
    "err_no_captions_text": "❌ Keine Untertitel verfügbar — der Text dieses Videos kann nicht geladen werden.",
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

    # ---------- Warteschlange ----------
    "queue_added": "📥 Das Video ist derzeit nicht verfügbar — in die Warteschlange gestellt.",
    "queue_hint": "   Prüfen: --check-queue; überwachen: --watch; Liste: --queue-list.",
    "queue_already": "ℹ️  Dieses Video steht bereits in der Warteschlange.",
    "queue_count": "⏳ In der Warteschlange: {count} — prüfe…",
    "queue_checking": "⌛ Prüfe die Warteschlange…",
    "queue_empty": "✅ Die Warteschlange ist leer.",
    "queue_resolved": "🎉 Das Video ist jetzt verfügbar — lade: {title}",
    "queue_still_unavailable": "   • noch nicht verfügbar: {url} ({reason})",
    "queue_watching": "👀 Überwache die Warteschlange: Prüfung alle {minutes} Min (Ctrl+C zum Beenden).",
    "queue_done_watching": "✅ Warteschlange leer — Überwachung beendet.",
    "queue_watch_stopped": "👋 Überwachung gestoppt.",
    "queue_list_header": "⏳ Warteschlange:",
    "queue_list_line": "   • [{quality}] {url} — hinzugefügt {added}; Grund: {reason}",
    "queue_removed": "🗑 Aus der Warteschlange entfernt: {url}",
    "queue_not_found": "ℹ️  Dieser Link ist nicht in der Warteschlange: {url}",

    # ---------- Web server ----------
    "srv_url_missing": "URL fehlt",
    "srv_bad_quality": "Ungültige Qualität",
    "srv_ui_missing": "web_ui.html wurde nicht neben web_server.py gefunden",
    "srv_open_browser": "🌐 Im Browser öffnen: {url}",
    "srv_task_starting": "Wird gestartet…",
    "srv_task_done": "Fertig",
    "srv_task_failed": "Download fehlgeschlagen",
    "srv_bad_abitrate": "Ungültige mp3-Bitrate",

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
    "web_q_text": "Nur Text (Transkription)",
    "web_extra_label": "Extras",
    "web_save_mp3": "mp3 zusätzlich neben dem mp4 speichern",
    "web_abitrate_label": "mp3-Bitrate (für Audio)",
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
    "web_lbl_video": "Video",
    "web_lbl_audio": "Audio",
    "web_lbl_transcript": "Text",
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
    "web_queue_title": "⏳ Warten auf Verfügbarkeit",
    "web_queue_empty": "Warteschlange leer",
    "web_queue_col_url": "Link",
    "web_queue_col_quality": "Qualität",
    "web_queue_col_added": "Hinzugefügt",
    "web_queue_col_reason": "Grund",
    "web_queue_btn_check": "⌛ Jetzt prüfen",
    "web_queue_checked": "Geprüft: {resolved} geladen, {remaining} verbleiben in der Warteschlange",
}
