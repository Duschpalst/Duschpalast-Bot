import os
import sqlite3

DIR = os.path.dirname(__file__)
db = sqlite3.connect(os.path.join(DIR, "assets/database.db"))
SQL = db.cursor()


standard_footer = "Fragen? Nutze den /faq command"

booster_xp_multiplier = 2

message_xp = 1
call_xp_5min = 10
call_xp_60min = 5

lvl_up_reward = 100

daily_coin_reward_min = 50
daily_coin_reward_max = 100
daily_xp_reward_min = 15
daily_xp_reward_max = 50

self_roles_messages_id = [1174125525892071474, 1174125527058108487, 1174125528136040518]
color_picker_message_id = 1174125529390133249
lvl_roles_id = [1169061540209627206, 1169061375235076097, 1169061217302757456, 1169061144724504606, 1169061828165369866]

bot_id = 1054069404410855466

roles_id = {
    "booster": 853208244721287179,
    "vip": 928786184866508801,
    "bot": 844980448094715947,
}


channels_id = {
    "log": 1015678383541211206,
    "welcome": 797094559988711427,
    "self_roles": 998569311369183323,
    "events": 1015680099850408038,
    "afk": 843754571377147934,


    # Stats Channel
    "all": 1055141450762952774,
    "member": 1055141454730776686,
    "bots": 1055141458774065212,
    "in_voice": 1071784772533223454,
}

basic_cmds = [
    ["</faq:1175468452123783270>\n"
    "Noch nichts eingefügt"],

    ["</help:1175468452123783270>\n"
    "Noch nichts eingefügt"],

    ["</stats:1175468452652253184>\n"
    "Noch nichts eingefügt"],

    ["</tic-tac-toe:1175468452652253184> [User]\n"
    "Noch nichts eingefügt"],

]

lvl_cmds = [
    ["</level:1175468452652253184> (User)\n"
    "Noch nichts eingefügt"],

    ["</leaderboard:1175468452123783270>\n"
    "Die Bestenliste des aktuellen Servers."],

    ["</daily:1175468452123783270>\n"
    "Noch nichts eingefügt"],
]

coins_cmds = [
    ["</wallet:1175468452652253184>\n"
    "Noch nichts eingefügt"],

    ["</daily:1175468452123783270>\n"
    "Noch nichts eingefügt"],
]

admin_cmds = [
    ["</clear:1175468452652253184>\n"
    "Noch nichts eingefügt"],

    ["</remove-level:1175468452652253184>\n"
    "Noch nichts eingefügt"],

    ["</protokoll:1175468452652253184>\n"
    "Noch nichts eingefügt"],

    ["</roles:1175468452652253184>\n"
    "Noch nichts eingefügt"],

    ["</selfroles:1175468452652253184>\n"
    "Noch nichts eingefügt"],
]

invites = []
