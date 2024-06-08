from nba_api.stats.endpoints import playergamelogs
import mysql.connector
import sys
from time import sleep

conexion = mysql.connector.connect(host='192.168.1.122', user='andreu', password='01011900', database='nba_uf6')
cursor = conexion.cursor()

# Creates
# ---------------------------------------------------------------------------------------
def create_seasons():
    cursor.execute("DROP TABLE IF EXISTS seasons")
    crear_taula_seasons = """
    CREATE TABLE IF NOT EXISTS seasons (
        year CHAR(10),
        CONSTRAINT PK_year PRIMARY KEY (year)
    );   
    """
    cursor.execute(crear_taula_seasons)

def create_teams():
    crear_taula_teams = """
    CREATE TABLE IF NOT EXISTS teams (
        team_id INT,
        team_name VARCHAR(255),
        team_abbreviation CHAR(3),
        CONSTRAINT PK_team_id PRIMARY KEY (team_id)
    );   
    """
    cursor.execute(crear_taula_teams)

def create_players():
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

def create_games():
    crear_taula_games = """
    CREATE TABLE IF NOT EXISTS games (
        game_id VARCHAR(255),
        season_year CHAR(10),
        CONSTRAINT PK_game_id PRIMARY KEY (game_id)
    );   
    """
    cursor.execute(crear_taula_games)

def create_player_stats():
    crear_taula_player_stats = """
        CREATE TABLE IF NOT EXISTS playerstats (
            player_id INT,
            player_name VARCHAR(255),
            nickname VARCHAR(255),
            team_id INT,
            team_abbreviation VARCHAR(255),
            team_name VARCHAR(255),
            game_id VARCHAR(255),
            game_date DATE,
            matchup VARCHAR(255),
            wl VARCHAR(1),
            min FLOAT,
            fgm INT,
            fga INT,
            fg_pct FLOAT,
            fg3m INT,
            fg3a INT,
            fg3_pct FLOAT,
            ftm INT,
            fta INT,
            ft_pct FLOAT,
            oreb INT,
            dreb INT,
            reb INT,
            ast INT,
            tov INT,
            stl INT,
            blk INT,
            blka INT,
            pf INT,
            pfd INT,
            pts FLOAT,
            plus_minus FLOAT,
            nba_fantasy_pts INT,
            dd2 INT,
            td3 INT,
            wnba_fantasy_pts INT,
            gp_rank INT,
            w_rank INT,
            l_rank INT,
            w_pct_rank INT,
            min_rank INT,
            fgm_rank INT,
            fga_rank INT,
            fg_pct_rank INT,
            fg3m_rank INT,
            fg3a_rank INT,
            fg3_pct_rank INT,
            ftm_rank INT,
            fta_rank INT,
            ft_pct_rank INT,
            oreb_rank INT,
            dreb_rank INT,
            reb_rank INT,
            ast_rank INT,
            tov_rank INT,
            stl_rank INT,
            blk_rank INT,
            blka_rank INT,
            pf_rank INT,
            pfd_rank INT,
            pts_rank INT,
            plus_minus_rank INT,
            nba_fantasy_pts_rank INT,
            dd2_rank INT,
            td3_rank INT,
            wnba_fantasy_pts_rank INT,
            available_flag INT,
            CONSTRAINT PK_player_id PRIMARY KEY (player_id),
            CONSTRAINT FK_team_id FOREIGN KEY (team_id) REFERENCES teams(team_id),
            CONSTRAINT FK_season_year FOREIGN KEY (season_year) REFERENCES seasons(year)
        );
        """
    cursor.execute(crear_taula_player_stats)
# ---------------------------------------------------------------------------------------

# Insert
# ---------------------------------------------------------------------------------------
def insert_player_stats(seasons):
    for season in seasons: 
        diccionario = playergamelogs.PlayerGameLogs(season_nullable=season).player_game_logs.get_dict()
        for dada in diccionario["data"]:
            insert_season = f"INSERT INTO playerstats VALUES({dada})"
            cursor.execute(insert_season)

def insert_seasons(seasons):
    for season in seasons: 
        insert_season = "INSERT INTO seasons (year) VALUES(%s)"
        cursor.execute(insert_season, [season])
        conexion.commit()

def insert_teams(teams):
    for team in teams:
        dada = team.split(",")
        team_id = dada[0]
        team_name = dada[1]
        team_abbreviation = dada[2]

        insert = "INSERT INTO teams (team_id, team_name, team_abbreviation) VALUES(%s, %s, %s)"
        cursor.execute(insert, [team_id, team_name, team_abbreviation])
        conexion.commit()    

def insert_players(players):
    for player in players:
        dada = player.split(",")
        playerID = dada[0]
        playerName = dada[1]
        playerNickname = dada[2]
        team_id = dada[3]
        team_name = dada[4]
        seasonYear = dada[5]

        insert = "INSERT INTO players (player_id, player_name, player_nickname, team_id, team_name, seasonYear) VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert, [playerID, playerName, playerNickname, team_id, team_name, seasonYear])
        conexion.commit()   

# ----------------------------------------------------------------------------------------
i = 16
x = 17

create_seasons()
create_teams()
create_players()
setAnys = set()
setTeam = set()
setplayer = set()
while i != 18:
    diccionario = playergamelogs.PlayerGameLogs(season_nullable=f'20{i}-{x}').player_game_logs.get_dict()
    for dada in diccionario["data"]:
        
        # Dades seasons
        seasonYear = dada[0]
        
        # Dades player
        playerID = dada[1]
        playerName = dada[2]
        playerNickname = dada[3]
        
        # Dades team
        teamID = dada[4]
        teamName = dada[6]
        teamAbbreviation = dada[5]


        #Dades games
        gameID = dada[7]

        playerComplet = (f"{playerID},{playerName},{playerNickname},{teamID},{teamName},{seasonYear}")
        teamComplet = (f"{teamID},{teamName},{teamAbbreviation}")
        setplayer.add(playerComplet)
        setTeam.add(teamComplet)
        setAnys.add(seasonYear)
        print((dada[0]))
        sleep(0.00001)
    i += 1
    x += 1

seasons = list(setAnys)
teams = list(setTeam)
players = list(setplayer)

insert_seasons(seasons)
insert_teams(teams)
insert_players(players)
# ----------------------------------------------------------------------------------------
