import json
import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator

from config import Position


app = FastAPI()


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
    teams: list[str]
    scores: list[int]
    date: str
    stadium: str
    localization: tuple[float, float]
    scorers: dict[str, list[dict[str, dict]]]

    @model_validator(mode="before")
    def check_teams_and_scores(cls, values):
        teams = values.get("teams", [])
        scores = values.get("scores", [])
        if len(teams) != len(scores):
            raise ValueError("Number of teams must match number of scores")
        return values


PLAYERS_FILE = "players.json"
TEAMS_FILE = "teams.json"
MATCHES_FILE = "matches.json"


def load_data(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Corrupted file: {filename}")
    return []


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)  # type: ignore


def save_players():
    save_data(PLAYERS_FILE, players)


def save_teams():
    save_data(TEAMS_FILE, teams)


def save_matches():
    save_data(MATCHES_FILE, matches)


players: list[dict] = load_data(PLAYERS_FILE)
teams: list[dict] = load_data(TEAMS_FILE)
matches: list[dict] = load_data(MATCHES_FILE)

players_dict = {f"{u['name']}_{u['number']}": u for u in players}
teams_dict = {t['name']: t for t in teams}


def find_player(name: str, number: int) -> dict:
    key = f"{name}_{number}"
    if key in players_dict:
        return players_dict[key]
    raise HTTPException(status_code=404, detail="Player not found")


def find_team(team_name: str) -> dict:
    if team_name in teams_dict:
        return teams_dict[team_name]
    raise HTTPException(status_code=404, detail="Team not found")


@app.post("/players/")
def add_player(player: Player):
    key = f"{player.name}_{player.number}"
    if key in players_dict:
        raise HTTPException(status_code=400, detail="Player already exists")
    player_data = player.model_dump()
    players.append(player_data)
    players_dict[key] = player_data
    save_players()
    return {"message": "Player added"}


@app.get("/players/")
def get_players():
    return players


@app.get("/players/{name}/{number}")
def get_player(name: str, number: int):
    return find_player(name, number)


@app.post("/teams/")
def add_team(team: Team):
    if team.name in teams_dict:
        raise HTTPException(status_code=400, detail="Team already exists")
    team_data = team.model_dump()
    teams.append(team_data)
    teams_dict[team.name] = team_data
    save_teams()
    return {"message": "Team added"}


@app.get("/teams/")
def get_teams():
    return teams


@app.get("/teams/name/{team_name}")
def get_team(team_name: str):
    return find_team(team_name)


@app.get("/teams/group/{group}")
def get_teams_from_group(group: str) -> list[dict]:
    return [team for team in teams if team["group"] == group]


@app.get("/teams/{team_name}/players")
def get_team_players(team_name: str) -> list[dict]:
    find_team(team_name)
    team_players = [player for player in players if player["team"] == team_name]
    if not team_players:
        raise HTTPException(status_code=404, detail=f"No players found for team {team_name}")
    return team_players


@app.put("/players/{name}/{number}/update_goals")
def update_player_goals(name: str, number: int, goals: int):
    player = find_player(name, number)
    player["goals"] += goals
    save_players()
    update_team_stats(player["team"])
    return {"message": "Player goals updated"}


def update_team_stats(team_name: str):
    team = find_team(team_name)
    team["total_goals"] = 0
    team["conceded_goals"] = 0
    team["points"] = 0

    for match in matches:
        if team_name in match["teams"]:
            match_datetime = datetime.fromisoformat(match["date"])
            now = datetime.now()

            if match_datetime <= now:
                team_index = match["teams"].index(team_name)
                scored_goals = match["scores"][team_index]
                conceded_goals = sum(match["scores"]) - scored_goals

                team["total_goals"] += scored_goals
                team["conceded_goals"] += conceded_goals

                if scored_goals > conceded_goals:
                    team["points"] += 3
                elif scored_goals == conceded_goals:
                    team["points"] += 1
    save_teams()


@app.post("/matches/")
def add_match(match: Match):
    for team_name in match.teams:
        if team_name not in teams_dict:
            raise HTTPException(status_code=400, detail=f"Team '{team_name}' does not exist")

    match_data = match.model_dump()
    matches.append(match_data)
    save_matches()

    for team_name in match.teams:
        update_team_stats(team_name)
    return {"message": "Match added"}


@app.get("/sorted_time_matches/")
def get_time_sorted_matches():
    sorted_matches: list[dict] = sorted(
        matches,
        key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M"),
        reverse=False
    )
    return sorted_matches


@app.get("/matches/")
def get_matches():
    return matches


@app.get("/matches/{round_number}")
def get_matches_by_round(round_number: int):
    round_matches = [match for match in matches if match["round"] == round_number]
    if not round_matches:
        raise HTTPException(status_code=404, detail="No matches found for this round")
    return round_matches
