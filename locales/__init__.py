"""Загрузчик переводов. Каждый locales/<lang>.py содержит STRINGS = {ключ: текст}.

Недостающие модули/ключи просто отсутствуют в STRINGS — t() делает fallback
на английский, поэтому частичные переводы не ломают работу программы.
"""

import importlib

LANGS = ("en", "ru", "uk", "pt", "de", "fr")

STRINGS = {}

for _lang in LANGS:
    try:
        _mod = importlib.import_module("." + _lang, __name__)
    except ImportError:
        continue
    for _key, _text in getattr(_mod, "STRINGS", {}).items():
        STRINGS.setdefault(_key, {})[_lang] = _text
