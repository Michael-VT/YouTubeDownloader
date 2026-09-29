"""Русские строки (исходный язык интерфейса программы)."""

STRINGS = {
    # ---------- CLI: argparse ----------
    "app_desc": "Скачивание видео, аудио и транскрипций с YouTube.",
    "help_url": "Ссылка на YouTube-видео",
    "help_quality": "Качество: max / medium / low / audio / text",
    "help_lang": "Язык аудио/транскрипции (по умолчанию: {default})",
    "help_mp3": "Дополнительно сохранить mp3-дорожку",
    "help_output": "Папка для сохранения (по умолчанию: downloads)",
    "help_ui_lang": "Язык интерфейса: en/ru/uk/pt/de/fr (по умолчанию: авто)",
    "help_abitrate": "Битрейт mp3 для режимов audio/--mp3 (128k/192k/320k, по умолчанию 192k)",
    "help_check_queue": "Проверить очередь ожидания (не стало ли что-то доступным) и выйти",
    "help_queue_list": "Показать очередь ожидания",
    "help_queue_remove": "Убрать ссылку из очереди ожидания",
    "help_watch": "Следить за очередью: проверять каждые N минут (по умолчанию 15)",

    # ---------- CLI: interactive ----------
    "choose_quality": "Выберите качество:",
    "q_max": "  1 — максимальное (1080p+ через DASH)",
    "q_medium": "  2 — среднее",
    "q_low": "  3 — низкое",
    "q_audio": "  4 — только аудио (mp3)",
    "q_text": "  5 — только текст (транскрипция)",
    "prompt_quality": "Номер (1/2/3/4/5) [1]: ",
    "prompt_url": "🔗 Ссылка на YouTube: ",
    "prompt_lang": "Язык аудио/транскрипции [{default}]: ",
    "prompt_mp3": "Сохранить также mp3-дорожку? (y/N): ",

    # ---------- CLI: extended help ----------
    "extended_help": """YouTube Downloader — подробная справка

РЕЖИМЫ КАЧЕСТВА:
  max     — максимальное доступное (1080p, 1440p, 4K через DASH)
  medium  — среднее
  low     — минимальное (144p–360p)
  audio   — только аудио в mp3 (удобно слушать в пути)
  text    — только текст (транскрипция из субтитров)

ДОПОЛНИТЕЛЬНО:
  --mp3            дополнительно сохранить mp3-дорожку рядом с mp4
  --abitrate RATE  битрейт mp3: 128k/192k/320k (по умолчанию 192k)
  --lang ru|en|…   язык аудио и транскрипции (по умолчанию ru)
  --ui-lang LL     язык интерфейса: en/ru/uk/pt/de/fr (по умолчанию авто)
  -o DIR           папка для сохранения (по умолчанию downloads)
  --check-queue    проверить очередь ожидания и скачать ставшее доступным
  --queue-list     показать очередь ожидания
  --queue-remove U убрать ссылку из очереди ожидания
  --watch [MIN]    следить за очередью: проверка каждые MIN минут (по умолчанию 15)

ПРИМЕРЫ:
  python download.py "https://youtu.be/XXXX" max
  python download.py "https://youtu.be/XXXX" audio
  python download.py "https://youtu.be/XXXX" text
  python download.py "https://youtu.be/XXXX" audio --abitrate 320k
  python download.py "https://youtu.be/XXXX" medium --lang en
  python download.py "https://youtu.be/XXXX" max --mp3 -o video
  python download.py "https://youtu.be/XXXX" max --ui-lang de

БЕЗ АРГУМЕНТОВ программа работает в интерактивном режиме с пошаговыми вопросами.""",

    # ---------- Fetch / info ----------
    "info_log_entries": "ℹ️  В журнале уже {count} записей.",
    "err_get_video": "❌ Ошибка получения видео: {error}",
    "err_bad_url": "❌ Некорректная ссылка: {error}",
    "already_summary": "📦 Уже скачано для этого видео: {items}",
    "sum_video": "видео {res}",
    "sum_audio": "аудио {value}",
    "sum_transcript": "транскрипция",
    "already_video_quality": "⚠️  Видео в качестве {res} уже скачано. Пропускаю.",
    "already_audio_quality": "⚠️  Аудио mp3 {bitrate} уже скачано. Пропускаю.",
    "already_transcript": "⚠️  Транскрипция уже скачана: {path}",
    "info_transcript_exists": "ℹ️  Транскрипция уже есть — повторно не качаю.",
    "err_no_captions_text": "❌ Субтитры недоступны — текст этого видео получить нельзя.",
    "video_title": "🎬 Название: {title}",
    "video_author": "👤 Автор: {author}",
    "video_duration": "⏱  Длительность: {duration}",
    "video_id": "🆔 ID: {id}",

    # ---------- Streams ----------
    "err_no_video_stream": "❌ Не удалось найти подходящий видеопоток",
    "err_no_audio_stream": "❌ Не удалось выбрать аудиодорожку",
    "audio_tracks_available": "🎧 Доступные аудиодорожки:",
    "audio_track_line": "   • {track} | {abr} | itag={itag} | ext={ext}{default}",
    "audio_selected": "✅ Выбрана аудиодорожка: {track} ({abr})",
    "audio_using_default": "ℹ️  Дорожки на запрошенном языке нет, используем default ({abr})",
    "audio_using_best": "ℹ️  Используем самую качественную дорожку ({abr})",
    "audio_header": "🎧 Аудио: {name} ({abr})",
    "video_stream_info": "🎞  Видео: {res} ({mode})",
    "merge_label": "🔧 Склейка: {value}",
    "word_yes": "да",
    "word_no": "нет",
    "audio_lang_embedded": "встроенная",

    # ---------- ffmpeg ----------
    "warn_no_ffmpeg_dash": "⚠️  ffmpeg не найден — DASH (1080p+) невозможен.",
    "warn_fallback_progressive": "   Переключаюсь на progressive (максимум 720p).",
    "err_no_progressive": "❌ Progressive недоступен. Установите ffmpeg.",
    "dl_video_stream": "⬇️  Скачивание видеопотока...",
    "dl_audio_stream": "⬇️  Скачивание аудиопотока...",
    "downloaded": "⬇️  Скачано: {path}",
    "err_tmp_corrupt": "❌ Временный файл повреждён или пуст: {path}",
    "merging": "🔗 Склейка видео и аудио...",
    "merge_cmd": "🔗 Склейка ffmpeg: {cmd}",
    "err_ffmpeg_code": "❌ ffmpeg вернул код {code}",
    "stderr_tail": "   stderr: {stderr}",
    "err_output_missing": "❌ Итоговый файл отсутствует или подозрительно мал.",
    "err_no_audio_track_out": "❌ В итоговом файле НЕ обнаружена аудиодорожка.",
    "warn_merge_failed": "⚠️  Склейка не удалась. Пробую fallback: progressive.",
    "ok_saved_fallback": "✅ Сохранено (fallback): {path}",

    # ---------- mp3 ----------
    "converting_mp3": "🎵 Конвертация в mp3...",
    "ok_audio_saved": "✅ Аудио сохранено: {path}",
    "warn_mp3_failed": "⚠️  Не удалось конвертировать в mp3, оставляю исходный файл",
    "err_mp3_convert": "❌ Ошибка конвертации в mp3: {stderr}",
    "extra_mp3": "🎵 Дополнительно сохраняю mp3-дорожку...",
    "ok_mp3_saved": "✅ mp3 сохранён: {path}",
    "warn_mp3_kept_source": "⚠️  mp3 не сконвертирован, оставлен исходный: {path}",

    # ---------- Result ----------
    "ok_video_saved": "✅ Видео сохранено: {path}",
    "err_download": "❌ Ошибка при скачивании: {error}",
    "ok_log_entry": "📝 Запись добавлена в {txt} и {html}",

    # ---------- Transcript ----------
    "info_no_captions": "ℹ️  Субтитры/транскрипция недоступны.",
    "info_available_subs": "📄 Доступные субтитры: {codes}",
    "info_transcript_lang": "📄 Язык транскрипции: {code}",
    "ok_transcript": "✅ Транскрипция: {path}",
    "warn_transcript_error": "⚠️  Ошибка транскрипции: {error}",
    "tr_title": "# Транскрипция: {title}",
    "tr_author": "# Автор: {author}",
    "tr_lang": "# Язык: {lang}",
    "tr_source": "# Источник: {url}",

    # ---------- HTML log ----------
    "html_title": "Журнал скачанных видео",
    "html_total": "Всего записей: {count}",
    "html_empty": "Пока нет записей",
    "html_col_date": "Дата",
    "html_col_type": "Тип",
    "html_col_title": "Название",
    "html_col_author": "Автор",
    "html_col_quality": "Качество",
    "html_col_audio_lang": "Язык аудио",
    "html_col_duration": "Длительность",
    "html_col_size": "Размер",
    "html_col_audio_file": "Аудио-файл",

    # ---------- Очередь ожидания ----------
    "queue_added": "📥 Видео сейчас недоступно — добавлено в очередь ожидания.",
    "queue_hint": "   Проверить: --check-queue; следить: --watch; список: --queue-list.",
    "queue_already": "ℹ️  Это видео уже стоит в очереди ожидания.",
    "queue_count": "⏳ В очереди ожидания: {count} — проверяю…",
    "queue_checking": "⌛ Проверяю очередь ожидания…",
    "queue_empty": "✅ Очередь ожидания пуста.",
    "queue_resolved": "🎉 Видео стало доступно — скачиваю: {title}",
    "queue_still_unavailable": "   • всё ещё недоступно: {url} ({reason})",
    "queue_watching": "👀 Слежу за очередью ожидания: проверка каждые {minutes} мин (Ctrl+C — выход).",
    "queue_done_watching": "✅ Очередь пуста — слежение завершено.",
    "queue_watch_stopped": "👋 Слежение остановлено.",
    "queue_list_header": "⏳ Очередь ожидания:",
    "queue_list_line": "   • [{quality}] {url} — добавлено {added}; причина: {reason}",
    "queue_removed": "🗑 Убрано из очереди: {url}",
    "queue_not_found": "ℹ️  Этой ссылки нет в очереди: {url}",

    # ---------- Web server ----------
    "srv_url_missing": "URL не указан",
    "srv_bad_quality": "Неверное качество",
    "srv_ui_missing": "web_ui.html не найден рядом с web_server.py",
    "srv_open_browser": "🌐 Открой в браузере: {url}",
    "srv_task_starting": "Запуск…",
    "srv_task_done": "Готово",
    "srv_task_failed": "Скачивание не удалось",
    "srv_bad_abitrate": "Неверный битрейт mp3",

    # ---------- Web UI ----------
    "web_app_title": "🎬 YouTube Downloader",
    "web_subtitle": "Видео, аудио и транскрипции — прямо из браузера",
    "web_lang": "🌐 Язык",
    "web_url_label": "Ссылка на видео",
    "web_url_placeholder": "https://www.youtube.com/watch?v=...",
    "web_quality_label": "Качество",
    "web_q_max": "Максимальное (1080p+ DASH)",
    "web_q_medium": "Среднее",
    "web_lang_audio": "Язык аудио / транскрипции",
    "web_q_audio": "Только аудио (mp3)",
    "web_q_text": "Только текст (транскрипция)",
    "web_extra_label": "Дополнительно",
    "web_save_mp3": "Сохранить mp3 рядом с mp4",
    "web_abitrate_label": "Битрейт mp3 (для аудио)",
    "web_btn_info": "🔍 Получить информацию",
    "web_btn_download": "⬇️ Скачать",
    "web_btn_loading": '<span class="spinner"></span>Загрузка…',
    "web_info_title": "Информация о видео",
    "web_author": "Автор",
    "web_duration": "Длительность",
    "web_id": "ID",
    "web_status": "Статус",
    "web_resolutions": "Доступные разрешения",
    "web_captions_yes": "  •  есть субтитры",
    "web_captions_no": "  •  субтитров нет",
    "web_badge_new": "Новое",
    "web_lbl_video": "видео",
    "web_lbl_audio": "аудио",
    "web_lbl_transcript": "текст",
    "web_progress_title": "Прогресс скачивания",
    "web_files_title": "📁 Скачанные файлы",
    "web_log_title": "📊 Журнал загрузок",
    "web_col_file": "Файл",
    "web_col_size": "Размер",
    "web_col_date": "Дата",
    "web_col_type": "Тип",
    "web_col_title": "Название",
    "web_col_author": "Автор",
    "web_col_quality": "Качество",
    "web_col_audio_file": "Аудио-файл",
    "web_download_link": "скачать",
    "web_empty_files": "Пока нет файлов",
    "web_empty_log": "Пока нет записей",
    "web_err_no_url": "Введите ссылку на видео",
    "web_err_server": "Ошибка сервера",
    "web_err_prefix": "Ошибка: ",
    "web_error_prefix": "❌ Ошибка: ",
    "web_launching": "Запуск…",
    "web_done": "✅ Готово",
    "web_queue_title": "⏳ Ожидание доступности",
    "web_queue_empty": "Очередь пуста",
    "web_queue_col_url": "Ссылка",
    "web_queue_col_quality": "Качество",
    "web_queue_col_added": "Добавлено",
    "web_queue_col_reason": "Причина",
    "web_queue_btn_check": "⌛ Проверить сейчас",
    "web_queue_checked": "Проверено: скачано {resolved}, осталось в очереди {remaining}",
}
