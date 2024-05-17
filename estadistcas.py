from nba_api.stats.endpoints import playergamelogs
import mysql.connector
import sys
from time import sleep

conexion = mysql.connector.connect(host='10.94.255.24', user='andreu',password='01011900', database='nba_uf6')
cursor = conexion.cursor()


#Creates
#---------------------------------------------------------------------------------------
def create_seasons():
    crear_taula_seasons = """
    CREATE TABLE IF NOT EXISTS seasons (
        year CHAR(7),
        CONSTRAINT PK_year 	PRIMARY KEY (year)
    );   
    """
    cursor.execute(crear_taula_seasons)

def create_players():
    pass

def create_games():
    pass

def create_players_stats():
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
            CONSTRAINT PK_player_id 	PRIMARY KEY (player_id),
            CONSTRAINT FK_season_id FOREIGN KEY REFERENCES temporades(temporada_id)
        );
        """
    cursor.execute(crear_taula_player_stats)
#---------------------------------------------------------------------------------------

#Insert
#---------------------------------------------------------------------------------------
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





i=16
x=17

setAnys = set()
while i!=18:
    diccionario = diccionario = playergamelogs.PlayerGameLogs(season_nullable=f'20{i}-{x}').player_game_logs.get_dict()
    for dada in diccionario["data"]:
        setAnys.add(dada[0])
        print((dada[0]))
        sleep(0.0001)
    i+=1
    x+=1

seasons = setAnys
seasons = list(seasons)


print(seasons)

create_seasons()
insert_seasons(seasons)

# for i in seasons:
# # 

# for i in diccionario["data"]:
#     print(i)

# diccionario = playergamelogs.PlayerGameLogs(season_nullable='2019-20').player_game_logs.get_dict()

# for i in diccionario["headers"]:
#     print(i)

# for i in diccionario["data"]:
#     print(i[0])

# print(diccionario["data"][0])

