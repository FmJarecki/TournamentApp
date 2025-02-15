from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import get_db, PlayerModel, TeamModel, MatchModel
from models import Player, Team, Match
from crud import add_player, add_team, add_match
from auth import get_current_admin


app = FastAPI()


@app.get("/players/")
def get_players(db: Session = Depends(get_db)):
    return db.query(PlayerModel).all()


@app.get("/players/player_id")
def get_player(
        player_id: int,
        db: Session = Depends(get_db)
):
    player = db.query(PlayerModel).filter_by(id=player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@app.get("/teams/")
def get_teams(db: Session = Depends(get_db)):
    return db.query(TeamModel).all()


@app.get("/teams/{team_id}")
def get_team(team_id: str, db: Session = Depends(get_db)):
    team = db.query(TeamModel).filter_by(id=team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.get("/teams/group/{group}")
def get_teams_from_group(group: str, db: Session = Depends(get_db)):
    return db.query(TeamModel).filter_by(group=group).all()


@app.get("/teams/{team_id}/players")
def get_team_players(
        team_id: int,
        db: Session = Depends(get_db)
):
    team = db.query(TeamModel).options(joinedload(TeamModel.players)).filter_by(id=team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team.players


@app.get("/matches/")
def get_matches(db: Session = Depends(get_db)):
    return db.query(MatchModel).all()


@app.get("/matches/{round_number}")
def get_matches_by_round(round_number: int, db: Session = Depends(get_db)):
    matches = db.query(MatchModel).filter_by(round=round_number).all()
    if not matches:
        raise HTTPException(status_code=404, detail="No matches found for this round")
    return matches


@app.get("/sorted_time_matches/")
def get_time_sorted_matches(db: Session = Depends(get_db)):
    return db.query(MatchModel).order_by(MatchModel.date).all()


@app.post("/players/")
def create_player(
    player: Player,
    db: Session = Depends(get_db),
    admin: str = Depends(get_current_admin)
):
    return add_player(db, player)


@app.post("/teams/")
def create_team(
        team: Team,
        db: Session = Depends(get_db)
):
    return add_team(db, team)


@app.post("/matches/")
def create_match(
        match: Match,
        db: Session = Depends(get_db)
):
    return add_match(db, match)


@app.put("/players/{player_id}/update_goals")
def update_player_goals(
        name: str,
        number: int,
        goals: int,
        db: Session = Depends(get_db)
):
    player = db.query(PlayerModel).filter_by(name=name, number=number).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")

    player.goals += goals
    db.commit()
    return {"message": "Player goals updated"}
