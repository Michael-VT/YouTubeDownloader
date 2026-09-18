import os
import sys
from pytubefix import YouTube
from pytubefix.cli import on_progress


def download_video(url: str, quality: str, output_path: str = "downloads"):
    """
    Скачивает видео с YouTube в выбранном качестве.
    
    :param url: ссылка на видео
    :param quality: 'max', 'medium' или 'low'
    :param output_path: папка для сохранения
    """
    os.makedirs(output_path, exist_ok=True)

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
    except Exception as e:
        print(f"❌ Ошибка при получении видео: {e}")
        return

    print(f"\n🎬 Название: {yt.title}")
    print(f"👤 Автор: {yt.author}")
    print(f"⏱  Длительность: {yt.length // 60} мин {yt.length % 60} сек\n")

    streams = yt.streams.filter(progressive=True, file_extension="mp4")

    if not streams:
        streams = yt.streams.filter(file_extension="mp4", adaptive=True)

    # Сортируем по разрешению
    sorted_streams = sorted(
        streams,
        key=lambda s: int(s.resolution.replace("p", "")) if s.resolution else 0,
    )

    if not sorted_streams:
        print("❌ Не удалось найти подходящие потоки видео")
        return

    quality_map = {
        "max": sorted_streams[-1],       # самое высокое
        "medium": sorted_streams[len(sorted_streams) // 2],  # среднее
        "low": sorted_streams[0],        # самое низкое
    }

    selected = quality_map.get(quality.lower())
    if selected is None:
        print("❌ Неверное значение качества. Используйте: max / medium / low")
        return

    print(f"⬇️  Выбрано качество: {selected.resolution} "
          f"({selected.filesize_mb:.1f} MB)")

    try:
        filepath = selected.download(output_path=output_path)
        print(f"\n✅ Видео сохранено: {filepath}")
    except Exception as e:
        print(f"\n❌ Ошибка при скачивании: {e}")


def main():
    if len(sys.argv) >= 3:
        url = sys.argv[1]
        quality = sys.argv[2]
    else:
        url = input("🔗 Введите ссылку на YouTube видео: ").strip()
        print("\nВыберите качество:")
        print("  1 — максимальное")
        print("  2 — среднее")
        print("  3 — низкое")
        choice = input("Введите номер (1/2/3) [по умолчанию 1]: ").strip() or "1"

        quality = {"1": "max", "2": "medium", "3": "low"}.get(choice, "max")

    download_video(url, quality)


if __name__ == "__main__":
    main()
