from settings_db import SettingsDB


class TextManager:
    _instance = None

    TEXT_FIELDS = {
        "en": {
            "dark_theme": "Dark theme",
            "language": "Language",
            "name": "Name",
            'pts': "PTS",
            'gf': "GF",
            'ga': "GA"
        },
        "it": {
            "dark_theme": "Tema scuro",
            "language": "Lingua",
            "name": "Nome",
            'pts': "PTS",
            'gf': "GF",
            'ga': "GA"
        }
    }

    _current_language = None

    @classmethod
    def get_text(cls, key: str) -> str:
        if cls._current_language is None:
            cls._current_language = SettingsDB.get_language()
        if key in cls.TEXT_FIELDS[cls._current_language]:
            return cls.TEXT_FIELDS[cls._current_language][key]
        else:
            return key

    @classmethod
    def set_language(cls, language: str):
        if language in cls.TEXT_FIELDS:
            cls._current_language = language
            SettingsDB.set_language(language)
