import os
import re
import sys
import html
import json
import time
import threading
import argparse
import subprocess
import shutil
from datetime import datetime

from pytubefix import YouTube
from pytubefix.cli import on_progress
from pytubefix.exceptions import RegexMatchError

import i18n
from i18n import t

# ---------- Константы ----------
LOG_TXT = "download_log.txt"
LOG_HTML = "download_log.html"

DEFAULT_LANG = "ru"
RU_LANG_CODES = {"ru", "rus", "russian", "русский"}

# Очередь ожидания недоступных видео и битрейт mp3 по умолчанию
QUEUE_FILE = "pending_queue.json"
DEFAULT_BITRATE = "192k"

# Веб-интерфейс скачивает в потоках: записи журнала и очереди защищаем
# блокировками, чтобы параллельные задачи их не портили
_LOG_LOCK = threading.Lock()
_QUEUE_LOCK = threading.Lock()

# Регулярка для парсинга txt-лога.
# ВАЖНО: формат лога — данные, а не интерфейс. Подписи полей фиксированы
# по-русски и НЕ переводятся, иначе сломается дедупликация «уже скачано».
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
    print(t("extended_help"))


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

def _file_exists(path: str) -> bool:
    """Запись лога актуальна, только пока её файл существует на диске."""
    return bool(path) and path != "—" and os.path.exists(path)


def _audio_key_from_path(path: str) -> str:
    """Битрейт приложенного mp3 виден в имени файла: «title [320k].mp3»."""
    m = re.search(r"\[(\d+k)\]\.mp3?$", os.path.basename(path))
    return f"audio/mp3-{m.group(1)}" if m else "audio/mp3-192k"


def _existing_summary(existing: dict) -> str:
    """Человекочитаемый список того, что уже скачано для видео."""
    def res_num(r):
        try:
            return int(r.rstrip("p") or 0)
        except ValueError:
            return 0

    parts = [t("sum_video", res=r) for r in sorted(existing["video"], key=res_num)]
    parts += [t("sum_audio", value=k.replace("audio/mp3-", "mp3 "))
              for k in sorted(existing["audio"])]
    if existing["transcript"]:
        parts.append(t("sum_transcript"))
    return ", ".join(parts)


def existing_for_video(video_id: str, entries=None) -> dict:
    """
    Что уже скачано для видео, по типам содержимого:
      {'video': {'1080p', …}, 'audio': {'audio/mp3-192k', …},
       'transcript': '<путь>' | None}
    Каждый тип учитывается отдельно: видео в низком качестве не мешает
    скачать максимальное, аудио или текст. Запись считается скачанной,
    только если её файл ещё есть на диске (удалённый файл качается заново).
    """
    if entries is None:
        entries = parse_log_entries()
    res = {"video": set(), "audio": set(), "transcript": None}
    for e in entries:
        if e["id"] != video_id:
            continue
        if e["type"] == "video" and _file_exists(e["file"]):
            res["video"].add(e["quality"])
        elif e["type"] == "audio" and _file_exists(e["file"]):
            # старые записи писались как «audio/mp3» — это был 192k
            q = e["quality"] if e["quality"] != "audio/mp3" else "audio/mp3-192k"
            res["audio"].add(q)
        elif e["type"] == "text" and _file_exists(e["file"]):
            res["transcript"] = res["transcript"] or e["file"]
        # mp3, приложенный к видеозаписи (--mp3)
        if e["type"] == "video" and _file_exists(e["audio_file"]):
            res["audio"].add(_audio_key_from_path(e["audio_file"]))
        # транскрипция, приложенная к записи видео/аудио
        if res["transcript"] is None and _file_exists(e["transcript"]):
            res["transcript"] = e["transcript"]
    return res


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
    # Формат фиксирован (см. комментарий у LOG_LINE_RE) — не переводим.
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
                + html.escape(t("html_empty")) + '</td></tr>')
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
<html lang="{i18n.get_language()}">
<head>
  <meta charset="UTF-8">
  <title>{html.escape(t("html_title"))}</title>
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
  <h1>{html.escape(t("html_title"))}</h1>
  <p class="count">{html.escape(t("html_total", count=len(entries)))}</p>
  <table>
    <thead>
      <tr>
        <th>{html.escape(t("html_col_date"))}</th>
        <th>ID</th>
        <th>{html.escape(t("html_col_type"))}</th>
        <th>{html.escape(t("html_col_title"))}</th>
        <th>{html.escape(t("html_col_author"))}</th>
        <th>{html.escape(t("html_col_quality"))}</th>
        <th>{html.escape(t("html_col_audio_lang"))}</th>
        <th>{html.escape(t("html_col_duration"))}</th>
        <th>{html.escape(t("html_col_size"))}</th>
        <th>{html.escape(t("html_col_audio_file"))}</th>
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
    with _LOG_LOCK:
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


def _mp3_filename(title: str, bitrate: str = DEFAULT_BITRATE) -> str:
    """Имя mp3; нестандартный битрейт виден в имени — файлы не затирают друг друга."""
    suffix = f" [{bitrate}]" if bitrate != DEFAULT_BITRATE else ""
    return safe_filename(title) + suffix + ".mp3"


def _unique_path(path: str, marker: str) -> str:
    """
    Существующие скачивания никогда не затираются: если путь занят,
    новый файл сохраняется рядом — с пометкой качества в имени
    («Название [1080p].mp4») либо с номером, если и оно занято.
    """
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    tagged = marker and f"[{marker}]" not in os.path.basename(base)
    candidates = ([f"{base} [{marker}]{ext}"] if tagged else []) + \
                 [f"{base} {n}{ext}" for n in range(2, 100)]
    for candidate in candidates:
        if not os.path.exists(candidate):
            print(t("info_file_exists", old=os.path.basename(path),
                    new=os.path.basename(candidate)))
            return candidate
    return path


def _video_path(output_path: str, title: str, resolution, ext: str = "mp4") -> str:
    """Путь видеофайла; старые файлы не перезаписываются."""
    path = os.path.join(output_path, safe_filename(title) + "." + ext)
    return _unique_path(path, resolution or "video")


def _mp3_path(output_path: str, title: str, bitrate: str) -> str:
    """Путь mp3; старые файлы не перезаписываются."""
    path = os.path.join(output_path, _mp3_filename(title, bitrate))
    return _unique_path(path, bitrate)

def _res_key(s):
    """Ключ сортировки потоков по разрешению ('720p' -> 720)."""
    return int(s.resolution.replace("p", "")) if s.resolution else 0


def _report(progress, percent, key, **kwargs):
    """Сообщает прогресс подписчику (например, веб-интерфейсу)."""
    if progress is not None:
        progress(percent, t(key, **kwargs))


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
    print(t("merge_cmd", cmd=" ".join(cmd)))
    result = subprocess.run(
        cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
    )
    if result.returncode != 0:
        print(t("err_ffmpeg_code", code=result.returncode))
        print(t("stderr_tail", stderr=result.stderr[-800:]))
        return False

    if not os.path.exists(output_path) or os.path.getsize(output_path) < 1024:
        print(t("err_output_missing"))
        return False

    if not has_audio_stream(output_path):
        print(t("err_no_audio_track_out"))
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
        print(t("err_mp3_convert", stderr=result.stderr[-400:]))
        return False
    return os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 1024


# ---------- Транскрипция ----------

def download_transcript(yt, output_dir: str, preferred_lang: str = DEFAULT_LANG,
                        progress=None):
    if not yt.captions:
        print(t("info_no_captions"))
        return None, None

    available = {c.code: c for c in yt.captions}
    print(t("info_available_subs", codes=", ".join(available.keys())))

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

    print(t("info_transcript_lang", code=chosen.code))

    base_name = safe_filename(yt.title)
    transcript_path = _unique_path(
        os.path.join(output_dir, f"{base_name}.transcript.txt"), chosen.code)

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
            f.write(t("tr_title", title=yt.title) + "\n")
            f.write(t("tr_author", author=yt.author) + "\n")
            f.write(t("tr_lang", lang=chosen.code) + "\n")
            f.write(t("tr_source", url=f"https://youtu.be/{yt.video_id}") + "\n")
            f.write("#" + "=" * 60 + "\n\n")
            f.write(text)

        print(t("ok_transcript", path=transcript_path))
        _report(progress, 90, "ok_transcript", path=transcript_path)
        return transcript_path, chosen.code
    except Exception as e:
        print(t("warn_transcript_error", error=e))
        return None, None


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

    print(t("audio_tracks_available"))
    for s in audio_streams[:10]:
        track = getattr(s, "audio_track_name", None) or "default"
        default_mark = " *" if getattr(s, "is_default_audio_track", False) else ""
        print(t("audio_track_line", track=track, abr=s.abr, itag=s.itag,
                ext=s.subtype, default=default_mark))

    # 1. Приоритет — русская дорожка
    if preferred_lang == "ru":
        for s in audio_streams:
            name = (getattr(s, "audio_track_name", None) or "").lower()
            if any(code in name for code in RU_LANG_CODES):
                print(t("audio_selected",
                        track=getattr(s, "audio_track_name", "default"), abr=s.abr))
                return s, getattr(s, "audio_track_name", "default")

    # 2. Любая дорожка с указанным языком
    for s in audio_streams:
        name = (getattr(s, "audio_track_name", None) or "").lower()
        if preferred_lang.lower() in name:
            print(t("audio_selected",
                    track=getattr(s, "audio_track_name", "default"), abr=s.abr))
            return s, getattr(s, "audio_track_name", "default")

    # 3. Дорожка по умолчанию
    for s in audio_streams:
        if getattr(s, "is_default_audio_track", False):
            print(t("audio_using_default", abr=s.abr))
            return s, getattr(s, "audio_track_name", "default")

    # 4. Самая качественная
    s = audio_streams[0]
    print(t("audio_using_best", abr=s.abr))
    return s, getattr(s, "audio_track_name", "default")


def pick_video_stream(yt, quality: str):
    """Выбирает видеопоток. Для 'max' — максимальное доступное разрешение (DASH)."""
    all_video = yt.streams.filter(only_video=True, adaptive=True, file_extension="mp4")

    if not all_video:
        # Fallback на progressive (обычно максимум 720p)
        progressive = yt.streams.filter(progressive=True, file_extension="mp4")
        if not progressive:
            return None, False
        sp = sorted(progressive, key=_res_key)
        return {"max": sp[-1], "medium": sp[len(sp) // 2], "low": sp[0]}.get(quality.lower()), False

    sv = sorted(all_video, key=_res_key)
    if quality.lower() == "max":
        return sv[-1], True
    if quality.lower() == "medium":
        return sv[len(sv) // 2], True
    if quality.lower() == "low":
        return sv[0], True
    return None, False


# ---------- Режим «только аудио» ----------

def download_audio_only(yt, output_path, preferred_lang, as_mp3=True,
                        bitrate=DEFAULT_BITRATE, progress=None):
    """Скачивает только аудио. При as_mp3 и ffmpeg — mp3 с выбранным битрейтом."""
    selected_audio, audio_lang_name = pick_audio_stream(yt, preferred_lang)
    if selected_audio is None:
        print(t("err_no_audio_stream"))
        return None, None

    print()
    print(t("audio_header", name=audio_lang_name, abr=selected_audio.abr))

    # Скачиваем исходное аудио во временный файл
    tmp_name = f"_tmp_a_{yt.video_id}.{selected_audio.subtype}"
    _report(progress, 30, "dl_audio_stream")
    tmp_path = selected_audio.download(output_path=output_path, filename=tmp_name)
    print(t("downloaded", path=tmp_path))

    if as_mp3 and check_ffmpeg():
        final_path = _mp3_path(output_path, yt.title, bitrate)
        print(t("converting_mp3"))
        _report(progress, 55, "converting_mp3")
        if convert_to_mp3(tmp_path, final_path, bitrate=bitrate):
            os.remove(tmp_path)
            print(t("ok_audio_saved", path=final_path))
            _report(progress, 80, "ok_audio_saved", path=final_path)
            return final_path, audio_lang_name
        else:
            print(t("warn_mp3_failed"))
            return tmp_path, audio_lang_name
    else:
        print(t("ok_audio_saved", path=tmp_path))
        return tmp_path, audio_lang_name


# ---------- Очередь ожидания ----------

def load_queue() -> list:
    """Читает очередь ожидания (недоступные видео)."""
    if not os.path.exists(QUEUE_FILE):
        return []
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def save_queue(items: list) -> None:
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def add_to_queue(url, quality, lang=DEFAULT_LANG, save_mp3=False,
                 abitrate=DEFAULT_BITRATE, reason="") -> bool:
    """Добавляет недоступное видео в очередь. False — если оно уже там."""
    with _QUEUE_LOCK:
        items = load_queue()
        for it in items:
            if it["url"] == url and it["quality"] == quality:
                it["reason"] = reason or it.get("reason", "")
                it["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save_queue(items)
                return False
        items.append({
            "url": url,
            "quality": quality,
            "lang": lang,
            "save_mp3": bool(save_mp3),
            "abitrate": abitrate,
            "reason": reason,
            "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_checked": None,
            "attempts": 0,
        })
        save_queue(items)
        return True


def remove_from_queue(url: str) -> bool:
    with _QUEUE_LOCK:
        items = load_queue()
        rest = [it for it in items if it["url"] != url]
        if len(rest) == len(items):
            return False
        save_queue(rest)
        return True


def check_pending(output_path: str = "downloads", progress=None) -> int:
    """
    Проверяет очередь ожидания: видео, ставшее доступным, скачивается
    с теми же параметрами и убирается из очереди. Возвращает число
    успешно скачанных.
    """
    with _QUEUE_LOCK:
        items = load_queue()
    if not items:
        print(t("queue_empty"))
        return 0

    print(t("queue_checking"))
    resolved_keys = []   # (url, quality) скачанных
    checked = {}         # (url, quality) -> обновления для оставшихся
    for it in items:
        key = (it["url"], it["quality"])
        try:
            yt = YouTube(it["url"], on_progress_callback=on_progress)
            title = yt.title
        except Exception as e:
            checked[key] = {
                "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "attempts": it.get("attempts", 0) + 1,
                "reason": str(e),
            }
            print(t("queue_still_unavailable", url=it["url"], reason=e))
            continue

        print()
        print(t("queue_resolved", title=title))
        if download_video(it["url"], it["quality"], output_path=output_path,
                          lang=it.get("lang", DEFAULT_LANG),
                          save_mp3=it.get("save_mp3", False),
                          abitrate=it.get("abitrate", DEFAULT_BITRATE),
                          progress=progress, yt=yt):
            resolved_keys.append(key)
        else:
            checked[key] = {
                "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "attempts": it.get("attempts", 0) + 1,
                "reason": it.get("reason", ""),
            }

    # Сеть позади: объединяем с текущим состоянием очереди, чтобы не
    # потерять записи, добавленные другими задачами за время проверки
    with _QUEUE_LOCK:
        current = load_queue()
        rest = []
        for it in current:
            key = (it["url"], it["quality"])
            if key in resolved_keys:
                continue
            if key in checked:
                it.update(checked[key])
            rest.append(it)
        save_queue(rest)
    return len(resolved_keys)


def _watch_loop(minutes: float, output_path: str = "downloads"):
    """Периодически проверяет очередь, пока она не опустеет (Ctrl+C — выход)."""
    print(t("queue_watching", minutes=minutes))
    try:
        while True:
            check_pending(output_path=output_path)
            if not load_queue():
                print(t("queue_done_watching"))
                return
            time.sleep(minutes * 60)
    except KeyboardInterrupt:
        print()
        print(t("queue_watch_stopped"))


# ---------- Основной сценарий ----------

def _queue_unavailable(url, quality, lang, save_mp3, abitrate, error) -> bool:
    """Сообщает о недоступном видео и ставит его в очередь ожидания."""
    print(t("err_get_video", error=error))
    if add_to_queue(url, quality, lang, save_mp3, abitrate, reason=str(error)):
        print(t("queue_added"))
        print(t("queue_hint"))
    else:
        print(t("queue_already"))
    return False


def download_video(url, quality, output_path="downloads",
                   lang=DEFAULT_LANG, save_mp3=False, abitrate=DEFAULT_BITRATE,
                   progress=None, yt=None):
    """
    Качество: 'max' / 'medium' / 'low' / 'audio' / 'text'.
    abitrate: битрейт mp3 для режима 'audio' и опции save_mp3.
    save_mp3: если True — дополнительно сохраняет mp3-дорожку рядом с видео.
    progress: опциональный callback(percent, message) для индикации прогресса.
    yt: заранее полученный объект YouTube (передаёт очередь ожидания).
    """
    os.makedirs(output_path, exist_ok=True)

    entries = parse_log_entries()
    downloaded_ids = {e["id"] for e in entries}
    if downloaded_ids:
        print(t("info_log_entries", count=len(downloaded_ids)))

    if yt is None:
        try:
            yt = YouTube(url, on_progress_callback=on_progress)
        except RegexMatchError as e:
            print(t("err_bad_url", error=e))
            return False
        except Exception as e:
            # Ошибка сети/бот-блокировка при получении метаданных
            return _queue_unavailable(url, quality, lang, save_mp3, abitrate, e)

    # pytubefix проверяет доступность лениво — при первом обращении
    # к свойствам, поэтому title/author/length тоже под защитой
    try:
        title, author, length = yt.title, yt.author, yt.length
    except Exception as e:
        # Видео недоступно (приватное, удалено, бот-блокировка…)
        return _queue_unavailable(url, quality, lang, save_mp3, abitrate, e)

    # Что уже скачано для этого видео — каждый тип/качество отдельно
    existing = existing_for_video(yt.video_id, entries)
    if existing["video"] or existing["audio"] or existing["transcript"]:
        print(t("already_summary", items=_existing_summary(existing)))

    print()
    print(t("video_title", title=title))
    print(t("video_author", author=author))
    print(t("video_duration", duration=format_duration(length)))
    print(t("video_id", id=yt.video_id))
    print()
    _report(progress, 10, "video_title", title=title)

    # ====== РЕЖИМ «ТОЛЬКО ТЕКСТ» ======
    if quality.lower() == "text":
        if existing["transcript"]:
            print(t("already_transcript", path=existing["transcript"]))
            return True
        if not yt.captions:
            print(t("err_no_captions_text"))
            return False
        transcript_path, tr_code = download_transcript(yt, output_path,
                                                       preferred_lang=lang,
                                                       progress=progress)
        if transcript_path is None:
            return False
        write_log_entry(
            video_id=yt.video_id,
            entry_type="text",
            title=yt.title,
            author=yt.author,
            quality=f"text/{tr_code}",
            audio_lang="—",
            duration=format_duration(yt.length),
            size_mb=os.path.getsize(transcript_path) / (1024 * 1024),
            transcript_path=os.path.abspath(transcript_path),
            filepath=os.path.abspath(transcript_path),
            audio_file=None,
        )
        print(t("ok_log_entry", txt=LOG_TXT, html=LOG_HTML))
        _report(progress, 100, "ok_log_entry", txt=LOG_TXT, html=LOG_HTML)
        return True

    # ====== РЕЖИМ «ТОЛЬКО АУДИО» ======
    if quality.lower() == "audio":
        audio_key = f"audio/mp3-{abitrate}"
        if audio_key in existing["audio"]:
            print(t("already_audio_quality", bitrate=abitrate))
            return True

        audio_path, audio_lang_name = download_audio_only(
            yt, output_path, preferred_lang=lang, as_mp3=True,
            bitrate=abitrate, progress=progress,
        )
        if audio_path is None:
            return False

        # Транскрипцию в audio-режиме качаем, только если её ещё нет
        transcript_path = None
        if not existing["transcript"]:
            transcript_path, _ = download_transcript(yt, output_path,
                                                     preferred_lang=lang,
                                                     progress=progress)
        size_mb = os.path.getsize(audio_path) / (1024 * 1024)

        write_log_entry(
            video_id=yt.video_id,
            entry_type="audio",
            title=yt.title,
            author=yt.author,
            quality=audio_key,
            audio_lang=audio_lang_name,
            duration=format_duration(yt.length),
            size_mb=size_mb,
            transcript_path=os.path.abspath(transcript_path) if transcript_path else None,
            filepath=os.path.abspath(audio_path),
            audio_file=os.path.abspath(audio_path),
        )
        print(t("ok_log_entry", txt=LOG_TXT, html=LOG_HTML))
        _report(progress, 100, "ok_log_entry", txt=LOG_TXT, html=LOG_HTML)
        return True

    # ====== РЕЖИМ ВИДЕО ======
    selected_video, is_dash = pick_video_stream(yt, quality)
    if selected_video is None:
        print(t("err_no_video_stream"))
        return False

    selected_audio = None
    audio_lang_name = t("audio_lang_embedded")
    if is_dash:
        selected_audio, audio_lang_name = pick_audio_stream(yt, preferred_lang=lang)

    # Если нужно склеивать, но нет ffmpeg — переключаемся на progressive
    needs_merge = is_dash and selected_audio is not None
    if needs_merge and not check_ffmpeg():
        print(t("warn_no_ffmpeg_dash"))
        print(t("warn_fallback_progressive"))
        fallback = yt.streams.filter(progressive=True, file_extension="mp4")
        if not fallback:
            print(t("err_no_progressive"))
            return False
        sp = sorted(fallback, key=_res_key)
        selected_video = {"max": sp[-1], "medium": sp[len(sp) // 2],
                          "low": sp[0]}.get(quality.lower())
        if selected_video is None:
            print(t("err_no_video_stream"))
            return False
        selected_audio = None
        needs_merge = False
        audio_lang_name = t("audio_lang_embedded")

    # Это же разрешение уже скачано — пропускаем (другие качества доступны)
    if (selected_video.resolution or "unknown") in existing["video"]:
        print(t("already_video_quality", res=selected_video.resolution or "unknown"))
        return True

    print()
    print(t("video_stream_info", res=selected_video.resolution,
            mode="DASH" if selected_video.is_adaptive else "progressive"))
    if selected_audio:
        print(t("audio_header", name=audio_lang_name, abr=selected_audio.abr))
    print(t("merge_label", value=t("word_yes") if needs_merge else t("word_no")))
    print()
    _report(progress, 20, "video_stream_info", res=selected_video.resolution,
            mode="DASH" if selected_video.is_adaptive else "progressive")

    try:
        if needs_merge:
            # Скачиваем видео и аудио во ВРЕМЕННЫЕ файлы, пути берём из download()
            tmp_v_name = f"_tmp_v_{yt.video_id}.{selected_video.subtype}"
            tmp_a_name = f"_tmp_a_{yt.video_id}.{selected_audio.subtype}"

            print(t("dl_video_stream"))
            _report(progress, 30, "dl_video_stream")
            tmp_video = selected_video.download(output_path=output_path, filename=tmp_v_name)
            print(t("dl_audio_stream"))
            _report(progress, 50, "dl_audio_stream")
            tmp_audio = selected_audio.download(output_path=output_path, filename=tmp_a_name)

            # Проверяем, что оба файла реально есть и не пустые
            for p in (tmp_video, tmp_audio):
                if not os.path.exists(p) or os.path.getsize(p) < 1024:
                    print(t("err_tmp_corrupt", path=p))
                    return False

            final_path = _video_path(output_path, yt.title, selected_video.resolution)

            print(t("merging"))
            _report(progress, 65, "merging")
            if not merge_video_audio(tmp_video, tmp_audio, final_path):
                print(t("warn_merge_failed"))
                # Чистим временные
                for p in (tmp_video, tmp_audio):
                    if os.path.exists(p):
                        os.remove(p)
                # Fallback на progressive
                prog = yt.streams.filter(progressive=True, file_extension="mp4")
                if not prog:
                    print(t("err_no_progressive"))
                    return False
                sp = sorted(prog, key=_res_key)
                fallback_stream = {"max": sp[-1], "medium": sp[len(sp) // 2],
                                   "low": sp[0]}.get(quality.lower())
                if fallback_stream is None:
                    print(t("err_no_video_stream"))
                    return False
                fb_path = _video_path(output_path, yt.title, fallback_stream.resolution,
                                      fallback_stream.subtype)
                filepath = fallback_stream.download(output_path=output_path,
                                                    filename=os.path.basename(fb_path))
                selected_video = fallback_stream
                audio_lang_name = t("audio_lang_embedded")
                print(t("ok_saved_fallback", path=filepath))
            else:
                filepath = final_path
                # Чистим временные только после успешной склейки
                for p in (tmp_video, tmp_audio):
                    if os.path.exists(p):
                        os.remove(p)
                print()
                print(t("ok_video_saved", path=filepath))
                _report(progress, 80, "ok_video_saved", path=filepath)
        else:
            _report(progress, 30, "dl_video_stream")
            v_path = _video_path(output_path, yt.title, selected_video.resolution,
                                 selected_video.subtype)
            filepath = selected_video.download(output_path=output_path,
                                               filename=os.path.basename(v_path))
            print()
            print(t("ok_video_saved", path=filepath))
            _report(progress, 80, "ok_video_saved", path=filepath)

    except Exception as e:
        print()
        print(t("err_download", error=e))
        return False

    # Транскрипция: качаем, только если её ещё нет
    transcript_path = None
    if existing["transcript"]:
        print(t("info_transcript_exists"))
    else:
        transcript_path, _ = download_transcript(yt, output_path, preferred_lang=lang,
                                                 progress=progress)

    # Опционально — mp3 рядом с видео (не дублируем уже скачанный битрейт)
    audio_file_path = None
    mp3_key = f"audio/mp3-{abitrate}"
    if save_mp3 and mp3_key in existing["audio"]:
        print(t("already_audio_quality", bitrate=abitrate))
    elif save_mp3:
        print()
        print(t("extra_mp3"))
        audio_stream, _ = pick_audio_stream(yt, preferred_lang=lang)
        if audio_stream is not None:
            tmp_a_name = f"_tmp_mp3_{yt.video_id}.{audio_stream.subtype}"
            tmp_a = audio_stream.download(output_path=output_path, filename=tmp_a_name)
            mp3_path = _mp3_path(output_path, yt.title, abitrate)
            if check_ffmpeg() and convert_to_mp3(tmp_a, mp3_path, bitrate=abitrate):
                if os.path.exists(tmp_a):
                    os.remove(tmp_a)
                audio_file_path = os.path.abspath(mp3_path)
                print(t("ok_mp3_saved", path=mp3_path))
                _report(progress, 95, "ok_mp3_saved", path=mp3_path)
            else:
                audio_file_path = os.path.abspath(tmp_a)
                print(t("warn_mp3_kept_source", path=tmp_a))

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
    print(t("ok_log_entry", txt=LOG_TXT, html=LOG_HTML))
    _report(progress, 100, "ok_log_entry", txt=LOG_TXT, html=LOG_HTML)
    return True


# ---------- CLI ----------

def _ui_lang_from_argv(argv):
    """Достаёт --ui-lang/--locale из argv до argparse, чтобы -h тоже был переведён."""
    for i, arg in enumerate(argv):
        if arg in ("--ui-lang", "--locale") and i + 1 < len(argv):
            return argv[i + 1]
        for prefix in ("--ui-lang=", "--locale="):
            if arg.startswith(prefix):
                return arg[len(prefix):]
    return None


def main():
    i18n.set_language(_ui_lang_from_argv(sys.argv[1:]) or i18n.detect_language())

    parser = argparse.ArgumentParser(
        prog="download.py",
        description=t("app_desc"),
        add_help=True,
    )
    parser.add_argument("url", nargs="?", help=t("help_url"))
    parser.add_argument(
        "quality", nargs="?",
        choices=["max", "medium", "low", "audio", "text"],
        help=t("help_quality"),
    )
    parser.add_argument("-l", "--lang", default=DEFAULT_LANG,
                        help=t("help_lang", default=DEFAULT_LANG))
    parser.add_argument("--mp3", action="store_true",
                        help=t("help_mp3"))
    parser.add_argument("--abitrate", choices=["128k", "192k", "320k"],
                        default=DEFAULT_BITRATE, help=t("help_abitrate"))
    parser.add_argument("-o", "--output", default="downloads",
                        help=t("help_output"))
    parser.add_argument("-u", "--ui-lang", default=None,
                        help=t("help_ui_lang"))
    parser.add_argument("--check-queue", action="store_true",
                        help=t("help_check_queue"))
    parser.add_argument("--queue-list", action="store_true",
                        help=t("help_queue_list"))
    parser.add_argument("--queue-remove", metavar="URL",
                        help=t("help_queue_remove"))
    parser.add_argument("--watch", nargs="?", const=15, type=float, metavar="MIN",
                        help=t("help_watch"))

    args = parser.parse_args()

    # Язык мог быть задан короткой формой -u; применяем после разбора
    if args.ui_lang:
        i18n.set_language(args.ui_lang)

    # --- Команды очереди ожидания ---
    if args.queue_list:
        items = load_queue()
        if not items:
            print(t("queue_empty"))
        else:
            print(t("queue_list_header"))
            for it in items:
                print(t("queue_list_line", quality=it["quality"], url=it["url"],
                        added=it.get("added_at", "—"),
                        reason=it.get("reason", "—")))
        return
    if args.queue_remove:
        if remove_from_queue(args.queue_remove):
            print(t("queue_removed", url=args.queue_remove))
        else:
            print(t("queue_not_found", url=args.queue_remove))
        return
    if args.check_queue:
        check_pending(output_path=args.output)
        return
    if args.watch:
        _watch_loop(args.watch, output_path=args.output)
        return

    # Запуск без аргументов — показываем справку
    if args.url is None:
        parser.print_help()
        print_extended_help()
        return

    # Очередь не пуста — сначала проверим, не стало ли что-то доступным
    if load_queue():
        print(t("queue_count", count=len(load_queue())))
        check_pending(output_path=args.output)
        print()

    # Если URL есть, но качество не указано — интерактивный выбор
    if args.quality is None:
        print()
        print(t("choose_quality"))
        print(t("q_max"))
        print(t("q_medium"))
        print(t("q_low"))
        print(t("q_audio"))
        print(t("q_text"))
        choice = input(t("prompt_quality")).strip() or "1"
        quality = {"1": "max", "2": "medium", "3": "low", "4": "audio",
                   "5": "text"}.get(choice, "max")
    else:
        quality = args.quality

    # Если mp3 не указан явно и это не режим audio/text — спросим (только в интерактиве)
    save_mp3 = args.mp3
    if quality not in ("audio", "text") and not args.mp3 and args.quality is None:
        ans = input(t("prompt_mp3")).strip().lower()
        save_mp3 = ans in ("y", "yes", "д", "да")

    ok = download_video(args.url, quality, output_path=args.output,
                        lang=args.lang, save_mp3=save_mp3, abitrate=args.abitrate)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
