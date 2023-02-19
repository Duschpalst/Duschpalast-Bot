import os
import sqlite3

DIR = os.path.dirname(__file__)
db = sqlite3.connect(os.path.join(DIR, "./../storage/database.db"))
SQL = db.cursor()


def main():
    SQL.execute('SELECT name FROM sqlite_master WHERE type="table";')
    tables = SQL.fetchall()

    print("\nFür welche Tabelle willst du eine neue Spalte erstellen?")
    c1 = 0

    for x in tables:
        print(f"{c1} {x[0]}")
        c1 += 1

    table = int(input("Tabelle: "))
    if table > c1 or table < 0:
        print("ERROR")
        return

    name = input("Name: ")

    types = ["INTEGER", "TEXT", "BLOB", "REAL", "NUMERIC"]

    print("Column type")
    c2 = 0

    for x in types:
        print(f"{c2} {x}")
        c2 += 1

    type = int(input("Type: "))
    if type > c2 or type < 0:
        print("ERROR")
        return

    default = input("Default Value (NULL for None): ")

    SQL.execute(f'alter table {tables[table][0]} add column {name} {types[type]} default {default};')
    db.commit()


main()