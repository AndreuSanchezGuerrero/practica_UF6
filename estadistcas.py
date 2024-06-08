from nba_api.stats.endpoints import playergamelogs
import re
import mysql.connector
from mysql.connector import errorcode
from time import sleep

conexion = mysql.connector.connect(host='192.168.1.122', user='andreu', password='01011900', database='nba_uf6')
cursor = conexion.cursor()

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
            print("Error: Usuario o contraseña incorrectos.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Base de datos no existe.")
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
    # Pedir la IP del host y validar
    while True:
        host = input("Introduce la IP del host donde está la base de datos: ")
        if is_valid_ip(host):
            break
        else:
            print("Error: IP no válida. Por favor, introduce una IP correcta.")

    # Pedir el nombre de usuario y validar
    while True:
        user = input("Introduce el nombre de usuario: ")
        password = input("Introduce la contraseña: ")

        # Intentar conectar a la base de datos para verificar usuario y contraseña
        connection = connect_to_db(host, user, password)
        if connection:
            if check_user_exists(connection, user):
                break
            else:
                print("Error: El usuario no existe.")
        else:
            print("Error: Usuario o contraseña incorrectos.")

    # Pedir el nombre de la base de datos y validar
    while True:
        database = input("Introduce el nombre de la base de datos: ")
        if check_database_exists(connection, database):
            break
        else:
            print("Error: La base de datos no existe.")

    # Conexión final a la base de datos específica
    connection = connect_to_db(host, user, password, database)
    if connection:
        print("Conexión exitosa a la base de datos.")
        sleep(1)

    # El resto del código de procesamiento de datos
    process_data(connection)

def process_data(connection):
    cursor = connection.cursor()

    # Creates
    # ---------------------------------------------------------------------------------------
    def create_seasons():
        print("Creando tabla seasons")
        sleep(1)
        cursor.execute("DROP TABLE IF EXISTS seasons")
        crear_taula_seasons = """
        CREATE TABLE IF NOT EXISTS seasons (
            year CHAR(10),
            CONSTRAINT PK_year PRIMARY KEY (year)
        );   
        """
        cursor.execute(crear_taula_seasons)
        print("Tabla seasons creada")
        sleep(1)

    def create_teams():
        print("Creando tabla teams")
        sleep(1)
        cursor.execute("DROP TABLE IF EXISTS teams")
        crear_taula_teams = """
        CREATE TABLE IF NOT EXISTS teams (
            team_id INT,
            team_name VARCHAR(255),
            team_abbreviation CHAR(3),
            CONSTRAINT PK_team_id PRIMARY KEY (team_id)
        );   
        """
        cursor.execute(crear_taula_teams)
        print("Tabla teams creada")
        sleep(1)

    def create_players():
        print("Creando tabla players")
        sleep(1)
        cursor.execute("DROP TABLE IF EXISTS players")
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
        print("Tabla players creada")
        sleep(1)

    def create_games():
        print("Creando tabla games")
        sleep(1)
        cursor.execute("DROP TABLE IF EXISTS games")
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
        print("Tabla games creada")
        sleep(1)

    def create_player_stats():
        print("Creando tabla playerstats")
        sleep(1)
        cursor.execute("DROP TABLE IF EXISTS playerstats")
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
        print("Tabla playerstats creada")
        sleep(1)
    # ---------------------------------------------------------------------------------------

    # Insert
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
            print(f"Insertando datos {i+1}/{total_stats} en playerstats")
            sleep(0.1)
        print("Datos insertados en la tabla playerstats")
        sleep(1)

    def insert_seasons(seasons):
        total_seasons = len(seasons)
        for i, season in enumerate(seasons): 
            insert_season = "INSERT INTO seasons (year) VALUES(%s)"
            cursor.execute(insert_season, [season])
            connection.commit()
            print(f"Insertando datos {i+1}/{total_seasons} en seasons")
            sleep(0.1)
        print("Datos insertados en la tabla seasons")
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
            print(f"Insertando datos {i+1}/{total_teams} en teams")
            sleep(0.1)
        print("Datos insertados en la tabla teams")
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
            print(f"Insertando datos {i+1}/{total_players} en players")
            sleep(0.1)
        print("Datos insertados en la tabla players")
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
            print(f"Insertando datos {i+1}/{total_games} en games")
            sleep(0.1)
        print("Datos insertados en la tabla games")
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

    while i <= 22:  # Ajustar para procesar todas las temporadas necesarias
        diccionario = playergamelogs.PlayerGameLogs(season_nullable=f'20{i}-{x}').player_game_logs.get_dict()
        print(f"Processing season 20{i}-{x}")  # Impresión de depuración
        for dada in diccionario["data"]:
            # Dades player
            playerID = dada[1]
            playerName = dada[2]
            playerNickname = dada[3]
            
            # Dades team
            teamID = dada[4]
            teamName = dada[6]
            teamAbbreviation = dada[5]

            # Dades seasons
            seasonYear = dada[0]
            playerComplet = (f"{playerID},{playerName},{playerNickname},{teamID},{teamAbbreviation},{seasonYear}")
            teamComplet = (f"{teamID},{teamName},{teamAbbreviation}")
            setplayer.add(playerComplet)
            setTeam.add(teamComplet)
            setAnys.add(seasonYear)

            # Dades games
            game_id = dada[7]
            matchup = dada[9].split(" ")
            home_team_id = teamID
            away_team_id = None  # Inicializar away_team_id

            away_team_abbr = matchup[2]
            
            for team in setTeam:
                if away_team_abbr in team:
                    away_team_id = int(team.split(",")[0])

            # Asegurarse de que away_team_id se define
            if away_team_id is not None:
                gameComplet = (game_id, seasonYear, home_team_id, away_team_id)
                setGames.add(gameComplet)
                processed_game_ids.add(game_id)

            # Player stats
            pts = dada[31]  # Suponiendo que esta es la columna de puntos
            playerStatsComplet = (playerID, game_id, teamID, pts)
            setPlayerStats.add(playerStatsComplet)

            print(f"Processed game_id: {game_id}, player_id: {playerID}, pts: {pts}")  # Impresión de depuración
            sleep(0.00001)
        i += 1
        x += 1

    # Verificar la cantidad de datos recopilados para cada conjunto
    print(f"Total seasons: {len(setAnys)}")
    print(f"Total teams: {len(setTeam)}")
    print(f"Total players: {len(setplayer)}")
    print(f"Total games: {len(setGames)}")
    print(f"Total player stats: {len(setPlayerStats)}")

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

    # Consulta para sumar los puntos de los jugadores por equipo y partido
    get_team_points_per_game()

    print("Finished processing all data.")  # Mensaje de finalización

def get_team_points_per_game():
    cursor = conexion.cursor()
    query = """
        SELECT 
            g.game_id,
            t1.team_name AS home_team,
            SUM(CASE WHEN ps.team_id = g.home_team_id THEN ps.pts ELSE 0 END) AS home_team_pts,
            t2.team_name AS away_team,
            SUM(CASE WHEN ps.team_id = g.away_team_id THEN ps.pts ELSE 0 END) AS away_team_pts
        FROM 
            games g
        JOIN 
            playerstats ps ON g.game_id = ps.game_id
        JOIN 
            teams t1 ON g.home_team_id = t1.team_id
        JOIN 
            teams t2 ON g.away_team_id = t2.team_id
        GROUP BY 
            g.game_id, t1.team_name, t2.team_name
        ORDER BY 
            g.game_id;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    for row in results:
        print(f"{row[1]} {row[2]} - {row[3]} {row[4]}")

if __name__ == "__main__":
    main()
