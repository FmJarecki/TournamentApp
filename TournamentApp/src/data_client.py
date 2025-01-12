import logging
import requests


BASE_URL = "http://127.0.0.1:8000"

def get_all_users() -> list[dict]:
    url = f"{BASE_URL}/users/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error {response.status_code}: {response.json()}.")
        return [{}]

def get_user(username: str, number: int) -> dict:
    url = f"{BASE_URL}/users/{username}/{number}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        logging.info("User not found.")
        return {}
    else:
        logging.error(f"Error {response.status_code}: {response.json()}.")
        return {}


def get_all_teams() -> list[dict]:
    url = f"{BASE_URL}/teams/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error {response.status_code}: {response.json()}.")
        return [{}]


def get_team(team_name: str) -> dict:
    url = f"{BASE_URL}/teams/"
    response = requests.get(url)
    if response.status_code == 200:
        teams = response.json()
        for team in teams:
            if team["team"] == team_name:
                return team
        logging.info(f"Team {team_name} not found.")
        return {}
    else:
        logging.error(f"Error {response.status_code}: {response.json()}.")
        return {}
