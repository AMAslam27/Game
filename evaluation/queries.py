import sqlite3
from pathlib import Path

connection = sqlite3.connect("results/games.sqlite3")
connection.row_factory = sqlite3.Row

queries = Path("evaluation/queries.sql").read_text()

for query in queries.split(";"):
    if not query.strip():
        continue

    cursor = connection.execute(query)

    print("\n" + " | ".join(column[0] for column in cursor.description))
    for row in cursor:
        print(" | ".join(str(value) for value in row))

connection.close()
