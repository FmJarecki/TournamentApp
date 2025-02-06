from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List
from config import Position
from datetime import datetime


class Player(BaseModel):
    name: str
    number: int = Field(..., ge=1, le=99)
    team: str
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
    teams: List[str]
    scores: List[int]
    date: str
    stadium: str
    localization: tuple[float, float]
    scorers: dict[str, list[dict[str, dict]]]

    @field_validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Date must be in ISO format (%Y-%m-%d %H:%M)")
        return v

    @model_validator(mode="before")
    def check_teams_and_scores(cls, values):
        teams = values.get("teams", [])
        scores = values.get("scores", [])
        if len(teams) != len(scores):
            raise ValueError("Number of teams must match number of scores")
        return values
