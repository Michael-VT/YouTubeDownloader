"""Минималистичный i18n-модуль: выбор языка интерфейса и перевод ключей.

Языки: en, ru, uk, pt, de, fr. Переводы лежат в locales/<lang>.py (STRINGS).
Язык хранится в thread-local storage: веб-сервер выполняет задачи в потоках,
и каждая задача может использовать свой язык интерфейса.
"""

import os
import threading

try:
    from locales import LANGS, STRINGS
except ImportError:  # pragma: no cover - locales всегда рядом с i18n.py
    LANGS = ("en",)
    STRINGS = {}

LANGUAGE_NAMES = {
    "en": "English",
    "ru": "Русский",
    "uk": "Українська",
    "pt": "Português",
    "de": "Deutsch",
    "fr": "Français",
}

_local = threading.local()
DEFAULT = "en"


def normalize(lang) -> str | None:
    """«pt-BR» / «ru_RU.UTF-8» -> «pt» / «ru»; None для неизвестного языка."""
    if not lang:
        return None
    code = str(lang).strip().lower().replace("-", "_").split("_")[0]
    return code if code in LANGS else None


def set_language(lang) -> str:
    """Устанавливает язык интерфейса для текущего потока. Возвращает код."""
    code = normalize(lang) or DEFAULT
    _local.lang = code
    return code


def get_language() -> str:
    return getattr(_local, "lang", None) or DEFAULT


def detect_language() -> str:
    """Определяет язык из окружения (YTD_LANG, LC_ALL, LANG …), иначе 'en'."""
    for var in ("YTD_LANG", "LC_ALL", "LC_MESSAGES", "LANG"):
        val = os.environ.get(var)
        if val:
            code = normalize(val)
            if code:
                return code
    try:
        import locale
        loc = locale.getlocale()[0]
        if loc:
            code = normalize(loc)
            if code:
                return code
    except Exception:
        pass
    return DEFAULT


def available_languages() -> dict:
    return {code: LANGUAGE_NAMES.get(code, code) for code in LANGS}


def t(key: str, **kwargs) -> str:
    """Перевод ключа на текущий язык с fallback на английский."""
    entry = STRINGS.get(key)
    if not entry:
        return key
    text = entry.get(get_language()) or entry.get(DEFAULT)
    if text is None:
        return key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            return text
    return text
