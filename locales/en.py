"""English strings (reference for all other locales)."""

STRINGS = {
    # ---------- CLI: argparse ----------
    "app_desc": "Download videos, audio and transcripts from YouTube.",
    "help_url": "YouTube video URL",
    "help_quality": "Quality: max / medium / low / audio / text",
    "help_lang": "Audio/transcript language (default: {default})",
    "help_mp3": "Also save an mp3 track",
    "help_output": "Output folder (default: downloads)",
    "help_ui_lang": "Interface language: en/ru/uk/pt/de/fr (default: auto-detect)",
    "help_abitrate": "mp3 bitrate for the audio/--mp3 modes (128k/192k/320k, default 192k)",
    "help_check_queue": "Check the waiting queue (whether anything became available) and exit",
    "help_queue_list": "Show the waiting queue",
    "help_queue_remove": "Remove a URL from the waiting queue",
    "help_watch": "Watch the queue: check every N minutes (default 15)",

    # ---------- CLI: interactive ----------
    "choose_quality": "Choose quality:",
    "q_max": "  1 — maximum (1080p+ via DASH)",
    "q_medium": "  2 — medium",
    "q_low": "  3 — low",
    "q_audio": "  4 — audio only (mp3)",
    "q_text": "  5 — text only (transcript)",
    "prompt_quality": "Number (1/2/3/4/5) [1]: ",
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
  text    — text only (transcript from subtitles)

EXTRA OPTIONS:
  --mp3            also save an mp3 track next to the mp4
  --abitrate RATE  mp3 bitrate: 128k/192k/320k (default 192k)
  --lang ru|en|…   audio and transcript language (default: ru)
  --ui-lang LL     interface language: en/ru/uk/pt/de/fr (default: auto)
  -o DIR           output folder (default: downloads)
  --check-queue    check the waiting queue and download whatever became available
  --queue-list     show the waiting queue
  --queue-remove U remove a URL from the waiting queue
  --watch [MIN]    watch the queue, checking every MIN minutes (default 15)

EXAMPLES:
  python download.py "https://youtu.be/XXXX" max
  python download.py "https://youtu.be/XXXX" audio
  python download.py "https://youtu.be/XXXX" text
  python download.py "https://youtu.be/XXXX" audio --abitrate 320k
  python download.py "https://youtu.be/XXXX" medium --lang en
  python download.py "https://youtu.be/XXXX" max --mp3 -o video
  python download.py "https://youtu.be/XXXX" max --ui-lang de

WITHOUT ARGUMENTS the tool runs in interactive mode and asks step by step.""",

    # ---------- Fetch / info ----------
    "info_log_entries": "ℹ️  The log already has {count} entries.",
    "err_get_video": "❌ Error fetching video: {error}",
    "err_bad_url": "❌ Invalid URL: {error}",
    "already_summary": "📦 Already downloaded for this video: {items}",
    "sum_video": "video {res}",
    "sum_audio": "audio {value}",
    "sum_transcript": "transcript",
    "already_video_quality": "⚠️  Video in {res} quality is already downloaded. Skipping.",
    "already_audio_quality": "⚠️  Audio mp3 {bitrate} is already downloaded. Skipping.",
    "already_transcript": "⚠️  Transcript already downloaded: {path}",
    "info_transcript_exists": "ℹ️  Transcript already exists — not downloading it again.",
    "err_no_captions_text": "❌ No subtitles available — the text of this video cannot be downloaded.",
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
    "info_file_exists": "ℹ️  “{old}” already exists — saving as “{new}” (the old file is kept).",
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

    # ---------- Waiting queue ----------
    "queue_added": "📥 The video is unavailable right now — added to the waiting queue.",
    "queue_hint": "   Check: --check-queue; watch: --watch; list: --queue-list.",
    "queue_already": "ℹ️  This video is already in the waiting queue.",
    "queue_count": "⏳ Waiting queue: {count} — checking…",
    "queue_checking": "⌛ Checking the waiting queue…",
    "queue_empty": "✅ The waiting queue is empty.",
    "queue_resolved": "🎉 The video became available — downloading: {title}",
    "queue_still_unavailable": "   • still unavailable: {url} ({reason})",
    "queue_watching": "👀 Watching the waiting queue: checking every {minutes} min (Ctrl+C to stop).",
    "queue_done_watching": "✅ The queue is empty — watching finished.",
    "queue_watch_stopped": "👋 Watching stopped.",
    "queue_list_header": "⏳ Waiting queue:",
    "queue_list_line": "   • [{quality}] {url} — added {added}; reason: {reason}",
    "queue_removed": "🗑 Removed from the queue: {url}",
    "queue_not_found": "ℹ️  Not in the queue: {url}",

    # ---------- Web server ----------
    "srv_url_missing": "URL is missing",
    "srv_bad_quality": "Invalid quality",
    "srv_ui_missing": "web_ui.html not found next to web_server.py",
    "srv_open_browser": "🌐 Open in your browser: {url}",
    "srv_task_starting": "Starting…",
    "srv_task_done": "Done",
    "srv_task_failed": "Download failed",
    "srv_bad_abitrate": "Invalid mp3 bitrate",

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
    "web_q_text": "Text only (transcript)",
    "web_extra_label": "Extras",
    "web_save_mp3": "Also save mp3 next to mp4",
    "web_abitrate_label": "mp3 bitrate (for audio)",
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
    "web_lbl_video": "video",
    "web_lbl_audio": "audio",
    "web_lbl_transcript": "text",
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
    "web_queue_title": "⏳ Waiting for availability",
    "web_queue_empty": "The queue is empty",
    "web_queue_col_url": "URL",
    "web_queue_col_quality": "Quality",
    "web_queue_col_added": "Added",
    "web_queue_col_reason": "Reason",
    "web_queue_btn_check": "⌛ Check now",
    "web_queue_checked": "Checked: {resolved} downloaded, {remaining} still waiting",
}
