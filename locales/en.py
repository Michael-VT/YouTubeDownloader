"""English strings (reference for all other locales)."""

STRINGS = {
    # ---------- CLI: argparse ----------
    "app_desc": "Download videos, audio and transcripts from YouTube.",
    "help_url": "YouTube video URL",
    "help_quality": "Quality: max / medium / low / audio",
    "help_lang": "Audio/transcript language (default: {default})",
    "help_mp3": "Also save an mp3 track",
    "help_output": "Output folder (default: downloads)",
    "help_ui_lang": "Interface language: en/ru/uk/pt/de/fr (default: auto-detect)",

    # ---------- CLI: interactive ----------
    "choose_quality": "Choose quality:",
    "q_max": "  1 — maximum (1080p+ via DASH)",
    "q_medium": "  2 — medium",
    "q_low": "  3 — low",
    "q_audio": "  4 — audio only (mp3)",
    "prompt_quality": "Number (1/2/3/4) [1]: ",
    "prompt_url": "🔗 YouTube URL: ",
    "prompt_lang": "Audio/transcript language [{default}]: ",
    "prompt_mp3": "Also save an mp3 track? (y/N): ",

    # ---------- CLI: extended help ----------
    "extended_help": """YouTube Downloader — extended help

QUALITY MODES:
  max     — best available (1080p, 1440p, 4K via DASH)
  medium  — medium
  low     — lowest (144p–360p)
  audio   — audio only as mp3 (great for listening on the go)

EXTRA OPTIONS:
  --mp3            also save an mp3 track next to the mp4
  --lang ru|en|…   audio and transcript language (default: ru)
  --ui-lang LL     interface language: en/ru/uk/pt/de/fr (default: auto)
  -o DIR           output folder (default: downloads)

EXAMPLES:
  python download.py "https://youtu.be/XXXX" max
  python download.py "https://youtu.be/XXXX" audio
  python download.py "https://youtu.be/XXXX" medium --lang en
  python download.py "https://youtu.be/XXXX" max --mp3 -o video
  python download.py "https://youtu.be/XXXX" max --ui-lang de

WITHOUT ARGUMENTS the tool runs in interactive mode and asks step by step.""",

    # ---------- Fetch / info ----------
    "info_log_entries": "ℹ️  The log already has {count} entries.",
    "err_get_video": "❌ Error fetching video: {error}",
    "warn_already_downloaded": "⚠️  Already downloaded earlier. Skipping.",
    "already_id": "   ID: {id}",
    "already_title": "   Title: {title}",
    "video_title": "🎬 Title: {title}",
    "video_author": "👤 Author: {author}",
    "video_duration": "⏱  Duration: {duration}",
    "video_id": "🆔 ID: {id}",

    # ---------- Streams ----------
    "err_no_video_stream": "❌ No suitable video stream found",
    "err_no_audio_stream": "❌ Could not select an audio track",
    "audio_tracks_available": "🎧 Available audio tracks:",
    "audio_track_line": "   • {track} | {abr} | itag={itag} | ext={ext}{default}",
    "audio_selected": "✅ Selected audio track: {track} ({abr})",
    "audio_using_default": "ℹ️  No track for the requested language, using the default one ({abr})",
    "audio_using_best": "ℹ️  Using the highest quality track ({abr})",
    "audio_header": "🎧 Audio: {name} ({abr})",
    "video_stream_info": "🎞  Video: {res} ({mode})",
    "merge_label": "🔧 Merge: {value}",
    "word_yes": "yes",
    "word_no": "no",
    "audio_lang_embedded": "embedded",

    # ---------- ffmpeg ----------
    "warn_no_ffmpeg_dash": "⚠️  ffmpeg not found — DASH (1080p+) is unavailable.",
    "warn_fallback_progressive": "   Falling back to progressive (720p max).",
    "err_no_progressive": "❌ Progressive stream unavailable. Install ffmpeg.",
    "dl_video_stream": "⬇️  Downloading video stream...",
    "dl_audio_stream": "⬇️  Downloading audio stream...",
    "downloaded": "⬇️  Downloaded: {path}",
    "err_tmp_corrupt": "❌ Temporary file corrupted or empty: {path}",
    "merging": "🔗 Merging video and audio...",
    "merge_cmd": "🔗 ffmpeg merge: {cmd}",
    "err_ffmpeg_code": "❌ ffmpeg exited with code {code}",
    "stderr_tail": "   stderr: {stderr}",
    "err_output_missing": "❌ Output file is missing or suspiciously small.",
    "err_no_audio_track_out": "❌ No audio track found in the output file.",
    "warn_merge_failed": "⚠️  Merge failed. Trying fallback: progressive.",
    "ok_saved_fallback": "✅ Saved (fallback): {path}",

    # ---------- mp3 ----------
    "converting_mp3": "🎵 Converting to mp3...",
    "ok_audio_saved": "✅ Audio saved: {path}",
    "warn_mp3_failed": "⚠️  mp3 conversion failed, keeping the original file",
    "err_mp3_convert": "❌ mp3 conversion error: {stderr}",
    "extra_mp3": "🎵 Also saving an mp3 track...",
    "ok_mp3_saved": "✅ mp3 saved: {path}",
    "warn_mp3_kept_source": "⚠️  mp3 not converted, kept the source file: {path}",

    # ---------- Result ----------
    "ok_video_saved": "✅ Video saved: {path}",
    "err_download": "❌ Download error: {error}",
    "ok_log_entry": "📝 Entry added to {txt} and {html}",

    # ---------- Transcript ----------
    "info_no_captions": "ℹ️  Subtitles/transcript unavailable.",
    "info_available_subs": "📄 Available subtitles: {codes}",
    "info_transcript_lang": "📄 Transcript language: {code}",
    "ok_transcript": "✅ Transcript: {path}",
    "warn_transcript_error": "⚠️  Transcript error: {error}",
    "tr_title": "# Transcript: {title}",
    "tr_author": "# Author: {author}",
    "tr_lang": "# Language: {lang}",
    "tr_source": "# Source: {url}",

    # ---------- HTML log ----------
    "html_title": "Downloaded videos log",
    "html_total": "Total entries: {count}",
    "html_empty": "No entries yet",
    "html_col_date": "Date",
    "html_col_type": "Type",
    "html_col_title": "Title",
    "html_col_author": "Author",
    "html_col_quality": "Quality",
    "html_col_audio_lang": "Audio language",
    "html_col_duration": "Duration",
    "html_col_size": "Size",
    "html_col_audio_file": "Audio file",

    # ---------- Web server ----------
    "srv_url_missing": "URL is missing",
    "srv_bad_quality": "Invalid quality",
    "srv_ui_missing": "web_ui.html not found next to web_server.py",
    "srv_open_browser": "🌐 Open in your browser: {url}",
    "srv_task_starting": "Starting…",
    "srv_task_done": "Done",

    # ---------- Web UI ----------
    "web_app_title": "🎬 YouTube Downloader",
    "web_subtitle": "Video, audio and transcripts — right from your browser",
    "web_lang": "🌐 Language",
    "web_url_label": "Video URL",
    "web_url_placeholder": "https://www.youtube.com/watch?v=...",
    "web_quality_label": "Quality",
    "web_q_max": "Maximum (1080p+ DASH)",
    "web_q_medium": "Medium",
    "web_lang_audio": "Audio / transcript language",
    "web_q_audio": "Audio only (mp3)",
    "web_extra_label": "Extras",
    "web_save_mp3": "Also save mp3 next to mp4",
    "web_btn_info": "🔍 Get info",
    "web_btn_download": "⬇️ Download",
    "web_btn_loading": '<span class="spinner"></span>Loading…',
    "web_info_title": "Video information",
    "web_author": "Author",
    "web_duration": "Duration",
    "web_id": "ID",
    "web_status": "Status",
    "web_resolutions": "Available resolutions",
    "web_captions_yes": "  •  subtitles available",
    "web_captions_no": "  •  no subtitles",
    "web_badge_new": "New",
    "web_badge_downloaded": "Already downloaded",
    "web_progress_title": "Download progress",
    "web_files_title": "📁 Downloaded files",
    "web_log_title": "📊 Download log",
    "web_col_file": "File",
    "web_col_size": "Size",
    "web_col_date": "Date",
    "web_col_type": "Type",
    "web_col_title": "Title",
    "web_col_author": "Author",
    "web_col_quality": "Quality",
    "web_col_audio_file": "Audio file",
    "web_download_link": "download",
    "web_empty_files": "No files yet",
    "web_empty_log": "No entries yet",
    "web_err_no_url": "Enter a video URL",
    "web_err_server": "Server error",
    "web_err_prefix": "Error: ",
    "web_error_prefix": "❌ Error: ",
    "web_launching": "Starting…",
    "web_done": "✅ Done",
}
