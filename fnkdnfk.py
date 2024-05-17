from nba_api.stats.endpoints import playergamelogs
import mysql.connector
import sys
from time import sleep

conexion = mysql.connector.connect(host='10.94.255.24', user='andreu',password='01011900', database='nba_uf6')
cursor = conexion.cursor()

i=16
x=17

setAnys = set()
while i!=24:
    diccionario = diccionario = playergamelogs.PlayerGameLogs(season_nullable=f'20{i}-{x}').player_game_logs.get_dict()
    for dada in diccionario["data"]:
        setAnys.add(dada[0])
        print(dada[0])
        sleep(0.0005)
    i+=1
    x+=1

