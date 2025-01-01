import sqlite3
import random


# FOR TESTS ONLY
def generate_fake_data():
    def generate_players(players_per_team: int = 15):
        players = []
        team_name = 'Team @'
        for i in range(players_per_team*3):
            if i % players_per_team == 0:
                team_name = team_name[:-1] + chr(ord(team_name[-1]) + 1)
            while True:
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                player = f"{first_name} {last_name}"
                if player not in players:
                    players.append(player)
                    break
            db.add_user(player, random.randint(1, 99), team_name)

    db = TournamentDatabase()
    db.clear_database()

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

    generate_players()
    db.close()


class TournamentDatabase:
    def __init__(self, db_name='test_database.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS teams (
                    team TEXT PRIMARY KEY
                )
            """)

        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    number TEXT,
                    team TEXT,
                    FOREIGN KEY (team) REFERENCES teams (team)
                )
            """)
        self.connection.commit()

    def add_user(self, username, number, team):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, number, team) VALUES (?, ?, ?)",
                (username, number, team)
            )
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def add_team(self, team_name):
        try:
            self.cursor.execute("INSERT INTO teams (team) VALUES (?)", (team_name,))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"Team '{team_name}' already exists.")

    def get_teams(self) -> list[str]:
        self.cursor.execute("SELECT DISTINCT team FROM users")
        return [row[0] for row in self.cursor.fetchall()]

    def get_team_players(self, team) -> list[str]:
        self.cursor.execute('SELECT number, username FROM users WHERE team = ?', (team,))
        return [f'{row[0]}. {row[1]}' for row in self.cursor.fetchall()]

    def get_teams_with_players(self) -> dict[str, list[str]]:
        return {team: self.get_team_players(team) for team in self.get_teams()}

    def get_user_by_username(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def delete_user(self, username):
        self.cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        self.connection.commit()

    def delete_team(self, team_name):
        self.cursor.execute("DELETE FROM users WHERE team_name = ?", (team_name,))
        self.cursor.execute("DELETE FROM teams WHERE team_name = ?", (team_name,))
        self.connection.commit()

    def clear_database(self):
        self.cursor.execute("DELETE FROM users")
        self.connection.commit()

    def close(self):
        self.connection.close()
