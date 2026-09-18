import os
import sys
import io
import threading
import uuid

from flask import Flask, request, jsonify, send_file, Response

# Импортируем логику из download.py (файл должен лежать рядом)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import download as dl  # noqa: E402
import i18n  # noqa: E402
from i18n import t  # noqa: E402

app = Flask(__name__)

# Хранилище задач: task_id -> dict
TASKS = {}
TASKS_LOCK = threading.Lock()

HTML_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_ui.html")


# ---------- Раздача страницы ----------

@app.route("/")
def index():
    if not os.path.exists(HTML_FILE):
        return Response(t("srv_ui_missing"), status=500)
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return Response(f.read(), mimetype="text/html; charset=utf-8")


# ---------- API: переводы для веб-интерфейса ----------

@app.route("/api/i18n")
def api_i18n():
    """Отдаёт все строки web.* на всех языках: {lang: {key: text}}."""
    from locales import STRINGS
    out = {}
    for key, translations in STRINGS.items():
        if not key.startswith("web_"):
            continue
        for lang, text in translations.items():
            out.setdefault(lang, {})[key] = text
    return jsonify(out)


# ---------- API: информация о видео ----------

@app.route("/api/info", methods=["POST"])
def api_info():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"error": t("srv_url_missing")}), 400

    try:
        from pytubefix import YouTube
        yt = YouTube(url)

        adaptive = yt.streams.filter(only_video=True, adaptive=True, file_extension="mp4")
        resolutions = sorted(
            {s.resolution for s in adaptive if s.resolution},
            key=lambda r: int(r.replace("p", "")),
        )
        progressive = yt.streams.filter(progressive=True, file_extension="mp4")
        prog_res = sorted(
            {s.resolution for s in progressive if s.resolution},
            key=lambda r: int(r.replace("p", "")),
        )

        return jsonify({
            "id": yt.video_id,
            "title": yt.title,
            "author": yt.author,
            "length": yt.length,
            "duration": dl.format_duration(yt.length),
            "thumbnail": yt.thumbnail_url,
            "resolutions": resolutions,
            "progressive_resolutions": prog_res,
            "has_captions": bool(yt.captions),
            "already_downloaded": yt.video_id in dl.load_downloaded_ids(),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------- API: запуск скачивания ----------

@app.route("/api/download", methods=["POST"])
def api_download():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    quality = data.get("quality", "max")
    lang = data.get("lang", dl.DEFAULT_LANG)
    save_mp3 = bool(data.get("save_mp3", False))
    output = data.get("output", "downloads")
    ui_lang = data.get("ui_lang")

    if not url:
        return jsonify({"error": t("srv_url_missing")}), 400
    if quality not in ("max", "medium", "low", "audio"):
        return jsonify({"error": t("srv_bad_quality")}), 400

    task_id = uuid.uuid4().hex
    with TASKS_LOCK:
        TASKS[task_id] = {
            "status": "running",
            "percent": 5,
            "message": t("srv_task_starting"),
            "log": "",
            "stage": "init",
        }

    def run_task():
        # Перехватываем stdout download_video, чтобы отдавать лог в UI.
        # Язык интерфейса — thread-local, поэтому задача не влияет на другие
        # запросы и сама не зависит от них.
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf
        i18n.set_language(ui_lang)

        def update(percent=None, message=None):
            with TASKS_LOCK:
                if task_id not in TASKS:
                    return
                TASKS[task_id]["log"] = buf.getvalue()
                if message is not None:
                    TASKS[task_id]["message"] = message
                if percent is not None:
                    TASKS[task_id]["percent"] = percent

        def progress(percent, message):
            update(percent=percent, message=message)

        try:
            dl.download_video(url, quality, output_path=output,
                              lang=lang, save_mp3=save_mp3,
                              progress=progress)

            with TASKS_LOCK:
                TASKS[task_id]["status"] = "done"
                TASKS[task_id]["percent"] = 100
                TASKS[task_id]["message"] = t("srv_task_done")
                TASKS[task_id]["log"] = buf.getvalue()
        except Exception as e:
            with TASKS_LOCK:
                TASKS[task_id]["status"] = "error"
                TASKS[task_id]["message"] = str(e)
                TASKS[task_id]["log"] = buf.getvalue() + f"\n❌ {e}"
        finally:
            sys.stdout = old_stdout

    threading.Thread(target=run_task, daemon=True).start()
    return jsonify({"task_id": task_id})


# ---------- API: статус задачи ----------

@app.route("/api/status/<task_id>")
def api_status(task_id):
    with TASKS_LOCK:
        task = TASKS.get(task_id)
        if task is None:
            return jsonify({"error": "Unknown task"}), 404
        return jsonify(task)


# ---------- API: журнал ----------

@app.route("/api/log")
def api_log():
    entries = dl.parse_log_entries()
    return jsonify(entries)


# ---------- API: файлы в downloads ----------

@app.route("/api/files")
def api_files():
    out_dir = "downloads"
    files = []
    if os.path.isdir(out_dir):
        for name in sorted(os.listdir(out_dir)):
            path = os.path.join(out_dir, name)
            if os.path.isfile(path):
                files.append({"name": name, "size": os.path.getsize(path)})
    return jsonify(files)


@app.route("/api/files/<path:filename>")
def api_get_file(filename):
    out_dir = os.path.abspath("downloads")
    target = os.path.abspath(os.path.join(out_dir, filename))
    if not target.startswith(out_dir):
        return Response("Forbidden", status=403)
    if not os.path.isfile(target):
        return Response("Not found", status=404)
    return send_file(target, as_attachment=True)


# ---------- Запуск ----------

if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    i18n.set_language(i18n.detect_language())
    print("\n" + t("srv_open_browser", url=f"http://{host}:{port}") + "\n")
    app.run(host=host, port=port, debug=False, threaded=True)
