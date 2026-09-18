import os
import re
import sys
import html
import argparse
import subprocess
import shutil
from datetime import datetime

from pytubefix import YouTube
from pytubefix.cli import on_progress

import i18n
from i18n import t

# ---------- Константы ----------
LOG_TXT = "download_log.txt"
LOG_HTML = "download_log.html"

DEFAULT_LANG = "ru"
RU_LANG_CODES = {"ru", "rus", "russian", "русский"}

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
        return None

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
            f.write(t("tr_title", title=yt.title) + "\n")
            f.write(t("tr_author", author=yt.author) + "\n")
            f.write(t("tr_lang", lang=chosen.code) + "\n")
            f.write(t("tr_source", url=f"https://youtu.be/{yt.video_id}") + "\n")
            f.write("#" + "=" * 60 + "\n\n")
            f.write(text)

        print(t("ok_transcript", path=transcript_path))
        _report(progress, 90, "ok_transcript", path=transcript_path)
        return transcript_path
    except Exception as e:
        print(t("warn_transcript_error", error=e))
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

def download_audio_only(yt, output_path, preferred_lang, as_mp3=True, progress=None):
    """Скачивает только аудио. Если as_mp3 и есть ffmpeg — конвертирует в mp3."""
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
        final_name = safe_filename(yt.title) + ".mp3"
        final_path = os.path.join(output_path, final_name)
        print(t("converting_mp3"))
        _report(progress, 55, "converting_mp3")
        if convert_to_mp3(tmp_path, final_path):
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


# ---------- Основной сценарий ----------

def download_video(url, quality, output_path="downloads",
                   lang=DEFAULT_LANG, save_mp3=False, progress=None):
    """
    Качество: 'max' / 'medium' / 'low' / 'audio'.
    save_mp3: если True — дополнительно сохраняет mp3-дорожку рядом с видео.
    progress: опциональный callback(percent, message) для индикации прогресса.
    """
    os.makedirs(output_path, exist_ok=True)

    downloaded_ids = load_downloaded_ids()
    if downloaded_ids:
        print(t("info_log_entries", count=len(downloaded_ids)))

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
    except Exception as e:
        print(t("err_get_video", error=e))
        return

    if yt.video_id in downloaded_ids:
        print()
        print(t("warn_already_downloaded"))
        print(t("already_id", id=yt.video_id))
        print(t("already_title", title=yt.title))
        return

    print()
    print(t("video_title", title=yt.title))
    print(t("video_author", author=yt.author))
    print(t("video_duration", duration=format_duration(yt.length)))
    print(t("video_id", id=yt.video_id))
    print()
    _report(progress, 10, "video_title", title=yt.title)

    # ====== РЕЖИМ «ТОЛЬКО АУДИО» ======
    if quality.lower() == "audio":
        audio_path, audio_lang_name = download_audio_only(
            yt, output_path, preferred_lang=lang, as_mp3=True, progress=progress,
        )
        if audio_path is None:
            return

        transcript_path = download_transcript(yt, output_path, preferred_lang=lang,
                                              progress=progress)
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
        print(t("ok_log_entry", txt=LOG_TXT, html=LOG_HTML))
        _report(progress, 100, "ok_log_entry", txt=LOG_TXT, html=LOG_HTML)
        return

    # ====== РЕЖИМ ВИДЕО ======
    selected_video, is_dash = pick_video_stream(yt, quality)
    if selected_video is None:
        print(t("err_no_video_stream"))
        return

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
            return
        sp = sorted(fallback, key=_res_key)
        selected_video = {"max": sp[-1], "medium": sp[len(sp) // 2],
                          "low": sp[0]}.get(quality.lower())
        if selected_video is None:
            print(t("err_no_video_stream"))
            return
        selected_audio = None
        needs_merge = False
        audio_lang_name = t("audio_lang_embedded")

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
                    return

            final_name = safe_filename(yt.title) + ".mp4"
            final_path = os.path.join(output_path, final_name)

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
                    return
                sp = sorted(prog, key=_res_key)
                fallback_stream = {"max": sp[-1], "medium": sp[len(sp) // 2],
                                   "low": sp[0]}.get(quality.lower())
                if fallback_stream is None:
                    print(t("err_no_video_stream"))
                    return
                filepath = fallback_stream.download(output_path=output_path)
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
            filepath = selected_video.download(output_path=output_path)
            print()
            print(t("ok_video_saved", path=filepath))
            _report(progress, 80, "ok_video_saved", path=filepath)

    except Exception as e:
        print()
        print(t("err_download", error=e))
        return

    # Транскрипция
    transcript_path = download_transcript(yt, output_path, preferred_lang=lang,
                                          progress=progress)

    # Опционально — mp3 рядом с видео
    audio_file_path = None
    if save_mp3:
        print()
        print(t("extra_mp3"))
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
        choices=["max", "medium", "low", "audio"],
        help=t("help_quality"),
    )
    parser.add_argument("-l", "--lang", default=DEFAULT_LANG,
                        help=t("help_lang", default=DEFAULT_LANG))
    parser.add_argument("--mp3", action="store_true",
                        help=t("help_mp3"))
    parser.add_argument("-o", "--output", default="downloads",
                        help=t("help_output"))
    parser.add_argument("-u", "--ui-lang", default=None,
                        help=t("help_ui_lang"))

    args = parser.parse_args()

    # Язык мог быть задан короткой формой -u; применяем после разбора
    if args.ui_lang:
        i18n.set_language(args.ui_lang)

    # Запуск без аргументов — показываем справку
    if args.url is None:
        parser.print_help()
        print_extended_help()
        return

    # Если URL есть, но качество не указано — интерактивный выбор
    if args.quality is None:
        print()
        print(t("choose_quality"))
        print(t("q_max"))
        print(t("q_medium"))
        print(t("q_low"))
        print(t("q_audio"))
        choice = input(t("prompt_quality")).strip() or "1"
        quality = {"1": "max", "2": "medium", "3": "low", "4": "audio"}.get(choice, "max")
    else:
        quality = args.quality

    # Если mp3 не указан явно и это не режим audio — спросим (только в интерактиве)
    save_mp3 = args.mp3
    if quality != "audio" and not args.mp3 and args.quality is None:
        ans = input(t("prompt_mp3")).strip().lower()
        save_mp3 = ans in ("y", "yes", "д", "да")

    download_video(args.url, quality, output_path=args.output,
                   lang=args.lang, save_mp3=save_mp3)


if __name__ == "__main__":
    main()
