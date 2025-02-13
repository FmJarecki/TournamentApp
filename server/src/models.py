from pydantic import BaseModel, Field, field_validator
from config import Position
from datetime import datetime


class Player(BaseModel):
    name: str
    number: int = Field(..., ge=1, le=99)
    team_id: int
    position: Position
    is_starting: bool
    goals: int = 0


class Team(BaseModel):
    name: str
    total_goals: int = 0
    conceded_goals: int = 0
    points: int = 0
    group: str = ''


class Match(BaseModel):
    round: int
    team1_id: int
    team2_id: int
    score1: int
    score2: int
    date: str
    stadium: str
    localization: tuple[float, float]
    scorers1: list[dict[str, dict]]
    scorers2: list[dict[str, dict]]

    @field_validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Date must be in ISO format (%Y-%m-%d %H:%M)")
        return v
