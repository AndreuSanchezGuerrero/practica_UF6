from nba_api.stats.endpoints import playergamelogs
import mysql.connector
import sys
from time import sleep

conexion = mysql.connector.connect(host='192.168.1.122', user='andreu', password='01011900', database='nba_uf6')
cursor = conexion.cursor()

# Consulta para sumar los puntos de los jugadores por equipo y partido
def get_team_points_per_game():
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

get_team_points_per_game()