import os
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session, joinedload

from database import get_db, PlayerModel, TeamModel, MatchModel
from models import Player, Team, Match
from crud import add_player, add_team, add_match
from auth import create_access_token, authenticate_user, get_current_admin


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


@app.get("/teams/{team_id}/logo")
def get_team_logo(team_id: int, db: Session = Depends(get_db)) -> FileResponse:
    team = db.query(TeamModel).filter_by(id=team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    logo_path: str = f"../data/logos/{team_id}.png"
    if not os.path.exists(logo_path):
        raise HTTPException(status_code=404, detail="Logo file not found")

    return FileResponse(logo_path)


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


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


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
