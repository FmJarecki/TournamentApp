from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from database import PlayerModel, TeamModel, MatchModel
from models import Player, Team, Match


def add_player(db: Session, player: Player):
    team = db.query(TeamModel).filter_by(name=player.team).first()
    if not team:
        raise HTTPException(status_code=400, detail="Team does not exist")

    db_player = PlayerModel(
        name=player.name,
        number=player.number,
        team_name=player.team,
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
    for team_name in match.teams:
        team = db.query(TeamModel).filter_by(name=team_name).first()
        if not team:
            raise HTTPException(status_code=400, detail=f"Team '{team_name}' does not exist")

    db_match = MatchModel(
        round=match.round,
        teams=match.teams,
        scores=match.scores,
        date=match.date,
        stadium=match.stadium,
        localization=list(match.localization),
        scorers=match.scorers
    )

    try:
        db.add(db_match)
        db.commit()
        db.refresh(db_match)

        for team_name in match.teams:
            update_team_stats(db, team_name)

        return {"message": "Match added successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error adding match")


def update_team_stats(db: Session, team_name: str):
    team = db.query(TeamModel).filter_by(name=team_name).first()
    team.total_goals = 0
    team.conceded_goals = 0
    team.points = 0

    matches = db.query(MatchModel).filter(MatchModel.teams.contains(team_name)).all()

    for match in matches:
        match_datetime = datetime.fromisoformat(match.date)
        now = datetime.now()

        if match_datetime <= now:
            team_index = match.teams.index(team_name)
            scored_goals = match.scores[team_index]
            conceded_goals = sum(match.scores) - scored_goals

            team.total_goals += scored_goals
            team.conceded_goals += conceded_goals

            if scored_goals > conceded_goals:
                team.points += 3
            elif scored_goals == conceded_goals:
                team.points += 1

    db.commit()
