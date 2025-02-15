from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException


from auth import get_current_admin
from database import PlayerModel, TeamModel, MatchModel
from models import Player, Team, Match


def add_player(db: Session, player: Player, current_user: str = Depends(get_current_admin)):
    if not current_user:
        raise HTTPException(status_code=403, detail="Not authorized")


    team = db.query(TeamModel).filter_by(id=player.team_id).first()
    if not team:
        raise HTTPException(status_code=400, detail="Team does not exist")

    db_player = PlayerModel(
        name=player.name,
        number=player.number,
        team_id=player.team_id,
        position=player.position.value,
        is_starting=player.is_starting,
        goals=player.goals
    )

    try:
        db.add(db_player)
        db.commit()
        db.refresh(db_player)
        return {"message": "Player added successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Player already exists")


def add_team(db: Session, team: Team):
    db_team = TeamModel(
        name=team.name,
        total_goals=team.total_goals,
        conceded_goals=team.conceded_goals,
        points=team.points,
        group=team.group
    )

    try:
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return {"message": "Team added successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Team already exists")


def add_match(db: Session, match: Match):
    team1 = db.query(TeamModel).filter_by(id=match.team1_id).first()
    team2 = db.query(TeamModel).filter_by(id=match.team2_id).first()
    if not team1 or not team2:
        raise HTTPException(status_code=400, detail="One or both teams do not exist")

    db_match = MatchModel(
        round=match.round,
        team1_id=match.team1_id,
        team2_id=match.team2_id,
        score1=match.score1,
        score2=match.score2,
        date=match.date,
        stadium=match.stadium,
        localization=list(match.localization),
        scorers1=match.scorers1,
        scorers2=match.scorers2
    )

    try:
        db.add(db_match)
        db.commit()
        db.refresh(db_match)

        update_team_stats(db, match.team1_id)
        update_team_stats(db, match.team2_id)

        return {"message": "Match added successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error adding match")


def update_team_stats(db: Session, team_id: int):
    team = db.query(TeamModel).filter_by(id=team_id).first()
    team.total_goals = 0
    team.conceded_goals = 0
    team.points = 0

    matches = db.query(MatchModel).filter(
        or_(MatchModel.team1_id == team_id, MatchModel.team2_id == team_id)
    ).all()

    for match in matches:
        match_datetime = datetime.strptime(match.date, "%Y-%m-%d %H:%M")
        now = datetime.now()

        if match_datetime <= now:
            if match.team1_id == team_id:
                scored_goals = match.score1
                conceded_goals = match.score2
            else:
                scored_goals = match.score2
                conceded_goals = match.score1

            team.total_goals += scored_goals
            team.conceded_goals += conceded_goals

            if scored_goals > conceded_goals:
                team.points += 3
            elif scored_goals == conceded_goals:
                team.points += 1

    db.commit()
