# ONLY FOR ADMINISTRATOR USAGE

import logging
import requests
import os
import random


BASE_URL = "http://127.0.0.1:8000"


def add_user(username: str, number: int, team: str):
    url = f"{BASE_URL}/users/"
    payload = {
        "username": username,
        "number": number,
        "team": team
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        logging.info(response.json())
    else:
        logging.error(f"Error {response.status_code}: {response.json()}")


def add_team(team: str):
    url = f"{BASE_URL}/teams/"
    payload = {"name": team}
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        logging.info(response.json())
    else:
        logging.error(f"Error {response.status_code}: {response.json()}")


def add_match(round_number: int, teams: list[str], scores: list[int]):
    url = f"{BASE_URL}/matches/"
    if len(teams) != len(scores):
        logging.error("The number of teams must match the number of scores")
        return

    payload = {
        "round": round_number,
        "teams": teams,
        "scores": scores
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        logging.info(response.json())
    else:
        logging.error(f"Error {response.status_code}: {response.json()}")


def clear_data():
    files = ["users.json", "teams.json"]
    for file in files:
        if os.path.exists(file):
            os.remove(file)
            logging.info(f"Cleared data from {file}")
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
                username = f"{first_name} {last_name}"
                if username not in players:
                    players.add(username)
                    break
            number = random.randint(1, 99)
            add_user(username, number, team_name)
