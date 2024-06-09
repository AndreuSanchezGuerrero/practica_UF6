from nba_api.stats.endpoints import playergamelogs
import re
import mysql.connector
from mysql.connector import errorcode
from time import sleep

def is_valid_ip(ip):
    pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if pattern.match(ip):
        parts = ip.split(".")
        for part in parts:
            if int(part) < 0 or int(part) > 255:
                return False
        return True
    return False

def connect_to_db(host, user, password, database=None):
    try:
        connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Usuari o contrasenya incorrectes.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: La base de dades no existeix.")
        else:
            print(err)
        return None

def check_user_exists(connection, user):
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM mysql.user WHERE user = %s"
    cursor.execute(query, (user,))
    result = cursor.fetchone()
    return result[0] > 0

def check_database_exists(connection, database):
    cursor = connection.cursor()
    query = "SHOW DATABASES LIKE %s"
    cursor.execute(query, (database,))
    result = cursor.fetchone()
    return result is not None


def main():
    
    # Demanar la IP del host i validar
    while True:
        host = input("Introdueix la IP del host on està la base de dades: ")
        if is_valid_ip(host):
            break
        else:
            print("Error: IP no vàlida. Si us plau, introdueix una IP correcta.")

    # Demanar el nom d'usuari i validar
    while True:
        user = input("Introdueix el nom d'usuari: ")
        password = input("Introdueix la contrasenya: ")

        # Intentar connectar a la base de dades per verificar usuari i contrasenya
        connection = connect_to_db(host, user, password)
        if connection:
            if check_user_exists(connection, user):
                break
            else:
                print("Error: L'usuari no existeix.")
        else:
            print("Error: Usuari o contrasenya incorrectes.")

    # Demanar el nom de la base de dades i validar
    while True:
        database = input("Introdueix el nom de la base de dades: ")
        if check_database_exists(connection, database):
            break
        else:
            print("Error: La base de dades no existeix.")

    # Connexió final a la base de dades específica
    connection = connect_to_db(host, user, password, database)
    if connection:
        print("Connexió exitosa a la base de dades.")
        sleep(1)

    # La resta del codi de processament de dades
    process_data(connection)

def process_data(connection):
    cursor = connection.cursor()

    # Creació de taules
    # ---------------------------------------------------------------------------------------
    def create_seasons():
        print("Creant taula seasons")
        sleep(1)
        cursor.execute("DROP TABLE IF EXISTS seasons")
        crear_taula_seasons = """
        CREATE TABLE IF NOT EXISTS seasons (
            year CHAR(10),
            CONSTRAINT PK_year PRIMARY KEY (year)
        );   
        """
        cursor.execute(crear_taula_seasons)
        print("Taula seasons creada")
        sleep(1)

    def create_teams():
        print("Creant taula teams")
        sleep(1)
        cursor.execute("DROP TABLE IF NOT EXISTS teams")
        crear_taula_teams = """
        CREATE TABLE IF NOT EXISTS teams (
            team_id INT,
            team_name VARCHAR(255),
            team_abbreviation CHAR(3),
            CONSTRAINT PK_team_id PRIMARY KEY (team_id)
        );   
        """
        cursor.execute(crear_taula_teams)
        print("Taula teams creada")
        sleep(1)

    def create_players():
        print("Creant taula players")
        sleep(1)
        cursor.execute("DROP TABLE IF NOT EXISTS players")
        crear_taula_players = """
            CREATE TABLE IF NOT EXISTS players (
                player_id INT NOT NULL,
                player_name VARCHAR(100) NOT NULL,
                player_nickname VARCHAR(100),
                team_id INT,
                team_name VARCHAR(100),
                seasonYear CHAR(10),
                CONSTRAINT PK_player PRIMARY KEY (player_id, team_id, seasonYear),
                CONSTRAINT FK_team_id FOREIGN KEY (team_id) REFERENCES teams(team_id),
                CONSTRAINT FK_seasonYear FOREIGN KEY (seasonYear) REFERENCES seasons(year)
            );  
        """
        cursor.execute(crear_taula_players)
        print("Taula players creada")
        sleep(1)

    def create_games():
        print("Creant taula games")
        sleep(1)
        cursor.execute("DROP TABLE IF NOT EXISTS games")
        crear_taula_games = """
            CREATE TABLE IF NOT EXISTS games (
                game_id VARCHAR(255) PRIMARY KEY,
                season_year CHAR(10),
                home_team_id INT,
                away_team_id INT,
                FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
                FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
            );
        """
        cursor.execute(crear_taula_games)
        print("Taula games creada")
        sleep(1)

    def create_player_stats():
        print("Creant taula playerstats")
        sleep(1)
        cursor.execute("DROP TABLE IF NOT EXISTS playerstats")
        crear_taula_player_stats = """
            CREATE TABLE IF NOT EXISTS playerstats (
                player_id INT,
                game_id VARCHAR(255),
                team_id INT,
                pts FLOAT,
                PRIMARY KEY (player_id, game_id, team_id),
                FOREIGN KEY (team_id) REFERENCES teams(team_id),
                FOREIGN KEY (game_id) REFERENCES games(game_id)
            );
        """
        cursor.execute(crear_taula_player_stats)
        print("Taula playerstats creada")
        sleep(1)
    # ---------------------------------------------------------------------------------------

    # Insercions
    # ---------------------------------------------------------------------------------------
    def insert_player_stats(stats):
        total_stats = len(stats)
        for i, stat in enumerate(stats):
            player_id = stat[0]
            game_id = stat[1]
            team_id = stat[2]
            pts = stat[3]

            insert = """
            INSERT INTO playerstats (player_id, game_id, team_id, pts)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert, [player_id, game_id, team_id, pts])
            connection.commit()
            print(f"Insertant dades {i+1}/{total_stats} en playerstats")
            sleep(0.1)
        print("Dades inserides a la taula playerstats")
        sleep(1)

    def insert_seasons(seasons):
        total_seasons = len(seasons)
        for i, season in enumerate(seasons): 
            insert_season = "INSERT INTO seasons (year) VALUES(%s)"
            cursor.execute(insert_season, [season])
            connection.commit()
            print(f"Insertant dades {i+1}/{total_seasons} en seasons")
            sleep(0.1)
        print("Dades inserides a la taula seasons")
        sleep(1)

    def insert_teams(teams):
        total_teams = len(teams)
        for i, team in enumerate(teams):
            dada = team.split(",")
            team_id = int(dada[0])
            team_name = dada[1]
            team_abbreviation = dada[2]

            insert = "INSERT INTO teams (team_id, team_name, team_abbreviation) VALUES(%s, %s, %s)"
            cursor.execute(insert, [team_id, team_name, team_abbreviation])
            connection.commit()
            print(f"Insertant dades {i+1}/{total_teams} en teams")
            sleep(0.1)
        print("Dades inserides a la taula teams")
        sleep(1)

    def insert_players(players):
        total_players = len(players)
        for i, player in enumerate(players):
            dada = player.split(",")
            playerID = int(dada[0])
            playerName = dada[1]
            playerNickname = dada[2]
            team_id = int(dada[3])
            team_name = dada[4]
            seasonYear = dada[5]

            insert = "INSERT INTO players (player_id, player_name, player_nickname, team_id, team_name, seasonYear) VALUES(%s, %s, %s, %s, %s, %s)"
            cursor.execute(insert, [playerID, playerName, playerNickname, team_id, team_name, seasonYear])
            connection.commit()
            print(f"Insertant dades {i+1}/{total_players} en players")
            sleep(0.1)
        print("Dades inserides a la taula players")
        sleep(1)

    def insert_games(games):
        total_games = len(games)
        processed_games = set()
        for i, game in enumerate(games):
            game_id = game[0]
            if game_id in processed_games:
                continue
            season_year = game[1]
            home_team_id = game[2]
            away_team_id = game[3]

            insert = """
            INSERT INTO games (game_id, season_year, home_team_id, away_team_id)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert, [game_id, season_year, home_team_id, away_team_id])
            connection.commit()
            processed_games.add(game_id)
            print(f"Insertant dades {i+1}/{total_games} en games")
            sleep(0.1)
        print("Dades inserides a la taula games")
        sleep(1)

    # ----------------------------------------------------------------------------------------
    i = 16
    x = 17

    create_seasons()
    create_teams()
    create_players()
    create_games()
    create_player_stats()
    setAnys = set()
    setTeam = set()
    setplayer = set()
    setGames = set()
    setPlayerStats = set()
    processed_game_ids = set()

    while i <= 22:  # Ajustar per processar totes les temporades necessàries
        diccionario = playergamelogs.PlayerGameLogs(season_nullable=f'20{i}-{x}').player_game_logs.get_dict()
        print(f"Processant temporada 20{i}-{x}")  # Impressió de depuració
        for dada in diccionario["data"]:
            # Dades jugador
            playerID = dada[1]
            playerName = dada[2]
            playerNickname = dada[3]
            
            # Dades equip
            teamID = dada[4]
            teamName = dada[6]
            teamAbbreviation = dada[5]

            # Dades temporades
            seasonYear = dada[0]
            playerComplet = (f"{playerID},{playerName},{playerNickname},{teamID},{teamAbbreviation},{seasonYear}")
            teamComplet = (f"{teamID},{teamName},{teamAbbreviation}")
            setplayer.add(playerComplet)
            setTeam.add(teamComplet)
            setAnys.add(seasonYear)

            # Dades partits
            game_id = dada[7]
            matchup = dada[9].split(" ")
            home_team_id = teamID
            away_team_id = None  # Inicialitzar away_team_id

            away_team_abbr = matchup[2]
            
            for team in setTeam:
                if away_team_abbr in team:
                    away_team_id = int(team.split(",")[0])

            # Assegurar-se que away_team_id es defineix
            if away_team_id is not None:
                gameComplet = (game_id, seasonYear, home_team_id, away_team_id)
                setGames.add(gameComplet)
                processed_game_ids.add(game_id)

            # Estadístiques jugador
            pts = dada[31]  # Suposant que aquesta és la columna de punts
            playerStatsComplet = (playerID, game_id, teamID, pts)
            setPlayerStats.add(playerStatsComplet)

            print(f"Processat game_id: {game_id}, player_id: {playerID}, pts: {pts}")  # Impressió de depuració
            sleep(0.00001)
        i += 1
        x += 1

    # Verificar la quantitat de dades recopilades per a cada conjunt
    print(f"Total temporades: {len(setAnys)}")
    print(f"Total equips: {len(setTeam)}")
    print(f"Total jugadors: {len(setplayer)}")
    print(f"Total partits: {len(setGames)}")
    print(f"Total estadístiques jugadors: {len(setPlayerStats)}")

    seasons = list(setAnys)
    teams = list(setTeam)
    players = list(setplayer)
    games = list(setGames)
    player_stats = list(setPlayerStats)

    insert_seasons(seasons)
    insert_teams(teams)
    insert_players(players)
    insert_games(games)
    insert_player_stats(player_stats)

    # ----------------------------------------------------------------------------------------

    print("Procés completat.")  # Missatge de finalització



if __name__ == "__main__":
    main()
