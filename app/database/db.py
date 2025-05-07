import sqlite3
from pathlib import Path

db_path = Path(__file__).parent/"rbcml.db"

def insert(data, table, db=db_path):
    with sqlite3.connect(db) as connection:
        connection.execute("PRAGMA foreign_key = ON");
        cursor = connection.cursor()
        query = f"""INSERT INTO {table} {tuple(data.keys())}
                        VALUES {tuple(data.values())}"""
        try:
            cursor.execute(query)
            return (201, "Created")
        except:
            return (400, "Bad request!")

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

