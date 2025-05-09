# Before run the test, initialize test.db with the test.sql file
# use the command: sqlite3 test.db < test.sql

from pathlib import Path
from ...app.database.db import exists

db_path = Path(__file__).parent/"test.db"

assert exists("cyber_bob", "Tag", "User", db_path) == True
assert exists("alice", "Tag", "User", db_path) == False
assert exists(1, "Id", "Model", db_path) == True
assert exists(2, "Id", "Model", db_path) == False
assert exists(1, "Id", "Session", db_path) == True
assert exists(2, "Id", "Session", db_path) == False
