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
def fetch_data(endpoint: str, resource_id: str = None) -> list[dict] | dict:
    url = f"{SERVER_URL}/{endpoint}/"
    if resource_id:
        url += f"{resource_id}/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_all_users() -> list[dict]:
    return fetch_data("users")


def get_user(username: str, number: int) -> dict:
    return fetch_data("users", f"{username}/{number}")


def get_all_teams() -> list[dict]:
    return fetch_data("teams")


def get_team(team_name: str) -> dict:
    teams = fetch_data("teams")
    return next((team for team in teams if team["name"] == team_name), {})
