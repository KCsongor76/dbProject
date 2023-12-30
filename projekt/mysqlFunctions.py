import mysql.connector

db_config = {
    'host': "localhost",
    'user': "root",
    'password': "",
    'database': "db_project",
}


def connect_to_db():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    return db, cursor


def close_connection(db, cursor):
    cursor.close()
    db.close()


def create_db():
    db, cursor = connect_to_db()

    # query1 = "CREATE DATABASE IF NOT EXISTS db_project;"
    # cursor.execute(query1)

    cursor.execute("USE db_project")

    query2 = ("CREATE TABLE IF NOT EXISTS teams"
              "("
              "id INT(11) AUTO_INCREMENT PRIMARY KEY,"
              "team_name VARCHAR(255)"
              ")")
    cursor.execute(query2)

    query3 = ("CREATE TABLE IF NOT EXISTS players"
              "("
              "id INT(11) AUTO_INCREMENT PRIMARY KEY,"
              "teams_id INT(11),"
              "player_name VARCHAR(255),"
              "FOREIGN KEY(teams_id) REFERENCES teams(id)"
              ")")
    cursor.execute(query3)

    close_connection(db, cursor)


def team_already_in_db(team_name):
    db, cursor = connect_to_db()

    query = "SELECT team_name FROM teams WHERE team_name = %s"
    cursor.execute(query, (team_name,))
    team = cursor.fetchone()

    close_connection(db, cursor)
    return team is not None


def insert_team(team_name):
    db, cursor = connect_to_db()
    query = "INSERT INTO teams (team_name) VALUES (%s)"
    cursor.execute(query, (team_name,))
    db.commit()

    close_connection(db, cursor)


def insert_player(team_id, player_name):
    db, cursor = connect_to_db()
    query = "INSERT INTO players (teams_id, player_name) VALUES (%s, %s)"
    cursor.execute(query, (team_id, player_name))
    db.commit()

    close_connection(db, cursor)


def read_teams():
    db, cursor = connect_to_db()
    query = "SELECT team_name FROM teams"
    cursor.execute(query)

    teams = [row[0] for row in cursor.fetchall()]
    return teams


def get_team_id(team_name):
    db, cursor = connect_to_db()
    query = "SELECT id FROM teams where team_name = %s"
    cursor.execute(query, (team_name,))

    team_id = cursor.fetchone()[0]
    return team_id


def get_player_id(player_name, teams_id):
    db, cursor = connect_to_db()
    query = "SELECT id FROM players WHERE player_name = %s AND teams_id = %s"
    cursor.execute(query, (player_name, teams_id))
    player_id = cursor.fetchone()[0]
    return player_id


def player_already_in_db(team_id, player_name):
    db, cursor = connect_to_db()

    query = "SELECT player_name FROM players WHERE teams_id = %s AND player_name = %s LIMIT 1"
    cursor.execute(query, (team_id, player_name))
    player = cursor.fetchone()

    close_connection(db, cursor)
    return player is not None
