# ONLY FOR ADMINISTRATOR USAGE

import logging
import requests
import os
import random
import functools

from data_client import get_team, get_user
from config import SERVER_URL


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
def add_user(username: str, number: int, team: str) -> bool:
    if not check_team_exists(team):
        logging.error(f"Failed to add user {username} (number: {number}) to team {team}.")
        return False

    if get_user(username, number):
        logging.warning(f"User {username} with number {number} already exists.")
        return False

    url = f"{SERVER_URL}/users/"
    payload = {
        "username": username,
        "number": number,
        "team": team
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    logging.info(f"Added user {username} to team {team}.")
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
    files = ["users.json", "teams.json"]
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            logging.info(f"Cleared data from {file}.")
        else:
            logging.info(f"{file} does not exist, nothing to clear.")


def generate_fake_data(players_per_team=15, total_teams=3):
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
        add_team(team_name)

        players = set()
        for _ in range(players_per_team):
            while True:
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                username = f"{first_name}_{last_name}"
                if username not in players:
                    players.add(username)
                    break
            number = random.randint(1, 99)
            add_user(username, number, team_name)
