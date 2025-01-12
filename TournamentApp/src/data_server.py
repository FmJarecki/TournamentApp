import json
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()


class User(BaseModel):
    username: str
    number: int = Field(..., ge=1, le=99)
    team: str
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


USERS_FILE = "users.json"
TEAMS_FILE = "teams.json"
MATCHES_FILE = "matches.json"


def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return []


def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)  # type: ignore


users = load_data(USERS_FILE)
teams = load_data(TEAMS_FILE)
matches = load_data(MATCHES_FILE)


@app.post("/users/")
def add_user(user: User):
    for u in users:
        if u["username"] == user.username and u["number"] == user.number:
            raise HTTPException(status_code=400, detail="User already exists")
    users.append(user.dict())
    save_data(USERS_FILE, users)
    return {"message": "User added"}


@app.get("/users/")
def get_users():
    return users


@app.get("/users/{username}/{number}")
def get_user(username: str, number: int):
    for user in users:
        if user["username"] == username and user["number"] == number:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/teams/")
def add_team(team: Team):
    for t in teams:
        if t["name"] == team.name:
            raise HTTPException(status_code=400, detail="Team already exists")
    teams.append(team.dict())
    save_data(TEAMS_FILE, teams)
    return {"message": "Team added"}


@app.get("/teams/")
def get_teams():
    return teams


@app.put("/users/{username}/{number}/update_goals")
def update_user_goals(username: str, number: int, goals: int):
    for user in users:
        if user["username"] == username and user["number"] == number:
            user["goals"] += goals
            save_data(USERS_FILE, users)

            update_team_stats(user["team"], scored=goals)
            return {"message": "User goals updated"}
    raise HTTPException(status_code=404, detail="User not found")


def update_team_stats(team_name: str, scored: int = 0, conceded: int = 0):
    for team in teams:
        if team["name"] == team_name:
            team["total_goals"] += scored
            team["conceded_goals"] += conceded

            if scored > conceded:
                team["points"] += 3
            elif scored == conceded:
                team["points"] += 1
            save_data(TEAMS_FILE, teams)
            return
    raise HTTPException(status_code=404, detail="Team not found")



@app.post("/matches/")
def add_match(match: Match):
    if len(match.teams) != len(match.scores):
        raise HTTPException(status_code=400, detail="Number of teams must match number of scores")

    for team_name in match.teams:
        if team_name not in [team["team"] for team in teams]:
            raise HTTPException(status_code=400, detail=f"Team '{team_name}' does not exist")

    matches.append(match.dict())
    save_data(MATCHES_FILE, matches)

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
