from enum import Enum

SERVER_URL = "http://192.168.0.21:8000"  # fill with local ip

class Position(str, Enum):
    LB = "Left Back"
    RB = "Right Back"
    CB = "Center Back"
    LM = "Left Midfielder"
    RM = "Right Midfielder"
    CM = "Center Midfielder"
    ST = "Striker"
    GK = "Goalkeeper"
