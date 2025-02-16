import logging
import requests
import functools
import os

from config import SERVER_URL, IMAGES_PATH


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
def fetch_data(endpoint: str, binary: bool = False) -> list[dict] | dict | bytes | None:
    url = f"{SERVER_URL}/{endpoint}/"
    response = requests.get(url)
    response.raise_for_status()

    if binary:
        return response.content
    else:
        return response.json()


def get_all_players() -> list[dict]:
    return fetch_data("players")


def get_player(name: str, number: int) -> dict:
    return fetch_data(f"players/{name}/{number}")


def get_all_teams() -> list[dict]:
    return fetch_data("teams")


def get_team(team_id: int) -> dict:
    return fetch_data(f"teams/{team_id}")


def download_logos():
    save_dir = f"{IMAGES_PATH}/logos"
    os.makedirs(save_dir, exist_ok=True)
    teams = get_all_teams()

    for team in teams:
        team_id = team.get("id")
        save_logo_path = os.path.join(save_dir, f"{team_id}.png")

        logo_data = fetch_data(f"teams/{team_id}/logo", binary=True)
        if not logo_data:
            logging.error(f"Failed to download team {team_id} logo.")
            continue

        with open(save_logo_path, "wb") as file:
            file.write(logo_data)


def get_all_players_from_team(team_id: int) -> list[dict]:
    return fetch_data(f"teams/{team_id}/players")


def get_teams_from_group(group: str) -> list[dict]:
    return fetch_data(f"teams/group/{group}")


def get_time_sorted_matches() -> list[dict]:
    return fetch_data(f"sorted_time_matches")
