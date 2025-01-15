import json
import os
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


class Match(BaseModel):
    round: int
    teams: list[str]
    scores: list[int]

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


@app.get("/teams/{team_name}")
def get_team(team_name: str):
    return find_team(team_name)


@app.get("/teams/{team_name}/players")
def get_team_players(team_name: str):
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
    update_team_stats(player["team"], scored=goals)
    return {"message": "Player goals updated"}


def update_team_stats(team_name: str, scored: int = 0, conceded: int = 0):
    team = find_team(team_name)
    team["total_goals"] += scored
    team["conceded_goals"] += conceded

    if scored > conceded:
        team["points"] += 3
    elif scored == conceded:
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

    for i, team_name in enumerate(match.teams):
        scored = match.scores[i]
        conceded = sum(match.scores) - scored
        update_team_stats(team_name, scored=scored, conceded=conceded)
    return {"message": "Match added"}


@app.get("/matches/")
def get_matches():
    return matches


@app.get("/matches/{round_number}")
def get_matches_by_round(round_number: int):
    round_matches = [match for match in matches if match["round"] == round_number]
    if not round_matches:
        raise HTTPException(status_code=404, detail="No matches found for this round")
    return round_matches
