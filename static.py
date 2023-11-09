import os
import sqlite3

DIR = os.path.dirname(__file__)
db = sqlite3.connect(os.path.join(DIR, "assets/database.db"))
SQL = db.cursor()


self_roles_messages_id = [1067919658365243463, 1067919659531255979, 1067919661041188894]
lvl_roles_id = [1169061540209627206, 1169061375235076097, 1169061217302757456, 1169061144724504606, 1169061828165369866]

channels_id = {
    "log": 1015678383541211206,
    "welcome": 797094559988711427,
    "self_roles": 998569311369183323,
    "events": 1015680099850408038,


    # Stats Channel
    "all": 1055141450762952774,
    "member": 1055141454730776686,
    "bots": 1055141458774065212,
    "in_voice": 1071784772533223454,
}

invites = []
