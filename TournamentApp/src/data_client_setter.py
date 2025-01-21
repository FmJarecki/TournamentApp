# ONLY FOR ADMINISTRATOR USAGE

import logging
import requests
import os
import random
import functools

from data_client import get_team, get_player
from config import SERVER_URL, Position


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
def add_team(team: str) -> bool:
    if check_team_exists(team):
        logging.warning(f"Team {team} already exists.")
        return False

    url = f"{SERVER_URL}/teams/"
    payload = {"name": team}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    logging.info(f"Added team {team}.")
    return True


@handle_http_errors
def add_match(round_number: int, teams: list[str], scores: list[int]) -> bool:
    if len(teams) != len(scores):
        logging.error("The number of teams must match the number of scores.")
        return False

    for team in teams:
        if not check_team_exists(team):
            logging.error(f"Team {team} does not exist. Cannot add match.")
            return False

    url = f"{SERVER_URL}/matches/"
    payload = {
        "round": round_number,
        "teams": teams,
        "scores": scores
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    logging.info(f"Added match for round {round_number}.")
    return True


def clear_data():
    files = ["players.json", "teams.json"]
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

    teams = []

    # Add teams and players
    for team_index in range(total_teams):
        team_name = f"Team {chr(65 + team_index)}"
        print(team_name)
        if add_team(team_name):
            teams.append(team_name)
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

    num_teams = len(teams)
    if num_teams % 2 == 1:
        teams.append("BYE")

    num_teams = len(teams)
    num_rounds = num_teams - 1
    matches_per_round = num_teams // 2

    for round_num in range(num_rounds):
        for match_index in range(matches_per_round):
            team1 = teams[match_index]
            team2 = teams[-1 - match_index]
            if "BYE" not in (team1, team2):
                add_match(round_num + 1, [team1, team2],[random.randint(0,5), random.randint(0,5)])
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]



