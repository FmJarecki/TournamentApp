# ONLY FOR ADMINISTRATOR USAGE
import functools
import logging
import os
import random
from datetime import datetime, timedelta

import requests
from fastapi import HTTPException

from config import SERVER_URL, Position
from data_server import teams, players, find_team, find_player
from data_server import Player


def get_player(player_name: str, player_number: int) -> dict:
    try:
        return find_player(player_name, player_number)
    except HTTPException:
        return {}


def get_teams() -> list[dict]:
    return teams


def get_all_players_from_team(team_name: str) -> list[dict]:
    return [player for player in players if player["team"] == team_name]


def get_team(team_name: str) -> dict:
    try:
        return find_team(team_name)
    except HTTPException:
        return {}


def handle_http_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP error in {func.__name__}: {e}")
            return False
    return wrapper


def check_team_exists(team: str) -> bool:
    return bool(get_team(team))


@handle_http_errors
def add_player(name: str, number: int, team: str, position: Position, is_starting: bool) -> bool:
    if not check_team_exists(team):
        logging.error(f"Failed to add player {name} (number: {number}) to team {team}.")
        return False

    if get_player(name, number):
        logging.warning(f"Player {name} with number {number} already exists.")
        return False

    url = f"{SERVER_URL}/players/"
    payload = {
        "name": name,
        "number": number,
        "team": team,
        "position": position,
        "is_starting": is_starting
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    logging.info(f"Added player {name} to team {team}.")
    return True


@handle_http_errors
def add_team(team: str, group: str = '') -> bool:
    if check_team_exists(team):
        logging.warning(f"Team {team} already exists.")
        return False

    url = f"{SERVER_URL}/teams/"
    payload = {"name": team,
               "group": group}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    logging.info(f"Added team {team}.")
    return True


@handle_http_errors
def add_match(round: int, teams: list[str], scores: list[int], date: str, stadium: str, localization: tuple[float, float],
              scorers: dict) -> bool:
    if scorers is None:
        scorers = [{}]
    if len(teams) != len(scores):
        logging.error("The number of teams must match the number of scores.")
        return False

    for team in teams:
        if not check_team_exists(team):
            logging.error(f"Team {team} does not exist. Cannot add match.")
            return False

    url = f"{SERVER_URL}/matches/"
    payload = {
        "round": round,
        "teams": teams,
        "scores": scores,
        "date": date,
        "stadium": stadium,
        "localization": localization,
        "scorers": scorers
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    logging.info(f"Added match for round {round}.")
    return True


def clear_data():
    files = ["players.json", "teams.json", "matches.json"]
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            logging.info(f"Cleared data from {file}.")
        else:
            logging.info(f"{file} does not exist, nothing to clear.")


def generate_fake_data(players_per_team: int = 15, total_teams: int = 3) -> None:
    first_names = [
        "Anna", "Maria", "Giulia", "Sofia", "Alessia", "Martina", "Chiara", "Giorgia",
        "Elena", "Francesca", "Arianna", "Rebecca", "Valentina", "Camilla", "Alice",
        "Sara", "Beatrice", "Silvia", "Isabella", "Martina", "Ludovica", "Giada",
        "Noemi", "Caterina", "Marta", "Clara", "Viviana", "Letizia", "Raffaella",
        "Tiziana", "Ginevra", "Zoe", "Lucia", "Sabrina", "Elisa", "Giovanna",
        "Benedetta", "Diana", "Monica", "Lorenza", "Francesca", "Patrizia",
        "Tamara", "Giuliana", "Piera", "Samantha", "Alberta", "Filomena"
    ]

    last_names = [
        "Rossi", "Ferrari", "Esposito", "Russo", "Colombo", "Ricci", "Marino",
        "Conti", "Bianchi", "Moretti", "Gallo", "Greco", "Sorrentino", "Lombardi",
        "Fabbri", "Barbieri", "Giordano", "Pellegrini", "Rinaldi", "Carbone",
        "Giusti", "Martini", "De Luca", "Rinaldi", "Cattaneo", "Caputo",
        "Bianco", "Testa", "Santi", "Crispo", "Marra", "Vitale", "Palmieri",
        "Rossetti", "D'Amico", "Bruno", "Conti", "Pavan", "Lazzaro",
        "Mariani", "Mancini", "Ruggiero", "Palumbo", "Serafini", "Fontana"
    ]

    for team_index in range(total_teams):
        team_name = f"Team {chr(65 + team_index)}"
        group_name: str = 'A' if team_index<total_teams//2 else 'B'
        add_team(team_name, group_name)
        players = set()
        positions = list(Position)

        starting_positions = [Position.GK, Position.LB, Position.RB, Position.LM, Position.RM]

        for position in starting_positions:
            while True:
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                name = f"{first_name} {last_name}"
                if name not in players:
                    players.add(name)
                    break

            number = random.randint(1, 99)
            add_player(name, number, team_name, position, is_starting=True)

        for _ in range(players_per_team - 5):
            while True:
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                name = f"{first_name} {last_name}"
                if name not in players:
                    players.add(name)
                    break

            number = random.randint(1, 99)
            position = random.choice(positions)
            add_player(name, number, team_name, position, is_starting=False)

    def assign_goals_to_players(team_players: list[dict], num_goals: int, match_start_time: datetime) -> list[
        dict[str, Player]]:
        scorers = []
        for _ in range(num_goals):
            goal_time = match_start_time + timedelta(minutes=random.randint(1, 40))
            goal_time_str = goal_time.strftime("%H:%M")

            scorer = random.choice(team_players)
            scorer["goals"] += 1

            scorers.append({goal_time_str: scorer})
        return scorers


    teams = get_teams()
    current_time = datetime.now()
    for i in range(0, len(teams), 2):
        match_time = current_time - timedelta(hours=i)

        team_a_name = teams[i]["name"]
        team_b_name = teams[i+1]["name"]

        team_a_players = get_all_players_from_team(team_a_name)
        team_b_players = get_all_players_from_team(team_b_name)

        team_a_goals = random.randint(0, 5)
        team_b_goals = random.randint(0, 5)
        team_a_scorers = assign_goals_to_players(team_a_players, team_a_goals, match_time)
        team_b_scorers = assign_goals_to_players(team_b_players, team_b_goals, match_time)

        scorers = {
            "team_1": team_a_scorers,
            "team_2": team_b_scorers,
        }

        add_match(
            round=1,
            teams=[teams[i]["name"], teams[i+1]["name"]],
            scores=[team_a_goals, team_b_goals],
            date=match_time.strftime("%Y-%m-%d %H:%M"),
            stadium=f"Stadium {i}",
            localization=(1.0, 1.0),
            scorers=scorers
        )

    tomorrow = current_time + timedelta(days=1)
    for i in range(0, len(teams)//4):
        match_time = tomorrow + timedelta(hours=i)
        add_match(
            round=2,
            teams=[teams[i]["name"], teams[i+2]["name"]],
            scores=[0, 0],
            date=match_time.strftime("%Y-%m-%d %H:%M"),
            stadium=f"Stadium {i}",
            localization=(3.0, 3.0),
            scorers={}
        )
    for i in range(len(teams)//2, 3*len(teams)//4):
        match_time = tomorrow + timedelta(hours=i)
        add_match(
            round=2,
            teams=[teams[i]["name"], teams[i+2]["name"]],
            scores=[0, 0],
            date=match_time.strftime("%Y-%m-%d %H:%M"),
            stadium=f"Stadium {i}",
            localization = (2.0, 2.0),
            scorers={}
        )
