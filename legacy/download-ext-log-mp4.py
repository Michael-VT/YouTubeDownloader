import os
import re
import sys
import html
import subprocess
import shutil
from datetime import datetime
from pytubefix import YouTube
from pytubefix.cli import on_progress

# ---------- Константы ----------
LOG_TXT = "download_log.txt"
LOG_HTML = "download_log.html"

# Язык по умолчанию для аудио и транскрипции
DEFAULT_LANG = "ru"
# Коды языков для поиска русской аудиодорожки
RU_LANG_CODES = {"ru", "rus", "russian", "русский"}

# Регулярка для парсинга txt-лога (обновлена: добавлены поля audio_lang и transcript)
LOG_LINE_RE = re.compile(
    r"^\[(?P<date>[^\]]+)\]\s*"
    r"ID:\s*(?P<id>[^\s|]+)\s*\|\s*"
    r"Название:\s*(?P<title>.*?)\s*\|\s*"
    r"Автор:\s*(?P<author>.*?)\s*\|\s*"
    r"Качество:\s*(?P<quality>.*?)\s*\|\s*"
    r"Язык\s*аудио:\s*(?P<audio_lang>.*?)\s*\|\s*"
    r"Длительность:\s*(?P<duration>.*?)\s*\|\s*"
    r"Размер:\s*(?P<size>.*?)\s*\|\s*"
    r"Транскрипция:\s*(?P<transcript>.*?)\s*\|\s*"
    r"Файл:\s*(?P<file>.*)$"
)


# ---------- Проверка ffmpeg ----------

def check_ffmpeg() -> bool:
    """Проверяет наличие ffmpeg в PATH."""
    return shutil.which("ffmpeg") is not None


# ---------- Логирование ----------

def load_downloaded_ids(log_path=LOG_TXT):
    """Возвращает множество ID уже скачанных видео."""
    if not os.path.exists(log_path):
        return set()
    ids = set()
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            m = LOG_LINE_RE.match(line.strip())
            if m:
                ids.add(m.group("id"))
    return ids


def parse_log_entries(log_path=LOG_TXT):
    """Парсит txt-лог в список словарей для генерации HTML."""
    if not os.path.exists(log_path):
        return []
    entries = []
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            m = LOG_LINE_RE.match(line.strip())
            if m:
                entries.append(m.groupdict())
    return entries


def append_txt_log(entry):
    """Добавляет одну запись в текстовый лог."""
    line = (
        f"[{entry['date']}] ID: {entry['id']} | "
        f"Название: {entry['title']} | "
        f"Автор: {entry['author']} | "
        f"Качество: {entry['quality']} | "
        f"Язык аудио: {entry['audio_lang']} | "
        f"Длительность: {entry['duration']} | "
        f"Размер: {entry['size']} | "
        f"Транскрипция: {entry['transcript']} | "
        f"Файл: {entry['file']}\n"
    )
    with open(LOG_TXT, "a", encoding="utf-8") as f:
        f.write(line)


def regenerate_html_log(entries):
    """Полностью пересобирает HTML-лог из списка записей."""
    if not entries:
        rows = '      <tr><td colspan="9" style="text-align:center;color:#888;">Пока нет записей</td></tr>'
    else:
        rows = "\n".join(
            f"""      <tr>
        <td>{html.escape(e['date'])}</td>
        <td>{html.escape(e['id'])}</td>
        <td><a href="https://youtu.be/{html.escape(e['id'])}" target="_blank">{html.escape(e['title'])}</a></td>
        <td>{html.escape(e['author'])}</td>
        <td>{html.escape(e['quality'])}</td>
        <td>{html.escape(e['audio_lang'])}</td>
        <td>{html.escape(e['duration'])}</td>
        <td>{html.escape(e['size'])}</td>
        <td>{html.escape(e['transcript'])}</td>
      </tr>"""
            for e in entries
        )

    content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Журнал скачанных видео</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }}
    h1 {{ color: #333; }}
    .count {{ color: #666; margin-bottom: 15px; }}
    table {{ border-collapse: collapse; width: 100%; background: #fff;
             box-shadow: 0 2px 6px rgba(0,0,0,0.1); }}
    th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
    th {{ background: #4a90e2; color: #fff; }}
    tr:nth-child(even) {{ background: #f9f9f9; }}
    tr:hover {{ background: #eaf3ff; }}
    a {{ color: #1a0dab; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <h1>Журнал скачанных видео</h1>
  <p class="count">Всего записей: {len(entries)}</p>
  <table>
    <thead>
      <tr>
        <th>Дата</th>
        <th>ID</th>
        <th>Название</th>
        <th>Автор</th>
        <th>Качество</th>
        <th>Язык аудио</th>
        <th>Длительность</th>
        <th>Размер</th>
        <th>Транскрипция</th>
      </tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
</body>
</html>
"""
    with open(LOG_HTML, "w", encoding="utf-8") as f:
        f.write(content)


def write_log_entry(video_id, title, author, quality, audio_lang,
                    duration, size_mb, transcript_path, filepath):
    """Записывает инфу о скачанном видео и в .txt, и в .html."""
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id": video_id,
        "title": title,
        "author": author,
        "quality": quality,
        "audio_lang": audio_lang,
        "duration": duration,
        "size": f"{size_mb:.2f} MB",
        "transcript": transcript_path or "—",
        "file": filepath,
    }
    append_txt_log(entry)
    all_entries = parse_log_entries()
    regenerate_html_log(all_entries)


# ---------- Утилиты ----------

def format_duration(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def safe_filename(name: str, max_len: int = 120) -> str:
    """Убирает из имени файла запрещённые символы."""
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    return name[:max_len].strip()


# ---------- Транскрипция ----------

def download_transcript(yt, output_dir: str, preferred_lang: str = DEFAULT_LANG):
    """
    Скачивает текст видео (субтитры) в .txt-файл.
    Приоритет — preferred_lang (по умолчанию 'ru').
    Возвращает путь к файлу или None.
    """
    if not yt.captions:
        print("ℹ️  Субтитры/транскрипция для этого видео недоступны.")
        return None

    available = {c.code: c for c in yt.captions}
    print(f"📄 Доступные языки субтитров: {', '.join(available.keys())}")

    chosen = None

    # 1. Ищем точное совпадение с предпочитаемым языком
    for code, caption in available.items():
        if code.lower().startswith(preferred_lang.lower()):
            chosen = caption
            break

    # 2. Fallback: русский (если preferred не ru)
    if chosen is None and preferred_lang != "ru":
        for code, caption in available.items():
            if code.lower().startswith("ru"):
                chosen = caption
                break

    # 3. Fallback: английский
    if chosen is None:
        for code, caption in available.items():
            if code.lower().startswith("en"):
                chosen = caption
                break

    # 4. Fallback: первый доступный
    if chosen is None:
        chosen = next(iter(available.values()))

    print(f"📄 Выбран язык транскрипции: {chosen.code}")

    base_name = safe_filename(yt.title)
    transcript_path = os.path.join(output_dir, f"{base_name}.transcript.txt")

    try:
        # generate_srt_captions() возвращает SRT — очищаем от таймкодов и номеров
        srt_text = chosen.generate_srt_captions()
        # Убираем блоки таймкодов (например: "1\n00:00:10,200 --> 00:00:11,140")
        clean_lines = []
        for line in srt_text.splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            if re.match(r"^\d+$", stripped):
                continue
            if re.match(r"^\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->", stripped):
                continue
            clean_lines.append(stripped)

        # Дополнительно чистим HTML-теги и склеиваем
        text = "\n".join(clean_lines)
        text = re.sub(r"<[^>]+>", "", text)

        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(f"# Транскрипция: {yt.title}\n")
            f.write(f"# Автор: {yt.author}\n")
            f.write(f"# Язык: {chosen.code}\n")
            f.write(f"# Источник: https://youtu.be/{yt.video_id}\n")
            f.write("#" + "=" * 60 + "\n\n")
            f.write(text)

        print(f"✅ Транскрипция сохранена: {transcript_path}")
        return transcript_path

    except Exception as e:
        print(f"⚠️  Не удалось сохранить транскрипцию: {e}")
        return None


# ---------- Выбор аудиодорожки ----------

def pick_audio_stream(yt, preferred_lang: str = DEFAULT_LANG):
    """
    Выбирает аудиодорожку с приоритетом preferred_lang (по умолчанию 'ru').
    Возвращает объект Stream или None.
    """
    # Все адаптивные аудиопотоки (m4a для совместимости с mp4-видео)
    audio_streams = yt.streams.filter(
        only_audio=True, adaptive=True, file_extension="mp4"
    ).order_by("abr").desc()

    if not audio_streams:
        # Fallback на любой аудиопоток
        audio_streams = yt.streams.filter(only_audio=True).order_by("abr").desc()

    if not audio_streams:
        return None, "unknown"

    # Выводим доступные дорожки для информации
    print("🎧 Доступные аудиодорожки:")
    for s in audio_streams:
        track_name = getattr(s, "audio_track_name", None) or "default"
        default_mark = " (по умолчанию)" if getattr(s, "is_default_audio_track", False) else ""
        print(f"   • {track_name} | {s.abr} | itag={s.itag}{default_mark}")

    # 1. Ищем дорожку, соответствующую preferred_lang
    for s in audio_streams:
        track_name = (getattr(s, "audio_track_name", None) or "").lower()
        if any(code in track_name for code in RU_LANG_CODES if preferred_lang == "ru"):
            print(f"✅ Выбрана аудиодорожка: {getattr(s, 'audio_track_name', 'default')} ({s.abr})")
            return s, getattr(s, "audio_track_name", "default")

    # 2. Ищем любую дорожку с кодом языка
    for s in audio_streams:
        track_name = (getattr(s, "audio_track_name", None) or "").lower()
        if preferred_lang.lower() in track_name:
            print(f"✅ Выбрана аудиодорожка: {getattr(s, 'audio_track_name', 'default')} ({s.abr})")
            return s, getattr(s, "audio_track_name", "default")

    # 3. Fallback: дорожка по умолчанию или самая качественная
    for s in audio_streams:
        if getattr(s, "is_default_audio_track", False):
            print(f"ℹ️  Русская дорожка не найдена, используется дорожка по умолчанию ({s.abr})")
            return s, getattr(s, "audio_track_name", "default")

    # 4. Fallback: самая качественная
    s = audio_streams[0]
    print(f"ℹ️  Выбрана самая качественная доступная дорожка ({s.abr})")
    return s, getattr(s, "audio_track_name", "default")


# ---------- Выбор видеопотока ----------

def pick_video_stream(yt, quality: str):
    """
    Выбирает видеопоток по уровню качества.
    Для 'max' — DASH-поток максимального разрешения (1080p+).
    Возвращает объект Stream и флаг is_dash.
    """
    all_video_streams = yt.streams.filter(
        only_video=True, adaptive=True, file_extension="mp4"
    )

    if not all_video_streams:
        # Fallback на progressive (максимум 720p)
        progressive = yt.streams.filter(progressive=True, file_extension="mp4")
        if not progressive:
            return None, False
        sorted_p = sorted(
            progressive,
            key=lambda s: int(s.resolution.replace("p", "")) if s.resolution else 0,
        )
        quality_map = {
            "max": sorted_p[-1],
            "medium": sorted_p[len(sorted_p) // 2],
            "low": sorted_p[0],
        }
        return quality_map.get(quality.lower()), False

    sorted_streams = sorted(
        all_video_streams,
        key=lambda s: int(s.resolution.replace("p", "")) if s.resolution else 0,
    )

    if quality.lower() == "max":
        return sorted_streams[-1], True
    elif quality.lower() == "medium":
        return sorted_streams[len(sorted_streams) // 2], True
    elif quality.lower() == "low":
        return sorted_streams[0], True
    else:
        return None, False


# ---------- Основная логика ----------

def download_video(url: str, quality: str, output_path: str = "downloads",
                   lang: str = DEFAULT_LANG):
    """
    Скачивает видео с YouTube в выбранном качестве с логированием,
    проверкой дубликатов, выбором аудиодорожки и сохранением транскрипции.
    """
    os.makedirs(output_path, exist_ok=True)

    downloaded_ids = load_downloaded_ids()
    if downloaded_ids:
        print(f"ℹ️  В журнале уже {len(downloaded_ids)} скачанных видео.")

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
    except Exception as e:
        print(f"❌ Ошибка при получении видео: {e}")
        return

    if yt.video_id in downloaded_ids:
        print(f"\n⚠️  Это видео уже было скачано ранее. Пропускаем.")
        print(f"   ID: {yt.video_id}")
        print(f"   Название: {yt.title}")
        return

    print(f"\n🎬 Название: {yt.title}")
    print(f"👤 Автор: {yt.author}")
    print(f"⏱  Длительность: {format_duration(yt.length)}")
    print(f"🆔 ID: {yt.video_id}\n")

    # --- Выбор видеопотока ---
    selected_video, is_dash = pick_video_stream(yt, quality)
    if selected_video is None:
        print("❌ Не удалось найти подходящий видеопоток")
        return

    # --- Выбор аудиодорожки ---
    selected_audio, audio_lang_name = pick_audio_stream(yt, preferred_lang=lang)

    # --- Определение необходимости склейки ---
    needs_merge = False
    if is_dash or (selected_audio is not None and selected_video.is_adaptive):
        needs_merge = True

    # Если ffmpeg нет, а нужен DASH — предупреждаем и переключаемся на progressive
    if needs_merge and not check_ffmpeg():
        print("⚠️  ffmpeg не найден в PATH! Скачивание 1080p+ невозможно.")
        print("   Переключаюсь на progressive-поток (максимум 720p)...")
        fallback = yt.streams.filter(progressive=True, file_extension="mp4")
        if not fallback:
            print("❌ Progressive-потоки недоступны. Установите ffmpeg и повторите.")
            return
        sorted_p = sorted(
            fallback,
            key=lambda s: int(s.resolution.replace("p", "")) if s.resolution else 0,
        )
        selected_video = sorted_p[-1] if quality == "max" else (
            sorted_p[len(sorted_p) // 2] if quality == "medium" else sorted_p[0]
        )
        selected_audio = None
        needs_merge = False
        audio_lang_name = "встроенная"

    print(f"\n🎞  Видео: {selected_video.resolution} "
          f"({'DASH' if selected_video.is_adaptive else 'progressive'})")
    if selected_audio:
        print(f"🎧 Аудио: {audio_lang_name} ({selected_audio.abr})")
    print(f"🔧 Склейка через ffmpeg: {'да' if needs_merge else 'нет'}\n")

    # --- Скачивание ---
    try:
        if needs_merge and selected_audio is not None:
            # Скачиваем видео и аудио во временные файлы
            tmp_video = os.path.join(output_path, f"_tmp_video_{yt.video_id}.mp4")
            tmp_audio = os.path.join(output_path, f"_tmp_audio_{yt.video_id}.m4a")

            print("⬇️  Скачивание видеопотока...")
            selected_video.download(output_path=output_path, filename=os.path.basename(tmp_video))
            print("⬇️  Скачивание аудиопотока...")
            selected_audio.download(output_path=output_path, filename=os.path.basename(tmp_audio))

            # Итоговое имя файла
            final_name = safe_filename(yt.title) + ".mp4"
            final_path = os.path.join(output_path, final_name)

            print("🔗 Склейка видео и аудио через ffmpeg...")
            ffmpeg_cmd = [
                "ffmpeg", "-y",
                "-i", tmp_video,
                "-i", tmp_audio,
                "-c", "copy",
                "-map", "0:v:0",
                "-map", "1:a:0",
                final_path,
            ]
            result = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
            )

            if result.returncode != 0:
                print(f"❌ Ошибка ffmpeg: {result.stderr[:500]}")
                return

            # Удаляем временные файлы
            for tmp in (tmp_video, tmp_audio):
                if os.path.exists(tmp):
                    os.remove(tmp)

            filepath = final_path
        else:
            # Progressive-поток — качаем как есть
            filepath = selected_video.download(output_path=output_path)

        print(f"\n✅ Видео сохранено: {filepath}")

    except Exception as e:
        print(f"\n❌ Ошибка при скачивании: {e}")
        return

    # --- Транскрипция ---
    transcript_path = download_transcript(yt, output_path, preferred_lang=lang)

    # --- Размер файла ---
    try:
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
    except OSError:
        size_mb = 0.0

    # --- Логирование ---
    write_log_entry(
        video_id=yt.video_id,
        title=yt.title,
        author=yt.author,
        quality=selected_video.resolution or "unknown",
        audio_lang=audio_lang_name,
        duration=format_duration(yt.length),
        size_mb=size_mb,
        transcript_path=os.path.abspath(transcript_path) if transcript_path else None,
        filepath=os.path.abspath(filepath),
    )
    print(f"📝 Запись добавлена в {LOG_TXT} и {LOG_HTML}")


def main():
    # Разбор аргументов командной строки
    # Формат: python script.py <url> <quality> [lang]
    if len(sys.argv) >= 3:
        url = sys.argv[1]
        quality = sys.argv[2]
        lang = sys.argv[3] if len(sys.argv) >= 4 else DEFAULT_LANG
    else:
        url = input("🔗 Введите ссылку на YouTube видео: ").strip()
        print("\nВыберите качество:")
        print("  1 — максимальное (1080p+ через DASH)")
        print("  2 — среднее")
        print("  3 — низкое")
        choice = input("Введите номер (1/2/3) [по умолчанию 1]: ").strip() or "1"
        quality = {"1": "max", "2": "medium", "3": "low"}.get(choice, "max")

        lang_input = input(
            f"\nЯзык аудио/транскрипции [по умолчанию {DEFAULT_LANG}]: "
        ).strip()
        lang = lang_input or DEFAULT_LANG

    download_video(url, quality, lang=lang)


if __name__ == "__main__":
    main()

