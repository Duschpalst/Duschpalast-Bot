# Es kann sein das die Datei nicht mit der Datei auf dem Server übereinstimmt da bei Test zwecken Funktionen deaktiviert werden oder umgeschrieben werden

# Library Import
import os

import discord

# Files Import
import secret
from assets.create_tables import create_sql_tables
from utils.guilds.update_invites import update_invites

client = discord.Bot(intents=discord.Intents.all())

create_sql_tables()


@client.event
async def on_ready():
    print("Ich bin on!")

    # Code der nur aufm Main Bot funktioniert und nicht auf dem Test Bot
    if client.user.id == 1054069404410855466:
        await update_invites(client)


cogs_directory = ['src']

# Import all commands Files
for directory in cogs_directory:
    for path, subdirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".py"):
                #p = path.replace("/", ".")
                p = path.replace("\\", ".")
                client.load_extension(f"{p}.{name[:-3]}")


client.run(secret.Test_bot_TOKEN)
