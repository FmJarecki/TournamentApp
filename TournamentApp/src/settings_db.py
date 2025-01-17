import sqlite3
import logging
from pathlib import Path


class SettingsDB:
    DB_FILE = "settings.db"

    @staticmethod
    def initialize_database():
        if not Path(SettingsDB.DB_FILE).exists():
            with sqlite3.connect(SettingsDB.DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE settings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        is_dark_theme BOOLEAN DEFAULT 1
                    )
                ''')
                cursor.execute('INSERT INTO settings (is_dark_theme) VALUES (1)')
                conn.commit()
            logging.info("Database initialized with default settings.")
        else:
            logging.info("Database already exists.")

    @staticmethod
    def get_dark_theme_setting() -> bool:
        with sqlite3.connect(SettingsDB.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT is_dark_theme FROM settings WHERE id = 1')
            result = cursor.fetchone()
            return bool(result[0]) if result else None

    @staticmethod
    def set_dark_theme_setting(is_dark_theme: bool):
        with sqlite3.connect(SettingsDB.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE settings SET is_dark_theme = ? WHERE id = 1', (1 if is_dark_theme else 0,))
            conn.commit()
            logging.info(f"Dark theme setting updated to: {is_dark_theme}")
