from nba_api.stats.endpoints import playergamelogs
import mysql.connector
import sys
from time import sleep

conexion = mysql.connector.connect(host='10.91.255.121', user='andreu',password='01011900', database='nba_uf6')
cursor = conexion.cursor()

diccionario = diccionario = playergamelogs.PlayerGameLogs(season_nullable=f'20{i}-{x}').player_game_logs.get_dict()

print(diccionario)