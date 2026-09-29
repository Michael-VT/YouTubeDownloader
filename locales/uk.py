"""Українські рядки інтерфейсу."""

STRINGS = {
    # ---------- CLI: argparse ----------
    "app_desc": "Завантаження відео, аудіо та транскриптів з YouTube.",
    "help_url": "URL відео на YouTube",
    "help_quality": "Якість: max / medium / low / audio / text",
    "help_lang": "Мова аудіо/транскрипту (за замовчуванням: {default})",
    "help_mp3": "Також зберегти mp3-доріжку",
    "help_output": "Тека для збереження (за замовчуванням: downloads)",
    "help_ui_lang": "Мова інтерфейсу: en/ru/uk/pt/de/fr (за замовчуванням: автовизначення)",
    "help_abitrate": "Бітрейт mp3 для режимів audio/--mp3 (128k/192k/320k, типово 192k)",
    "help_check_queue": "Перевірити чергу очікування (чи стало щось доступним) і вийти",
    "help_queue_list": "Показати чергу очікування",
    "help_queue_remove": "Прибрати посилання з черги очікування",
    "help_watch": "Стежити за чергою: перевіряти кожні N хвилин (типово 15)",

    # ---------- CLI: interactive ----------
    "choose_quality": "Оберіть якість:",
    "q_max": "  1 — максимальна (1080p+ через DASH)",
    "q_medium": "  2 — середня",
    "q_low": "  3 — низька",
    "q_audio": "  4 — лише аудіо (mp3)",
    "q_text": "  5 — лише текст (транскрипція)",
    "prompt_quality": "Номер (1/2/3/4/5) [1]: ",
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
  text    — лише текст (транскрипція із субтитрів)

ДОДАТКОВІ ОПЦІЇ:
  --mp3            також зберегти mp3-доріжку поруч із mp4
  --abitrate RATE  бітрейт mp3: 128k/192k/320k (типово 192k)
  --lang ru|en|…   мова аудіо та транскрипту (за замовчуванням: ru)
  --ui-lang LL     мова інтерфейсу: en/ru/uk/pt/de/fr (за замовчуванням: авто)
  -o DIR           тека для збереження (за замовчуванням: downloads)
  --check-queue    перевірити чергу очікування і завантажити те, що стало доступним
  --queue-list     показати чергу очікування
  --queue-remove U прибрати посилання з черги очікування
  --watch [MIN]    стежити за чергою: перевірка кожні MIN хвилин (типово 15)

ПРИКЛАДИ:
  python download.py "https://youtu.be/XXXX" max
  python download.py "https://youtu.be/XXXX" audio
  python download.py "https://youtu.be/XXXX" text
  python download.py "https://youtu.be/XXXX" audio --abitrate 320k
  python download.py "https://youtu.be/XXXX" medium --lang en
  python download.py "https://youtu.be/XXXX" max --mp3 -o video
  python download.py "https://youtu.be/XXXX" max --ui-lang de

БЕЗ АРГУМЕНТІВ інструмент працює в інтерактивному режимі та запитує все крок за кроком.""",

    # ---------- Fetch / info ----------
    "info_log_entries": "ℹ️  У журналі вже {count} записів.",
    "err_get_video": "❌ Помилка отримання відео: {error}",
    "err_bad_url": "❌ Некоректне посилання: {error}",
    "already_summary": "📦 Уже завантажено для цього відео: {items}",
    "sum_video": "відео {res}",
    "sum_audio": "аудіо {value}",
    "sum_transcript": "транскрипція",
    "already_video_quality": "⚠️  Відео в якості {res} уже завантажено. Пропускаю.",
    "already_audio_quality": "⚠️  Аудіо mp3 {bitrate} уже завантажено. Пропускаю.",
    "already_transcript": "⚠️  Транскрипція вже завантажена: {path}",
    "info_transcript_exists": "ℹ️  Транскрипція вже є — повторно не завантажую.",
    "err_no_captions_text": "❌ Субтитри недоступні — текст цього відео отримати не можна.",
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

    # ---------- Черга очікування ----------
    "queue_added": "📥 Відео зараз недоступне — додано до черги очікування.",
    "queue_hint": "   Перевірити: --check-queue; стежити: --watch; список: --queue-list.",
    "queue_already": "ℹ️  Це відео вже в черзі очікування.",
    "queue_count": "⏳ У черзі очікування: {count} — перевіряю…",
    "queue_checking": "⌛ Перевіряю чергу очікування…",
    "queue_empty": "✅ Черга очікування порожня.",
    "queue_resolved": "🎉 Відео стало доступним — завантажую: {title}",
    "queue_still_unavailable": "   • досі недоступне: {url} ({reason})",
    "queue_watching": "👀 Стежу за чергою очікування: перевірка кожні {minutes} хв (Ctrl+C — вихід).",
    "queue_done_watching": "✅ Черга порожня — стеження завершено.",
    "queue_watch_stopped": "👋 Стеження зупинено.",
    "queue_list_header": "⏳ Черга очікування:",
    "queue_list_line": "   • [{quality}] {url} — додано {added}; причина: {reason}",
    "queue_removed": "🗑 Прибрано з черги: {url}",
    "queue_not_found": "ℹ️  Цього посилання немає в черзі: {url}",

    # ---------- Web server ----------
    "srv_url_missing": "Не вказано URL",
    "srv_bad_quality": "Некоректна якість",
    "srv_ui_missing": "web_ui.html не знайдено поруч із web_server.py",
    "srv_open_browser": "🌐 Відкрийте у браузері: {url}",
    "srv_task_starting": "Запуск…",
    "srv_task_done": "Готово",
    "srv_task_failed": "Завантаження не вдалося",
    "srv_bad_abitrate": "Некоректний бітрейт mp3",

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
    "web_q_text": "Лише текст (транскрипція)",
    "web_extra_label": "Додатково",
    "web_save_mp3": "Також зберегти mp3 поруч із mp4",
    "web_abitrate_label": "Бітрейт mp3 (для аудіо)",
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
    "web_lbl_video": "відео",
    "web_lbl_audio": "аудіо",
    "web_lbl_transcript": "текст",
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
    "web_queue_title": "⏳ Очікування доступності",
    "web_queue_empty": "Черга порожня",
    "web_queue_col_url": "Посилання",
    "web_queue_col_quality": "Якість",
    "web_queue_col_added": "Додано",
    "web_queue_col_reason": "Причина",
    "web_queue_btn_check": "⌛ Перевірити зараз",
    "web_queue_checked": "Перевірено: завантажено {resolved}, лишилось у черзі {remaining}",
}
