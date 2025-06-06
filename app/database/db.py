import sqlite3
from pathlib import Path

db_path = Path(__file__).parent/"rbcml.db"

def insert(data, table, db=db_path):
    with sqlite3.connect(db) as connection:
        connection.execute("PRAGMA foreign_key = ON");
        cursor = connection.cursor()
        if len(data) == 1:
            query = f"""INSERT INTO {table} ({list(data.keys())[0]})
                            VALUES ('{list(data.values())[0]}')"""
        else:
            query = f"""INSERT INTO {table} {tuple(data.keys())}
                            VALUES {tuple(data.values())}"""
        try:
            cursor.execute(query)
            return "Created", 201
        except Exception as e:
            print(query,'\n',e)
            return "Bad request!", 400

def search(data, key, table, db=db_path):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = f"""SELECT * FROM {table}
                        WHERE {key} = '{data}'"""
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except:
            return []

def exists(data, key, table, db=db_path):
    return len(search(data, key, table, db)) > 0

def delete(data, key, table, db=db_path):
    with sqlite3.connect(db) as connection:
        cursor = connection.cursor()
        query = f"""DELETE FROM {table}
                        WHERE {key} = '{data}'"""
        try:
            cursor.execute(query)
            return "Deleted", 200
        except:
            return "Bad request", 400

