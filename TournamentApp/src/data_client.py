import logging
import requests
import functools

from config import SERVER_URL


def handle_http_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP error in {func.__name__}: {e}")
            if func.__annotations__.get("return") == list:
                return [{}]
            return {}
    return wrapper


@handle_http_errors
def fetch_data(endpoint: str) -> list[dict] | dict:
    url = f"{SERVER_URL}/{endpoint}/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_all_players() -> list[dict]:
    return fetch_data("players")


def get_player(name: str, number: int) -> dict:
    return fetch_data(f"players/{name}/{number}")


def get_all_teams() -> list[dict]:
    return fetch_data("teams")


def get_team(team_name: str) -> dict:
    return fetch_data(f"teams/{team_name}")


def get_all_players_from_team(team_name: str) -> list[dict]:
    return fetch_data(f"teams/{team_name}/players")