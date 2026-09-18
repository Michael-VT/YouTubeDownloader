"""Textes d'interface en français."""

STRINGS = {
    # ---------- CLI: argparse ----------
    "app_desc": "Télécharge des vidéos, de l'audio et des transcriptions depuis YouTube.",
    "help_url": "URL de la vidéo YouTube",
    "help_quality": "Qualité : max / medium / low / audio",
    "help_lang": "Langue de l'audio/de la transcription (par défaut : {default})",
    "help_mp3": "Enregistrer aussi une piste mp3",
    "help_output": "Dossier de sortie (par défaut : downloads)",
    "help_ui_lang": "Langue de l'interface : en/ru/uk/pt/de/fr (par défaut : détection auto)",

    # ---------- CLI: interactive ----------
    "choose_quality": "Choisissez la qualité :",
    "q_max": "  1 — maximale (1080p+ via DASH)",
    "q_medium": "  2 — moyenne",
    "q_low": "  3 — basse",
    "q_audio": "  4 — audio uniquement (mp3)",
    "prompt_quality": "Numéro (1/2/3/4) [1] : ",
    "prompt_url": "🔗 URL YouTube : ",
    "prompt_lang": "Langue de l'audio/de la transcription [{default}] : ",
    "prompt_mp3": "Enregistrer aussi une piste mp3 ? (o/N) : ",

    # ---------- CLI: extended help ----------
    "extended_help": """YouTube Downloader — aide étendue

MODES DE QUALITÉ :
  max     — meilleure disponible (1080p, 1440p, 4K via DASH)
  medium  — moyenne
  low     — la plus basse (144p–360p)
  audio   — audio uniquement en mp3 (idéal pour l'écoute en déplacement)

OPTIONS SUPPLÉMENTAIRES :
  --mp3            enregistrer aussi une piste mp3 à côté du mp4
  --lang ru|en|…   langue de l'audio et de la transcription (par défaut : ru)
  --ui-lang LL     langue de l'interface : en/ru/uk/pt/de/fr (par défaut : auto)
  -o DIR           dossier de sortie (par défaut : downloads)

EXEMPLES :
  python download.py "https://youtu.be/XXXX" max
  python download.py "https://youtu.be/XXXX" audio
  python download.py "https://youtu.be/XXXX" medium --lang en
  python download.py "https://youtu.be/XXXX" max --mp3 -o video
  python download.py "https://youtu.be/XXXX" max --ui-lang de

SANS ARGUMENT, l'outil démarre en mode interactif et pose les questions étape par étape.""",

    # ---------- Fetch / info ----------
    "info_log_entries": "ℹ️  Le journal contient déjà {count} entrées.",
    "err_get_video": "❌ Erreur lors de la récupération de la vidéo : {error}",
    "warn_already_downloaded": "⚠️  Déjà téléchargée précédemment. Ignorée.",
    "already_id": "   ID : {id}",
    "already_title": "   Titre : {title}",
    "video_title": "🎬 Titre : {title}",
    "video_author": "👤 Auteur : {author}",
    "video_duration": "⏱  Durée : {duration}",
    "video_id": "🆔 ID : {id}",

    # ---------- Streams ----------
    "err_no_video_stream": "❌ Aucun flux vidéo adapté trouvé",
    "err_no_audio_stream": "❌ Impossible de sélectionner une piste audio",
    "audio_tracks_available": "🎧 Pistes audio disponibles :",
    "audio_track_line": "   • {track} | {abr} | itag={itag} | ext={ext}{default}",
    "audio_selected": "✅ Piste audio sélectionnée : {track} ({abr})",
    "audio_using_default": "ℹ️  Aucune piste dans la langue demandée, utilisation de la piste par défaut ({abr})",
    "audio_using_best": "ℹ️  Utilisation de la piste de meilleure qualité ({abr})",
    "audio_header": "🎧 Audio : {name} ({abr})",
    "video_stream_info": "🎞  Vidéo : {res} ({mode})",
    "merge_label": "🔧 Fusion : {value}",
    "word_yes": "oui",
    "word_no": "non",
    "audio_lang_embedded": "intégrée",

    # ---------- ffmpeg ----------
    "warn_no_ffmpeg_dash": "⚠️  ffmpeg introuvable — DASH (1080p+) indisponible.",
    "warn_fallback_progressive": "   Repli en progressive (720p max).",
    "err_no_progressive": "❌ Flux progressive indisponible. Installez ffmpeg.",
    "dl_video_stream": "⬇️  Téléchargement du flux vidéo...",
    "dl_audio_stream": "⬇️  Téléchargement du flux audio...",
    "downloaded": "⬇️  Téléchargé : {path}",
    "err_tmp_corrupt": "❌ Fichier temporaire corrompu ou vide : {path}",
    "merging": "🔗 Fusion vidéo et audio...",
    "merge_cmd": "🔗 Fusion ffmpeg : {cmd}",
    "err_ffmpeg_code": "❌ ffmpeg s'est terminé avec le code {code}",
    "stderr_tail": "   stderr : {stderr}",
    "err_output_missing": "❌ Le fichier de sortie est absent ou suspectement petit.",
    "err_no_audio_track_out": "❌ Aucune piste audio trouvée dans le fichier de sortie.",
    "warn_merge_failed": "⚠️  Échec de la fusion. Tentative de repli : progressive.",
    "ok_saved_fallback": "✅ Enregistré (repli) : {path}",

    # ---------- mp3 ----------
    "converting_mp3": "🎵 Conversion en mp3...",
    "ok_audio_saved": "✅ Audio enregistré : {path}",
    "warn_mp3_failed": "⚠️  Échec de la conversion mp3, conservation du fichier original",
    "err_mp3_convert": "❌ Erreur de conversion mp3 : {stderr}",
    "extra_mp3": "🎵 Enregistrement supplémentaire d'une piste mp3...",
    "ok_mp3_saved": "✅ mp3 enregistré : {path}",
    "warn_mp3_kept_source": "⚠️  mp3 non converti, fichier source conservé : {path}",

    # ---------- Result ----------
    "ok_video_saved": "✅ Vidéo enregistrée : {path}",
    "err_download": "❌ Erreur de téléchargement : {error}",
    "ok_log_entry": "📝 Entrée ajoutée à {txt} et {html}",

    # ---------- Transcript ----------
    "info_no_captions": "ℹ️  Sous-titres/transcription indisponibles.",
    "info_available_subs": "📄 Sous-titres disponibles : {codes}",
    "info_transcript_lang": "📄 Langue de la transcription : {code}",
    "ok_transcript": "✅ Transcription : {path}",
    "warn_transcript_error": "⚠️  Erreur de transcription : {error}",
    "tr_title": "# Transcription : {title}",
    "tr_author": "# Auteur : {author}",
    "tr_lang": "# Langue : {lang}",
    "tr_source": "# Source : {url}",

    # ---------- HTML log ----------
    "html_title": "Journal des vidéos téléchargées",
    "html_total": "Total des entrées : {count}",
    "html_empty": "Aucune entrée pour le moment",
    "html_col_date": "Date",
    "html_col_type": "Type",
    "html_col_title": "Titre",
    "html_col_author": "Auteur",
    "html_col_quality": "Qualité",
    "html_col_audio_lang": "Langue de l'audio",
    "html_col_duration": "Durée",
    "html_col_size": "Taille",
    "html_col_audio_file": "Fichier audio",

    # ---------- Web server ----------
    "srv_url_missing": "URL manquante",
    "srv_bad_quality": "Qualité invalide",
    "srv_ui_missing": "web_ui.html introuvable à côté de web_server.py",
    "srv_open_browser": "🌐 Ouvrez dans votre navigateur : {url}",
    "srv_task_starting": "Démarrage…",
    "srv_task_done": "Terminé",

    # ---------- Web UI ----------
    "web_app_title": "🎬 YouTube Downloader",
    "web_subtitle": "Vidéo, audio et transcriptions — directement depuis votre navigateur",
    "web_lang": "🌐 Langue",
    "web_url_label": "URL de la vidéo",
    "web_url_placeholder": "https://www.youtube.com/watch?v=...",
    "web_quality_label": "Qualité",
    "web_q_max": "Maximale (1080p+ DASH)",
    "web_q_medium": "Moyenne",
    "web_lang_audio": "Langue de l'audio / de la transcription",
    "web_q_audio": "Audio uniquement (mp3)",
    "web_extra_label": "Options supplémentaires",
    "web_save_mp3": "Enregistrer aussi le mp3 à côté du mp4",
    "web_btn_info": "🔍 Obtenir les infos",
    "web_btn_download": "⬇️ Télécharger",
    "web_btn_loading": '<span class="spinner"></span>Chargement…',
    "web_info_title": "Informations sur la vidéo",
    "web_author": "Auteur",
    "web_duration": "Durée",
    "web_id": "ID",
    "web_status": "Statut",
    "web_resolutions": "Résolutions disponibles",
    "web_captions_yes": "  •  sous-titres disponibles",
    "web_captions_no": "  •  pas de sous-titres",
    "web_badge_new": "Nouveau",
    "web_badge_downloaded": "Déjà téléchargée",
    "web_progress_title": "Progression du téléchargement",
    "web_files_title": "📁 Fichiers téléchargés",
    "web_log_title": "📊 Journal des téléchargements",
    "web_col_file": "Fichier",
    "web_col_size": "Taille",
    "web_col_date": "Date",
    "web_col_type": "Type",
    "web_col_title": "Titre",
    "web_col_author": "Auteur",
    "web_col_quality": "Qualité",
    "web_col_audio_file": "Fichier audio",
    "web_download_link": "télécharger",
    "web_empty_files": "Aucun fichier pour le moment",
    "web_empty_log": "Aucune entrée pour le moment",
    "web_err_no_url": "Saisissez une URL de vidéo",
    "web_err_server": "Erreur du serveur",
    "web_err_prefix": "Erreur : ",
    "web_error_prefix": "❌ Erreur : ",
    "web_launching": "Démarrage…",
    "web_done": "✅ Terminé",
}
