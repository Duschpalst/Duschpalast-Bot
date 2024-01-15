import os
import sqlite3

# SQL setup
DIR = os.path.dirname(__file__)
db = sqlite3.connect(os.path.join(DIR, "assets/database.db"))
SQL = db.cursor()

# Special character for formatting
invisible_character = "⠀"

# Default footer for an Embed
standard_footer = "Fragen? Nutze den /help command"

# XP multipliers
booster_xp_multiplier = 2

# XP rewards for various actions
message_xp = 1
cmd_xp = 2
call_xp_5min = 10
call_xp_60min = 5

# Leveling system rewards
lvl_up_reward = 100

# Daily rewards range
daily_coin_reward_min = 50
daily_coin_reward_max = 100
daily_xp_reward_min = 15
daily_xp_reward_max = 50

# Roles everyone becomes on Server Join
join_roles = [1015943649672048660, 1015925203617984593, 1015926714079133736, 1015926956144992327, 843963164056092732]

# Message IDs for self-assignable roles
self_roles_messages_id = [1174125525892071474, 1174125527058108487]#, 1174125528136040518]

# Message ID for the color picker
color_picker_message_id = 1174125529390133249

# Role IDs for leveling roles
lvl_roles_id = [1169061540209627206, 1169061375235076097, 1169061217302757456, 1169061144724504606, 1169061828165369866]

# Bot's user ID
bot_id = 1054069404410855466

# Duschpalast Guild ID
duschpalast_guild_id = 797094559988711424

# Role IDs
roles_id = {
    "booster": 853208244721287179,
    "vip": 928786184866508801,
    "bot": 844980448094715947,
    "d-member": 843963164056092732,
}

# Channel IDs
channels_id = {
    "log": 1015678383541211206,
    "team": 1015678328994271362,
    "welcome": 797094559988711427,
    "general": 843487679265898537,
    "self_roles": 998569311369183323,
    "events": 1015680099850408038,
    "afk": 843754571377147934,
    "news": 1015679592750649365,


    # Stats Channel
    "all": 1055141450762952774,
    "member": 1055141454730776686,
    "bots": 1055141458774065212,
    "in_voice": 1071784772533223454,
}

# Command descriptions
basic_cmds = [
    ["help",
    "Zeige das Hilfemenü an."],

    ["stats",
    "Zeige dir deine Server Statistiken an"],

    ["tic-tac-toe [User]",
    "Spiele gegen einen User Tic Tac Toe"],

]

lvl_cmds = [
    ["level (User)",
    "Zeige deine eigenen Level oder die Level eines anderen Benutzers an."],

    ["leaderboard",
    "Zeige dir die Bestenliste an."],

    ["daily",
    "Hole dir deine täglichen Belohnungen ab."],
]

coins_cmds = [
    ["wallet",
    "Zeige den Stand deiner Duschcoins an."],

    ["daily",
    "Hole dir deine täglichen Belohnungen ab."],
]

admin_cmds = [
    ["clear (Anzahl)",
    "Lösche eine bestimmte Anzahl von Nachrichten."],

    ["remove-level [User] [Level]",
    "Entferne einem Benutzer eine bestimmte Anzahl von Leveln."],

    ["welcome-msg",
     "Verwalte die Willkommensnachricht im Allgemeinchat für neue Mitglieder auf dem Server."],

    ["protokoll",
    "Noch keine Beschreibung vorhanden."],

    ["roles [Geben/Nehmen] [Rolle]",
    "Weise alle Benutzern eine Rolle zu oder nehme sie ihnen weg."],

    ["selfroles",
    "Noch keine Beschreibung vorhanden."],
]

# List to store invites
invites = []
