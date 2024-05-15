from nba_api.stats.endpoints import playergamelogs
import mysql.connector
import sys

conexion = mysql.connector.connect(host='10.91.255.121', user='andreu',password='01011900', database='nba_uf6')
cursor = conexion.cursor()

crear_taula_seasons = """
CREATE TABLE IF NOT EXISTS seasons (
    year INT
)
"""

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

for i in sys.argv:
    print(i)





cursor.execute(crear_taula_player_stats)




# for i in seasons:
# # diccionario = playergamelogs.PlayerGameLogs(season_nullable=i).player_game_logs.
#     for j in diccionario["data"]:
#         insert

# for i in diccionario["data"]:
#     print(i)

# diccionario = playergamelogs.PlayerGameLogs(season_nullable='2019-20').player_game_logs.get_dict()

# for i in diccionario["headers"]:
#     print(i)

# for i in diccionario["data"]:
#     print(i[0])

# print(diccionario["data"][0])

