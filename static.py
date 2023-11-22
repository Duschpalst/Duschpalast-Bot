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
    ["faq",
    "Noch nichts eingefügt"],

    ["help",
    "Noch nichts eingefügt"],

    ["stats",
    "Noch nichts eingefügt"],

    ["tic-tac-toe [User]",
    "Noch nichts eingefügt"],

]

lvl_cmds = [
    ["level (User)",
    "Zeige dir deine Level oder die Level von einem User an."],

    ["leaderboard",
    "Zeige dir die Bestenliste an."],

    ["daily",
    "Hol dir deine Tägliche Belohnungen ab."],
]

coins_cmds = [
    ["wallet",
    "Zeige dir deine Duschcoins an."],

    ["daily",
    "Hol dir deine Tägliche Belohnungen ab."],
]

admin_cmds = [
    ["clear (Anzahl)",
    "Lösche Nachrichten"],

    ["remove-level [Uer] [Level]",
    "Entferne von einem User Level"],

    ["protokoll",
    "Noch nichts eingefügt"],

    ["roles",
    "Noch nichts eingefügt"],

    ["selfroles",
    "Noch nichts eingefügt"],
]

invites = []
