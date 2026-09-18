import os
import re
import sys
import html
import json
import argparse
import subprocess
import shutil
from datetime import datetime
from pytubefix import YouTube
from pytubefix.cli import on_progress

# ---------- Константы ----------
LOG_TXT = "download_log.txt"
LOG_HTML = "download_log.html"

DEFAULT_LANG = "ru"
RU_LANG_CODES = {"ru", "rus", "russian", "русский"}

# Регулярка для парсинга txt-лога
LOG_LINE_RE = re.compile(
    r"^\[(?P<date>[^\]]+)\]\s*"
    r"ID:\s*(?P<id>[^\s|]+)\s*\|\s*"
    r"Тип:\s*(?P<type>.*?)\s*\|\s*"
    r"Название:\s*(?P<title>.*?)\s*\|\s*"
    r"Автор:\s*(?P<author>.*?)\s*\|\s*"
    r"Качество:\s*(?P<quality>.*?)\s*\|\s*"
    r"Язык\s*аудио:\s*(?P<audio_lang>.*?)\s*\|\s*"
    r"Длительность:\s*(?P<duration>.*?)\s*\|\s*"
    r"Размер:\s*(?P<size>.*?)\s*\|\s*"
    r"Транскрипция:\s*(?P<transcript>.*?)\s*\|\s*"
    r"Файл:\s*(?P<file>.*?)\s*\|\s*"
    r"Аудио-файл:\s*(?P<audio_file>.*)$"
)

def print_extended_help():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║  YouTube Downloader — подробная справка                              ║
╠══════════════════════════════════════════════════════════════════════╣
║  РЕЖИМЫ КАЧЕСТВА:                                                    ║
║    max     — максимальное доступное (1080p, 1440p, 4K через DASH)    ║
║    medium  — среднее                                                 ║
║    low     — минимальное (144p–360p)                                 ║
║    audio   — только аудио в mp3 (удобно слушать в пути)              ║
║                                                                      ║
║  ДОПОЛНИТЕЛЬНО:                                                      ║
║    --mp3           дополнительно сохранить mp3-дорожку рядом с mp4   ║
║    --lang ru|en|…  язык аудио и транскрипции (по умолчанию ru)       ║
║    -o DIR          папка для сохранения (по умолчанию downloads)     ║
║                                                                      ║
║  ПРИМЕРЫ:                                                            ║
║    python download.py "https://youtu.be/XXXX" max                    ║
║    python download.py "https://youtu.be/XXXX" audio                  ║
║    python download.py "https://youtu.be/XXXX" medium --lang en       ║
║    python download.py "https://youtu.be/XXXX" max --mp3 -o video     ║
║                                                                      ║
║  БЕЗ АРГУМЕНТОВ — интерактивный режим с пошаговыми вопросами.        ║
╚══════════════════════════════════════════════════════════════════════╝
""")

# ---------- Проверка ffmpeg / ffprobe ----------

def check_ffmpeg() -> bool:
    return shutil.which("ffmpeg") is not None


def check_ffprobe() -> bool:
    return shutil.which("ffprobe") is not None


def has_audio_stream(path: str) -> bool:
    """Проверяет наличие аудиодорожки в файле через ffprobe."""
    if not check_ffprobe():
        # Без ffprobe не можем проверить — считаем, что всё ок
        return True
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error",
             "-select_streams", "a",
             "-show_entries", "stream=codec_type",
             "-of", "csv=p=0", path],
            capture_output=True, text=True, timeout=30,
        )
        return "audio" in result.stdout
    except Exception:
        return False


# ---------- Логирование ----------

def load_downloaded_ids(log_path=LOG_TXT):
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
    line = (
        f"[{entry['date']}] ID: {entry['id']} | "
        f"Тип: {entry['type']} | "
        f"Название: {entry['title']} | "
        f"Автор: {entry['author']} | "
        f"Качество: {entry['quality']} | "
        f"Язык аудио: {entry['audio_lang']} | "
        f"Длительность: {entry['duration']} | "
        f"Размер: {entry['size']} | "
        f"Транскрипция: {entry['transcript']} | "
        f"Файл: {entry['file']} | "
        f"Аудио-файл: {entry['audio_file']}\n"
    )
    with open(LOG_TXT, "a", encoding="utf-8") as f:
        f.write(line)


def regenerate_html_log(entries):
    if not entries:
        rows = ('      <tr><td colspan="10" style="text-align:center;color:#888;">'
                'Пока нет записей</td></tr>')
    else:
        rows = "\n".join(
            f"""      <tr>
        <td>{html.escape(e['date'])}</td>
        <td>{html.escape(e['id'])}</td>
        <td>{html.escape(e['type'])}</td>
        <td><a href="https://youtu.be/{html.escape(e['id'])}" target="_blank">{html.escape(e['title'])}</a></td>
        <td>{html.escape(e['author'])}</td>
        <td>{html.escape(e['quality'])}</td>
        <td>{html.escape(e['audio_lang'])}</td>
        <td>{html.escape(e['duration'])}</td>
        <td>{html.escape(e['size'])}</td>
        <td>{html.escape(e['audio_file'])}</td>
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
             box-shadow: 0 2px 6px rgba(0,0,0,0.1); font-size: 14px; }}
    th, td {{ border: 1px solid #ddd; padding: 6px 10px; text-align: left; }}
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
        <th>Тип</th>
        <th>Название</th>
        <th>Автор</th>
        <th>Качество</th>
        <th>Язык аудио</th>
        <th>Длительность</th>
        <th>Размер</th>
        <th>Аудио-файл</th>
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


def write_log_entry(video_id, entry_type, title, author, quality, audio_lang,
                    duration, size_mb, transcript_path, filepath, audio_file):
    entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id": video_id,
        "type": entry_type,
        "title": title,
        "author": author,
        "quality": quality,
        "audio_lang": audio_lang,
        "duration": duration,
        "size": f"{size_mb:.2f} MB",
        "transcript": transcript_path or "—",
        "file": filepath,
        "audio_file": audio_file or "—",
    }
    append_txt_log(entry)
    regenerate_html_log(parse_log_entries())


# ---------- Утилиты ----------

def format_duration(seconds: int) -> str:
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def safe_filename(name: str, max_len: int = 120) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    return name[:max_len].strip()


# ---------- Склейка видео + аудио ----------

def merge_video_audio(video_path: str, audio_path: str, output_path: str) -> bool:
    """
    Склеивает видео и аудио в MP4. Аудио ПЕРЕКОДИРУЕТСЯ в AAC —
    это устраняет проблему пропавшего звука при -c copy.
    Возвращает True при успехе.
    """
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",           # ← ключевое: не copy, а перекодирование
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        output_path,
    ]
    print("🔗 Склейка ffmpeg:", " ".join(cmd))
    result = subprocess.run(
        cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
    )
    if result.returncode != 0:
        print(f"❌ ffmpeg вернул код {result.returncode}")
        print(f"   stderr: {result.stderr[-800:]}")
        return False

    if not os.path.exists(output_path) or os.path.getsize(output_path) < 1024:
        print("❌ Итоговый файл отсутствует или подозрительно мал.")
        return False

    if not has_audio_stream(output_path):
        print("❌ В итоговом файле НЕ обнаружена аудиодорожка.")
        return False

    return True


def convert_to_mp3(source_path: str, mp3_path: str, bitrate: str = "192k") -> bool:
    """Конвертирует аудиофайл в mp3."""
    if not check_ffmpeg():
        return False
    cmd = [
        "ffmpeg", "-y",
        "-i", source_path,
        "-vn",
        "-c:a", "libmp3lame",
        "-b:a", bitrate,
        mp3_path,
    ]
    result = subprocess.run(
        cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
    )
    if result.returncode != 0:
        print(f"❌ Ошибка конвертации в mp3: {result.stderr[-400:]}")
        return False
    return os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 1024


# ---------- Транскрипция ----------

def download_transcript(yt, output_dir: str, preferred_lang: str = DEFAULT_LANG):
    if not yt.captions:
        print("ℹ️  Субтитры/транскрипция недоступны.")
        return None

    available = {c.code: c for c in yt.captions}
    print(f"📄 Доступные субтитры: {', '.join(available.keys())}")

    chosen = None
    for code, caption in available.items():
        if code.lower().startswith(preferred_lang.lower()):
            chosen = caption
            break
    if chosen is None and preferred_lang != "ru":
        for code, caption in available.items():
            if code.lower().startswith("ru"):
                chosen = caption
                break
    if chosen is None:
        for code, caption in available.items():
            if code.lower().startswith("en"):
                chosen = caption
                break
    if chosen is None:
        chosen = next(iter(available.values()))

    print(f"📄 Язык транскрипции: {chosen.code}")

    base_name = safe_filename(yt.title)
    transcript_path = os.path.join(output_dir, f"{base_name}.transcript.txt")

    try:
        srt_text = chosen.generate_srt_captions()
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
        text = re.sub(r"<[^>]+>", "", "\n".join(clean_lines))

        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(f"# Транскрипция: {yt.title}\n")
            f.write(f"# Автор: {yt.author}\n")
            f.write(f"# Язык: {chosen.code}\n")
            f.write(f"# Источник: https://youtu.be/{yt.video_id}\n")
            f.write("#" + "=" * 60 + "\n\n")
            f.write(text)

        print(f"✅ Транскрипция: {transcript_path}")
        return transcript_path
    except Exception as e:
        print(f"⚠️  Ошибка транскрипции: {e}")
        return None


# ---------- Выбор потоков ----------

def pick_audio_stream(yt, preferred_lang: str = DEFAULT_LANG):
    """Выбирает лучшую аудиодорожку. Аудио берём в m4a (mp4), чтобы точно был AAC."""
    audio_streams = yt.streams.filter(
        only_audio=True, file_extension="mp4"
    ).order_by("abr").desc()

    if not audio_streams:
        audio_streams = yt.streams.filter(only_audio=True).order_by("abr").desc()

    if not audio_streams:
        return None, "unknown"

    print("🎧 Доступные аудиодорожки:")
    for s in audio_streams[:10]:
        track = getattr(s, "audio_track_name", None) or "default"
        default_mark = " (по умолчанию)" if getattr(s, "is_default_audio_track", False) else ""
        print(f"   • {track} | {s.abr} | itag={s.itag} | ext={s.subtype}{default_mark}")

    # 1. Приоритет — русская дорожка
    if preferred_lang == "ru":
        for s in audio_streams:
            name = (getattr(s, "audio_track_name", None) or "").lower()
            if any(code in name for code in RU_LANG_CODES):
                print(f"✅ Выбрана аудиодорожка: {getattr(s, 'audio_track_name', 'default')} ({s.abr})")
                return s, getattr(s, "audio_track_name", "default")

    # 2. Любая дорожка с указанным языком
    for s in audio_streams:
        name = (getattr(s, "audio_track_name", None) or "").lower()
        if preferred_lang.lower() in name:
            print(f"✅ Выбрана аудиодорожка: {getattr(s, 'audio_track_name', 'default')} ({s.abr})")
            return s, getattr(s, "audio_track_name", "default")

    # 3. Дорожка по умолчанию
    for s in audio_streams:
        if getattr(s, "is_default_audio_track", False):
            print(f"ℹ️  Языковая дорожка не найдена, используем default ({s.abr})")
            return s, getattr(s, "audio_track_name", "default")

    # 4. Самая качественная
    s = audio_streams[0]
    print(f"ℹ️  Используем самую качественную дорожку ({s.abr})")
    return s, getattr(s, "audio_track_name", "default")


def pick_video_stream(yt, quality: str):
    """Выбирает видеопоток. Для 'max' — максимальное доступное разрешение (DASH)."""
    all_video = yt.streams.filter(only_video=True, adaptive=True, file_extension="mp4")

    if not all_video:
        # Fallback на progressive (обычно максимум 720p)
        progressive = yt.streams.filter(progressive=True, file_extension="mp4")
        if not progressive:
            return None, False
        sp = sorted(progressive,
                    key=lambda s: int(s.resolution.replace("p", "")) if s.resolution else 0)
        return {"max": sp[-1], "medium": sp[len(sp) // 2], "low": sp[0]}.get(quality.lower()), False

    sv = sorted(all_video,
                key=lambda s: int(s.resolution.replace("p", "")) if s.resolution else 0)
    if quality.lower() == "max":
        return sv[-1], True
    if quality.lower() == "medium":
        return sv[len(sv) // 2], True
    if quality.lower() == "low":
        return sv[0], True
    return None, False


# ---------- Режим «только аудио» ----------

def download_audio_only(yt, output_path, preferred_lang, as_mp3=True):
    """Скачивает только аудио. Если as_mp3 и есть ffmpeg — конвертирует в mp3."""
    selected_audio, audio_lang_name = pick_audio_stream(yt, preferred_lang)
    if selected_audio is None:
        print("❌ Не удалось выбрать аудиодорожку")
        return None, None

    print(f"\n🎧 Аудио: {audio_lang_name} ({selected_audio.abr})")

    # Скачиваем исходное аудио во временный файл
    tmp_name = f"_tmp_a_{yt.video_id}.{selected_audio.subtype}"
    tmp_path = selected_audio.download(output_path=output_path, filename=tmp_name)
    print(f"⬇️  Скачано: {tmp_path}")

    if as_mp3 and check_ffmpeg():
        final_name = safe_filename(yt.title) + ".mp3"
        final_path = os.path.join(output_path, final_name)
        print("🎵 Конвертация в mp3...")
        if convert_to_mp3(tmp_path, final_path):
            os.remove(tmp_path)
            print(f"✅ Аудио сохранено: {final_path}")
            return final_path, audio_lang_name
        else:
            print("⚠️  Не удалось конвертировать в mp3, оставляю исходный файл")
            return tmp_path, audio_lang_name
    else:
        print(f"✅ Аудио сохранено: {tmp_path}")
        return tmp_path, audio_lang_name


# ---------- Основной сценарий ----------

def download_video(url, quality, output_path="downloads",
                   lang=DEFAULT_LANG, save_mp3=False):
    """
    Качество: 'max' / 'medium' / 'low' / 'audio'.
    save_mp3: если True — дополнительно сохраняет mp3-дорожку рядом с видео.
    """
    os.makedirs(output_path, exist_ok=True)

    downloaded_ids = load_downloaded_ids()
    if downloaded_ids:
        print(f"ℹ️  В журнале уже {len(downloaded_ids)} записей.")

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
    except Exception as e:
        print(f"❌ Ошибка получения видео: {e}")
        return

    if yt.video_id in downloaded_ids:
        print(f"\n⚠️  Уже скачано ранее. Пропускаем.")
        print(f"   ID: {yt.video_id}")
        print(f"   Название: {yt.title}")
        return

    print(f"\n🎬 Название: {yt.title}")
    print(f"👤 Автор: {yt.author}")
    print(f"⏱  Длительность: {format_duration(yt.length)}")
    print(f"🆔 ID: {yt.video_id}\n")

    # ====== РЕЖИМ «ТОЛЬКО АУДИО» ======
    if quality.lower() == "audio":
        audio_path, audio_lang_name = download_audio_only(
            yt, output_path, preferred_lang=lang, as_mp3=True,
        )
        if audio_path is None:
            return

        transcript_path = download_transcript(yt, output_path, preferred_lang=lang)
        size_mb = os.path.getsize(audio_path) / (1024 * 1024)

        write_log_entry(
            video_id=yt.video_id,
            entry_type="audio",
            title=yt.title,
            author=yt.author,
            quality="audio/mp3",
            audio_lang=audio_lang_name,
            duration=format_duration(yt.length),
            size_mb=size_mb,
            transcript_path=os.path.abspath(transcript_path) if transcript_path else None,
            filepath=os.path.abspath(audio_path),
            audio_file=os.path.abspath(audio_path),
        )
        print(f"📝 Запись добавлена в {LOG_TXT} и {LOG_HTML}")
        return

    # ====== РЕЖИМ ВИДЕО ======
    selected_video, is_dash = pick_video_stream(yt, quality)
    if selected_video is None:
        print("❌ Не удалось найти подходящий видеопоток")
        return

    selected_audio = None
    audio_lang_name = "встроенная"
    if is_dash:
        selected_audio, audio_lang_name = pick_audio_stream(yt, preferred_lang=lang)

    # Если нужно склеивать, но нет ffmpeg — переключаемся на progressive
    needs_merge = is_dash and selected_audio is not None
    if needs_merge and not check_ffmpeg():
        print("⚠️  ffmpeg не найден — DASH (1080p+) невозможен.")
        print("   Переключаюсь на progressive (максимум 720p).")
        fallback = yt.streams.filter(progressive=True, file_extension="mp4")
        if not fallback:
            print("❌ Progressive недоступен. Установите ffmpeg.")
            return
        sp = sorted(fallback,
                    key=lambda s: int(s.resolution.replace("p", "")) if s.resolution else 0)
        selected_video = {"max": sp[-1], "medium": sp[len(sp) // 2],
                          "low": sp[0]}.get(quality.lower())
        selected_audio = None
        needs_merge = False
        audio_lang_name = "встроенная"

    print(f"\n🎞  Видео: {selected_video.resolution} "
          f"({'DASH' if selected_video.is_adaptive else 'progressive'})")
    if selected_audio:
        print(f"🎧 Аудио: {audio_lang_name} ({selected_audio.abr})")
    print(f"🔧 Склейка: {'да' if needs_merge else 'нет'}\n")

    try:
        if needs_merge:
            # Скачиваем видео и аудио во ВРЕМЕННЫЕ файлы, пути берём из download()
            tmp_v_name = f"_tmp_v_{yt.video_id}.{selected_video.subtype}"
            tmp_a_name = f"_tmp_a_{yt.video_id}.{selected_audio.subtype}"

            print("⬇️  Скачивание видеопотока...")
            tmp_video = selected_video.download(output_path=output_path, filename=tmp_v_name)
            print("⬇️  Скачивание аудиопотока...")
            tmp_audio = selected_audio.download(output_path=output_path, filename=tmp_a_name)

            # Проверяем, что оба файла реально есть и не пустые
            for p in (tmp_video, tmp_audio):
                if not os.path.exists(p) or os.path.getsize(p) < 1024:
                    print(f"❌ Временный файл повреждён или пуст: {p}")
                    return

            final_name = safe_filename(yt.title) + ".mp4"
            final_path = os.path.join(output_path, final_name)

            print("🔗 Склейка видео и аудио...")
            if not merge_video_audio(tmp_video, tmp_audio, final_path):
                print("⚠️  Склейка не удалась. Пробую fallback: progressive.")
                # Чистим временные
                for p in (tmp_video, tmp_audio):
                    if os.path.exists(p):
                        os.remove(p)
                # Fallback на progressive
                prog = yt.streams.filter(progressive=True, file_extension="mp4")
                if not prog:
                    print("❌ Progressive недоступен.")
                    return
                sp = sorted(prog,
                            key=lambda s: int(s.resolution.replace("p", "")) if s.resolution else 0)
                fallback_stream = {"max": sp[-1], "medium": sp[len(sp) // 2],
                                   "low": sp[0]}.get(quality.lower())
                filepath = fallback_stream.download(output_path=output_path)
                selected_video = fallback_stream
                audio_lang_name = "встроенная"
                print(f"✅ Сохранено (fallback): {filepath}")
            else:
                filepath = final_path
                # Чистим временные только после успешной склейки
                for p in (tmp_video, tmp_audio):
                    if os.path.exists(p):
                        os.remove(p)
                print(f"\n✅ Видео сохранено: {filepath}")
        else:
            filepath = selected_video.download(output_path=output_path)
            print(f"\n✅ Видео сохранено: {filepath}")

    except Exception as e:
        print(f"\n❌ Ошибка при скачивании: {e}")
        return

    # Транскрипция
    transcript_path = download_transcript(yt, output_path, preferred_lang=lang)

    # Опционально — mp3 рядом с видео
    audio_file_path = None
    if save_mp3:
        print("\n🎵 Дополнительно сохраняю mp3-дорожку...")
        audio_stream, _ = pick_audio_stream(yt, preferred_lang=lang)
        if audio_stream is not None:
            tmp_a_name = f"_tmp_mp3_{yt.video_id}.{audio_stream.subtype}"
            tmp_a = audio_stream.download(output_path=output_path, filename=tmp_a_name)
            mp3_name = safe_filename(yt.title) + ".mp3"
            mp3_path = os.path.join(output_path, mp3_name)
            if check_ffmpeg() and convert_to_mp3(tmp_a, mp3_path):
                if os.path.exists(tmp_a):
                    os.remove(tmp_a)
                audio_file_path = os.path.abspath(mp3_path)
                print(f"✅ mp3 сохранён: {mp3_path}")
            else:
                audio_file_path = os.path.abspath(tmp_a)
                print(f"⚠️  mp3 не сконвертирован, оставлен исходный: {tmp_a}")

    # Размер основного файла
    try:
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
    except OSError:
        size_mb = 0.0

    write_log_entry(
        video_id=yt.video_id,
        entry_type="video",
        title=yt.title,
        author=yt.author,
        quality=selected_video.resolution or "unknown",
        audio_lang=audio_lang_name,
        duration=format_duration(yt.length),
        size_mb=size_mb,
        transcript_path=os.path.abspath(transcript_path) if transcript_path else None,
        filepath=os.path.abspath(filepath),
        audio_file=audio_file_path,
    )
    print(f"📝 Запись добавлена в {LOG_TXT} и {LOG_HTML}")


# ---------- CLI ----------

def main():
    parser = argparse.ArgumentParser(
        prog="download.py",
        description="Скачивание видео, аудио и транскрипций с YouTube.",
        add_help=True,
    )
    parser.add_argument("url", nargs="?", help="Ссылка на YouTube видео")
    parser.add_argument(
        "quality", nargs="?",
        choices=["max", "medium", "low", "audio"],
        help="Качество: max / medium / low / audio",
    )
    parser.add_argument("-l", "--lang", default=DEFAULT_LANG,
                        help=f"Язык аудио/транскрипции (по умолчанию {DEFAULT_LANG})")
    parser.add_argument("--mp3", action="store_true",
                        help="Дополнительно сохранить mp3-дорожку")
    parser.add_argument("-o", "--output", default="downloads",
                        help="Папка для сохранения (по умолчанию downloads)")

    args = parser.parse_args()

    # Запуск без аргументов — показываем справку
    if args.url is None:
        parser.print_help()
        print_extended_help()
        return

    # Если URL есть, но качество не указано — интерактивный выбор
    if args.quality is None:
        print("\nВыберите качество:")
        print("  1 — максимальное (1080p+ через DASH)")
        print("  2 — среднее")
        print("  3 — низкое")
        print("  4 — только аудио (mp3)")
        choice = input("Номер (1/2/3/4) [1]: ").strip() or "1"
        quality = {"1": "max", "2": "medium", "3": "low", "4": "audio"}.get(choice, "max")
    else:
        quality = args.quality

    # Если mp3 не указан явно и это не режим audio — спросим (только в интерактиве)
    save_mp3 = args.mp3
    if quality != "audio" and not args.mp3 and args.quality is None:
        ans = input("Сохранить также mp3-дорожку? (y/N): ").strip().lower()
        save_mp3 = ans in ("y", "yes", "д", "да")

    download_video(args.url, quality, output_path=args.output,
                   lang=args.lang, save_mp3=save_mp3)


if __name__ == "__main__":
    main()


