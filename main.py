# Es kann sein das die Datei nicht mit der Datei auf dem Server übereinstimmt da bei Test zwecken Funktionen deaktiviert werden oder umgeschrieben werden

# Library Import
import os

import discord

# Files Import
import secret
import static
from assets.create_tables import create_sql_tables
from utils.guilds.update_invites import update_invites

client = discord.Bot(intents=discord.Intents.all())

create_sql_tables()


@client.event
async def on_ready():
    print("Ich bin on!")

    # Code der nur aufm Main Bot funktioniert und nicht auf dem Test Bot
    if client.user.id == static.bot_id:
        await update_invites(client)


cogs_directory = ['src']

# Import all commands Files
for directory in cogs_directory:
    for path, subdirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".py"):
                p = path.replace("/", ".") # Linux
                #p = path.replace("\\", ".") # Windows
                client.load_extension(f"{p}.{name[:-3]}")


client.run(secret.TOKEN)
