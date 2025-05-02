import sqlite3


def insert(data, table, db="rbcml.db"):
    with sqlite3.connect(db) as connection:
        connection.execute("PRAGMA foreign_key = ON");
        cursor = connection.cursor()
        query = f"""INSERT INTO {table} {tuple(data.keys())}
                        VALUES {tuple(data.values())}"""
        try:
            cursor.execute(query)
            return (201, "Created")
        except:
            return (400, "Bad request")

