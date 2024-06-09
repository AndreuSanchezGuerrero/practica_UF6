# Projecte d'Inserció de Dades a la Base de Dades de l'NBA

Aquest projecte connecta a una base de dades MySQL, crea diverses taules necessàries per emmagatzemar dades de l'NBA i insereix dades recuperades de l'API de l'NBA. A més, proporciona una funció per sumar els punts dels jugadors per equip i partit. A continuació s'explica cada detall i funció del codi.

## Descripció de les Funcions

### Funcions Auxiliars

#### `is_valid_ip(ip)`

- **Descripció**: Valida si l'string introduida és una adreça IP vàlida. 
- **Retorna**: `True` si l'adreça IP és vàlida, `False` en cas contrari.

#### `connect_to_db(host, user, password, database=None)`

- **Descripció**: Intenta connectar-se a una base de dades MySQL amb les credencials proporcionades.
- **Paràmetres**:
  - `host` (str) - L'adreça IP del servidor de la base de dades.
  - `user` (str) - El nom d'usuari.
  - `password` (str) - La contrasenya.
  - `database` (str, opcional) - El nom de la base de dades a la qual connectar-se.
- **Retorna**: L'objecte de connexió si té èxit, `None` en cas contrari.

#### `check_user_exists(connection, user)`

- **Descripció**: Comprova si un usuari existeix a la base de dades MySQL.
- **Paràmetres**:
  - `connection` (mysql.connector.connection) - L'objecte de connexió a la base de dades.
  - `user` (str) - El nom de l'usuari a comprovar.
- **Retorna**: `True` si l'usuari existeix, `False` en cas contrari.

#### `check_database_exists(connection, database)`

- **Descripció**: Comprova si una base de dades existeix al servidor MySQL.
- **Paràmetres**:
  - `connection` (mysql.connector.connection) - L'objecte de connexió a la base de dades.
  - `database` (str) - El nom de la base de dades a comprovar.
- **Retorna**: `True` si la base de dades existeix, `False` en cas contrari.

### Funció Principal

#### `main()`

- **Descripció**: Funció principal que gestiona el flux de treball complet, incloent la recollida de credencials, la validació i la connexió a la base de dades, així com el processament de les dades.
- **Flux de treball**:
  1. Demana la IP del host i la valida.
  2. Demana el nom d'usuari i la contrasenya, i comprova la seva existència.
  3. Demana el nom de la base de dades i comprova la seva existència.
  4. Es connecta a la base de dades específica i procedeix al processament de les dades.

### Funció de Processament de Dades

#### `process_data(connection)`

- **Descripció**: Processa les dades de l'API de l'NBA i les insereix a les taules de la base de dades.
- **Paràmetres**: `connection` (mysql.connector.connection) - L'objecte de connexió a la base de dades.
- **Sub-funcions**:
  - `create_seasons()`: Crea la taula `seasons`.
  - `create_teams()`: Crea la taula `teams`.
  - `create_players()`: Crea la taula `players`.
  - `create_games()`: Crea la taula `games`.
  - `create_player_stats()`: Crea la taula `playerstats`.
  - `insert_player_stats(stats)`: Insereix les estadístiques dels jugadors a la taula `playerstats`.
  - `insert_seasons(seasons)`: Insereix les temporades a la taula `seasons`.
  - `insert_teams(teams)`: Insereix els equips a la taula `teams`.
  - `insert_players(players)`: Insereix els jugadors a la taula `players`.
  - `insert_games(games)`: Insereix els partits a la taula `games`.

### Funcions de Creació de Taules

Cada funció de creació de taules segueix el mateix format:

- **Descripció**: Crea una taula específica si no existeix.
- **Flux de treball**:
  1. Imprimeix un missatge indicant que està creant la taula.
  2. Fa una pausa amb `sleep(1)`.
  3. Executa l'ordre SQL per crear la taula.
  4. Imprimeix un missatge indicant que la taula ha estat creada.
  5. Fa una pausa amb `sleep(1)`.

### Funcions d'Inserció de Dades

Cada funció d'inserció de dades segueix el mateix format:

- **Descripció**: Insereix dades a una taula específica.
- **Flux de treball**:
  1. Calcula el nombre total de registres a inserir.
  2. Per cada registre:
     - Insereix el registre a la taula.
     - Imprimeix un missatge indicant el progrés de la inserció.
     - Fa una pausa amb `sleep(0.1)`.
  3. Imprimeix un missatge indicant que totes les dades han estat inserides.
  4. Fa una pausa amb `sleep(1)`.

### Funció de Consulta

#### `get_team_points_per_game()`

- **Descripció**: Executa una consulta per sumar els punts dels jugadors per equip i partit, i imprimeix els resultats.
- **Flux de treball**:
  1. Executa la consulta SQL per sumar els punts per equip i partit.
  2. Recupera i imprimeix els resultats en el format `equip_local punts - equip_visitant punts`.

## Execució

Per executar el projecte, simplement cal executar el fitxer principal amb Python:

```bash
python main.py
