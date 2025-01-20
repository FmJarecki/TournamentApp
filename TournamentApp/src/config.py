from enum import Enum

SERVER_URL = "http://192.168.1.105:8000"  # fill with local ip

IMAGES_PATH = 'images'

DARK_COLOR = '#D9D9D9'
DARK_THEME_COLOR = (0.1, 0.1, 0.1, 1)
DARK_BUTTONS_COLOR = 0.2, 0.2, 0.2, 1
DARK_IMAGES_PATH: str = 'images/dark_theme'

BRIGHT_COLOR = '#434343'
BRIGHT_THEME_COLOR = (0.9, 0.9, 0.9, 1)
BRIGHT_BUTTONS_COLOR = 0.8, 0.8, 0.8, 1
BRIGHT_IMAGES_PATH: str = 'images/bright_theme'

class Position(str, Enum):
    LB = "Left Back"
    RB = "Right Back"
    CB = "Center Back"
    LM = "Left Midfielder"
    RM = "Right Midfielder"
    CM = "Center Midfielder"
    ST = "Striker"
    GK = "Goalkeeper"
