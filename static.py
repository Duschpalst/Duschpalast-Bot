import os
import sqlite3

DIR = os.path.dirname(__file__)
db = sqlite3.connect(os.path.join(DIR, "./storage/database.db"))
SQL = db.cursor()


self_roles_messages_id = [1067919658365243463, 1067919659531255979, 1067919661041188894]

all_items = {
    "Schaufel": "shovel",
    "Hammer": "hammer"
}

all_boosts = {
    "2x 1h": "",
    "2x 8h": "",
    "2x 24h": "",
    "10x 1h": "",
    "10x 2h": "",
    "100x 1h": "",
}
