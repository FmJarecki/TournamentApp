from settings_db import *


TEXT_FIELDS = {
    "en": {
        "dark_theme": "Dark theme"
    },
    "it": {
        "dark_theme": "Tema scuro"
    }
}

def get_text(key: str) -> str:
    curr_len = "en"
    return TEXT_FIELDS[curr_len][key]
