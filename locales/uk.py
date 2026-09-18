"""Українські рядки інтерфейсу."""

STRINGS = {
    # ---------- CLI: argparse ----------
    "app_desc": "Завантаження відео, аудіо та транскриптів з YouTube.",
    "help_url": "URL відео на YouTube",
    "help_quality": "Якість: max / medium / low / audio",
    "help_lang": "Мова аудіо/транскрипту (за замовчуванням: {default})",
    "help_mp3": "Також зберегти mp3-доріжку",
    "help_output": "Тека для збереження (за замовчуванням: downloads)",
    "help_ui_lang": "Мова інтерфейсу: en/ru/uk/pt/de/fr (за замовчуванням: автовизначення)",

    # ---------- CLI: interactive ----------
    "choose_quality": "Оберіть якість:",
    "q_max": "  1 — максимальна (1080p+ через DASH)",
    "q_medium": "  2 — середня",
    "q_low": "  3 — низька",
    "q_audio": "  4 — лише аудіо (mp3)",
    "prompt_quality": "Номер (1/2/3/4) [1]: ",
    "prompt_url": "🔗 URL YouTube: ",
    "prompt_lang": "Мова аудіо/транскрипту [{default}]: ",
    "prompt_mp3": "Також зберегти mp3-доріжку? (y/N): ",

    # ---------- CLI: extended help ----------
    "extended_help": """YouTube Downloader — розширена довідка

РЕЖИМИ ЯКОСТІ:
  max     — найкраща доступна (1080p, 1440p, 4K через DASH)
  medium  — середня
  low     — найнижча (144p–360p)
  audio   — лише аудіо у форматі mp3 (зручно для прослуховування)

ДОДАТКОВІ ОПЦІЇ:
  --mp3            також зберегти mp3-доріжку поруч із mp4
  --lang ru|en|…   мова аудіо та транскрипту (за замовчуванням: ru)
  --ui-lang LL     мова інтерфейсу: en/ru/uk/pt/de/fr (за замовчуванням: авто)
  -o DIR           тека для збереження (за замовчуванням: downloads)

ПРИКЛАДИ:
  python download.py "https://youtu.be/XXXX" max
  python download.py "https://youtu.be/XXXX" audio
  python download.py "https://youtu.be/XXXX" medium --lang en
  python download.py "https://youtu.be/XXXX" max --mp3 -o video
  python download.py "https://youtu.be/XXXX" max --ui-lang de

БЕЗ АРГУМЕНТІВ інструмент працює в інтерактивному режимі та запитує все крок за кроком.""",

    # ---------- Fetch / info ----------
    "info_log_entries": "ℹ️  У журналі вже {count} записів.",
    "err_get_video": "❌ Помилка отримання відео: {error}",
    "warn_already_downloaded": "⚠️  Це відео вже завантажене раніше. Пропускаємо.",
    "already_id": "   ID: {id}",
    "already_title": "   Назва: {title}",
    "video_title": "🎬 Назва: {title}",
    "video_author": "👤 Автор: {author}",
    "video_duration": "⏱  Тривалість: {duration}",
    "video_id": "🆔 ID: {id}",

    # ---------- Streams ----------
    "err_no_video_stream": "❌ Не знайдено підходящого відеопотоку",
    "err_no_audio_stream": "❌ Не вдалося обрати аудіодоріжку",
    "audio_tracks_available": "🎧 Доступні аудіодоріжки:",
    "audio_track_line": "   • {track} | {abr} | itag={itag} | ext={ext}{default}",
    "audio_selected": "✅ Обрано аудіодоріжку: {track} ({abr})",
    "audio_using_default": "ℹ️  Немає доріжки для запитаної мови, використовуємо типову ({abr})",
    "audio_using_best": "ℹ️  Використовуємо доріжку з найвищою якістю ({abr})",
    "audio_header": "🎧 Аудіо: {name} ({abr})",
    "video_stream_info": "🎞  Відео: {res} ({mode})",
    "merge_label": "🔧 Злиття: {value}",
    "word_yes": "так",
    "word_no": "ні",
    "audio_lang_embedded": "вбудована",

    # ---------- ffmpeg ----------
    "warn_no_ffmpeg_dash": "⚠️  ffmpeg не знайдено — DASH (1080p+) недоступний.",
    "warn_fallback_progressive": "   Перехід на progressive (максимум 720p).",
    "err_no_progressive": "❌ Progressive-потік недоступний. Встановіть ffmpeg.",
    "dl_video_stream": "⬇️  Завантаження відеопотоку...",
    "dl_audio_stream": "⬇️  Завантаження аудіопотоку...",
    "downloaded": "⬇️  Завантажено: {path}",
    "err_tmp_corrupt": "❌ Тимчасовий файл пошкоджений або порожній: {path}",
    "merging": "🔗 Злиття відео та аудіо...",
    "merge_cmd": "🔗 Злиття ffmpeg: {cmd}",
    "err_ffmpeg_code": "❌ ffmpeg завершився з кодом {code}",
    "stderr_tail": "   stderr: {stderr}",
    "err_output_missing": "❌ Вихідний файл відсутній або підозріло малий.",
    "err_no_audio_track_out": "❌ У вихідному файлі не знайдено аудіодоріжки.",
    "warn_merge_failed": "⚠️  Злиття не вдалося. Спроба запасного варіанту: progressive.",
    "ok_saved_fallback": "✅ Збережено (запасний варіант): {path}",

    # ---------- mp3 ----------
    "converting_mp3": "🎵 Конвертація в mp3...",
    "ok_audio_saved": "✅ Аудіо збережено: {path}",
    "warn_mp3_failed": "⚠️  Не вдалося конвертувати в mp3, залишаємо початковий файл",
    "err_mp3_convert": "❌ Помилка конвертації в mp3: {stderr}",
    "extra_mp3": "🎵 Також зберігаємо mp3-доріжку...",
    "ok_mp3_saved": "✅ mp3 збережено: {path}",
    "warn_mp3_kept_source": "⚠️  mp3 не сконвертовано, збережено початковий файл: {path}",

    # ---------- Result ----------
    "ok_video_saved": "✅ Відео збережено: {path}",
    "err_download": "❌ Помилка завантаження: {error}",
    "ok_log_entry": "📝 Запис додано до {txt} і {html}",

    # ---------- Transcript ----------
    "info_no_captions": "ℹ️  Субтитри/транскрипт недоступні.",
    "info_available_subs": "📄 Доступні субтитри: {codes}",
    "info_transcript_lang": "📄 Мова транскрипту: {code}",
    "ok_transcript": "✅ Транскрипт: {path}",
    "warn_transcript_error": "⚠️  Помилка транскрипту: {error}",
    "tr_title": "# Транскрипт: {title}",
    "tr_author": "# Автор: {author}",
    "tr_lang": "# Мова: {lang}",
    "tr_source": "# Джерело: {url}",

    # ---------- HTML log ----------
    "html_title": "Журнал завантажених відео",
    "html_total": "Усього записів: {count}",
    "html_empty": "Записів ще немає",
    "html_col_date": "Дата",
    "html_col_type": "Тип",
    "html_col_title": "Назва",
    "html_col_author": "Автор",
    "html_col_quality": "Якість",
    "html_col_audio_lang": "Мова аудіо",
    "html_col_duration": "Тривалість",
    "html_col_size": "Розмір",
    "html_col_audio_file": "Аудіофайл",

    # ---------- Web server ----------
    "srv_url_missing": "Не вказано URL",
    "srv_bad_quality": "Некоректна якість",
    "srv_ui_missing": "web_ui.html не знайдено поруч із web_server.py",
    "srv_open_browser": "🌐 Відкрийте у браузері: {url}",
    "srv_task_starting": "Запуск…",
    "srv_task_done": "Готово",

    # ---------- Web UI ----------
    "web_app_title": "🎬 YouTube Downloader",
    "web_subtitle": "Відео, аудіо та транскрипти — просто з вашого браузера",
    "web_lang": "🌐 Мова",
    "web_url_label": "URL відео",
    "web_url_placeholder": "https://www.youtube.com/watch?v=...",
    "web_quality_label": "Якість",
    "web_q_max": "Максимальна (1080p+ DASH)",
    "web_q_medium": "Середня",
    "web_lang_audio": "Мова аудіо / транскрипту",
    "web_q_audio": "Лише аудіо (mp3)",
    "web_extra_label": "Додатково",
    "web_save_mp3": "Також зберегти mp3 поруч із mp4",
    "web_btn_info": "🔍 Отримати інформацію",
    "web_btn_download": "⬇️ Завантажити",
    "web_btn_loading": '<span class="spinner"></span>Завантаження…',
    "web_info_title": "Інформація про відео",
    "web_author": "Автор",
    "web_duration": "Тривалість",
    "web_id": "ID",
    "web_status": "Статус",
    "web_resolutions": "Доступні роздільності",
    "web_captions_yes": "  •  субтитри доступні",
    "web_captions_no": "  •  без субтитрів",
    "web_badge_new": "Нове",
    "web_badge_downloaded": "Вже завантажено",
    "web_progress_title": "Хід завантаження",
    "web_files_title": "📁 Завантажені файли",
    "web_log_title": "📊 Журнал завантажень",
    "web_col_file": "Файл",
    "web_col_size": "Розмір",
    "web_col_date": "Дата",
    "web_col_type": "Тип",
    "web_col_title": "Назва",
    "web_col_author": "Автор",
    "web_col_quality": "Якість",
    "web_col_audio_file": "Аудіофайл",
    "web_download_link": "завантажити",
    "web_empty_files": "Файлів ще немає",
    "web_empty_log": "Записів ще немає",
    "web_err_no_url": "Введіть URL відео",
    "web_err_server": "Помилка сервера",
    "web_err_prefix": "Помилка: ",
    "web_error_prefix": "❌ Помилка: ",
    "web_launching": "Запуск…",
    "web_done": "✅ Готово",
}
