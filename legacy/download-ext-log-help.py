import os
import sys
import io
import threading
import uuid
import html as html_module

from flask import Flask, request, jsonify, send_file, Response

# Импортируем логику из download.py (файл должен лежать рядом)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import download as dl  # noqa: E402

app = Flask(__name__)

# Хранилище задач: task_id -> dict
TASKS = {}
TASKS_LOCK = threading.Lock()

HTML_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web_ui.html")


# ---------- Раздача страницы ----------

@app.route("/")
def index():
    if not os.path.exists(HTML_FILE):
        return Response("web_ui.html не найден рядом с web_server.py", status=500)
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return Response(f.read(), mimetype="text/html; charset=utf-8")


# ---------- API: информация о видео ----------

@app.route("/api/info", methods=["POST"])
def api_info():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify({"error": "URL не указан"}), 400

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

    if not url:
        return jsonify({"error": "URL не указан"}), 400
    if quality not in ("max", "medium", "low", "audio"):
        return jsonify({"error": "Неверное качество"}), 400

    task_id = uuid.uuid4().hex
    with TASKS_LOCK:
        TASKS[task_id] = {
            "status": "running",
            "percent": 5,
            "message": "Запуск…",
            "log": "",
            "stage": "init",
        }

    def run_task():
        # Перехватываем stdout download_video, чтобы отдавать лог в UI
        buf = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = buf

        def updater(stage, percent=None, message=None):
            with TASKS_LOCK:
                if task_id not in TASKS:
                    return
                TASKS[task_id]["log"] = buf.getvalue()
                if message is not None:
                    TASKS[task_id]["message"] = message
                if percent is not None:
                    TASKS[task_id]["percent"] = percent
                TASKS[task_id]["stage"] = stage

        try:
            # Скачивание (внутри download_video печатает в stdout)
            # Обновляем прогресс по ходу через простой таймер-наблюдатель
            import threading as _t

            def watcher():
                # простой анализатор stdout на предмет ключевых фраз
                mapping = [
                    ("Получение", 10), ("Название:", 15),
                    ("Выбрано качество", 20), ("Скачивание видеопотока", 30),
                    ("Скачивание аудиопотока", 50), ("Склейка", 65),
                    ("Видео сохранено", 80), ("Транскрипция", 90),
                    ("mp3 сохранён", 95), ("Запись добавлена", 100),
                ]
                seen = set()
                while True:
                    with TASKS_LOCK:
                        if task_id not in TASKS or TASKS[task_id]["status"] != "running":
                            return
                    text = buf.getvalue()
                    for key, pct in mapping:
                        if key in text and key not in seen:
                            seen.add(key)
                            updater("progress", pct, key)
                    _t.Event().wait(0.5)

            threading.Thread(target=watcher, daemon=True).start()

            dl.download_video(url, quality, output_path=output,
                              lang=lang, save_mp3=save_mp3)

            with TASKS_LOCK:
                TASKS[task_id]["status"] = "done"
                TASKS[task_id]["percent"] = 100
                TASKS[task_id]["message"] = "Готово"
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
        if not task:
            return jsonify({"error": "Задача не найдена"}), 404
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
    if not os.path.isdir(out_dir):
        return jsonify([])
    files = []
    for name in sorted(os.listdir(out_dir)):
        path = os.path.join(out_dir, name)
        if os.path.isfile(path):
            files.append({"name": name, "size": os.path.getsize(path)})
    return jsonify(files)


@app.route("/api/files/<path:filename>")
def api_get_file(filename):
    out_dir = os.path.abspath("downloads")
    target = os.path.abspath(os.path.join(out_dir, filename))
    if not target.startswith(out_dir + os.sep) or not os.path.isfile(target):
        return "Not found", 404
    return send_file(target, as_attachment=True)


# ---------- Запуск ----------

if __name__ == "__main__":
    print("\n🌐 Открой в браузере: http://127.0.0.1:5000\n")
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)

