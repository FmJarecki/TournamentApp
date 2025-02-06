from faker import Faker
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, PlayerModel, TeamModel, MatchModel
from models import Player, Team, Match
from database import Base, engine


fake = Faker()

POSITIONS = ["Left Back", "Right Back", "Center Back", "Left Midfielder", "Right Midfielder", "Center Midfielder", "Striker", "Goalkeeper"]


def generate_fake_matches():
    db = SessionLocal()

    try:
        teams = db.query(TeamModel).all()

        groups = {}
        for team in teams:
            if team.group not in groups:
                groups[team.group] = []
            groups[team.group].append(team)

        group_sizes = [len(groups[group]) for group in groups]
        if len(set(group_sizes)) != 1:
            raise ValueError("Not all groups have the same number of teams.")

        for group, group_teams in groups.items():
            for i in range(len(group_teams)):
                for j in range(i + 1, len(group_teams)):
                    team1 = group_teams[i]
                    team2 = group_teams[j]

                    is_past_match = random.choice([True, False])
                    if is_past_match:
                        score1 = random.randint(0, 5)
                        score2 = random.randint(0, 5)
                        date = datetime.now() - timedelta(days=random.randint(1, 30))
                    else:
                        score1 = 0
                        score2 = 0
                        date = datetime.now() + timedelta(days=random.randint(1, 30))

                    localization = (random.uniform(-90, 90), random.uniform(-180, 180))

                    scorers = {}
                    if is_past_match:
                        scorers[team1.name] = generate_scorers(db, team1, score1)
                        scorers[team2.name] = generate_scorers(db, team2, score2)

                    match = Match(
                        round=1,
                        teams=[team1.name, team2.name],
                        scores=[score1, score2],
                        date=date.strftime("%Y-%m-%d %H:%M"),
                        stadium=fake.city() + " Stadium",
                        localization=localization,
                        scorers=scorers
                    )

                    db_match = MatchModel(
                        round=match.round,
                        teams=match.teams,
                        scores=match.scores,
                        date=match.date,
                        stadium=match.stadium,
                        localization=list(match.localization),
                        scorers=match.scorers
                    )
                    db.add(db_match)
                    db.commit()

                    if is_past_match:
                        update_team_stats(db, team1.name)
                        update_team_stats(db, team2.name)

    finally:
        db.close()

def generate_scorers(db: Session, team: TeamModel, goals: int) -> list[dict[str, dict]]:
    scorers = []

    players = db.query(PlayerModel).filter_by(team_name=team.name).all()

    for _ in range(goals):
        player = random.choice(players)
        player.goals += 1
        scorers.append({"player": {"name": player.name}, "time": {"minute": str(random.randint(1, 90))}})

    db.commit()
    return scorers

def update_team_stats(db: Session, team_name: str):
    team = db.query(TeamModel).filter_by(team_name=team_name).first()
    if not team:
        return

    matches = db.query(MatchModel).filter(MatchModel.teams.contains(team_name)).all()

    for match in matches:
        match_datetime = datetime.strptime(match.date, "%Y-%m-%d %H:%M")
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


def generate_fake_team(name: str) -> Team:
    return Team(
        name=name,
        total_goals=0,
        conceded_goals=0,
        points=0,
        group=random.choice(["A", "B", "C", "D"])
    )

def generate_fake_player(team_name: str, used_numbers: set) -> Player:
    while True:
        number = random.randint(1, 99)
        if number not in used_numbers:
            used_numbers.add(number)
            break

    return Player(
        name=fake.last_name(),
        number=number,
        team=team_name,
        position=random.choice(POSITIONS),
        is_starting=False,
        goals=random.randint(0, 10)
    )

def generate_fake_data(player_per_team: int, number_of_teams: int, starting_players: int):
    db = SessionLocal()

    try:
        groups = ["A", "B"]

        if number_of_teams % len(groups) != 0:
            raise ValueError(f"The number of teams ({number_of_teams})"
                             f" is not divisible by the number of groups ({len(groups)}).")

        teams_per_group = number_of_teams // len(groups)

        for group in groups:
            for _ in range(teams_per_group):
                team_name = fake.city() + " FC"
                team = generate_fake_team(team_name)
                team.group = group

                db_team = TeamModel(
                    name=team.name,
                    total_goals=team.total_goals,
                    conceded_goals=team.conceded_goals,
                    points=team.points,
                    group=team.group
                )
                db.add(db_team)
                db.commit()
                db.refresh(db_team)

                used_numbers = set()

                players = []
                for _ in range(player_per_team):
                    player = generate_fake_player(team_name, used_numbers)
                    players.append(player)

                for player in players:
                    db_player = PlayerModel(
                        name=player.name,
                        number=player.number,
                        team_name=player.team,
                        position=player.position,
                        is_starting=player.is_starting,
                        goals=player.goals
                    )
                    db.add(db_player)
                    db.commit()
                    db.refresh(db_player)

                starting_players_list = random.sample(players, starting_players)
                for player in starting_players_list:
                    db_player = db.query(PlayerModel).filter(
                        PlayerModel.name == player.name,
                        PlayerModel.team_name == team_name,
                        PlayerModel.number == player.number
                    ).first()

                    if db_player is None:
                        print(f"Player not found: {player.name} (Number: {player.number}, Team: {team_name})")
                        continue

                    db_player.is_starting = True
                    db.commit()

    finally:
        db.close()

Base.metadata.create_all(bind=engine)

generate_fake_data(15, 8, 5)
generate_fake_matches()
