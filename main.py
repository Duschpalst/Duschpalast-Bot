# Library Import
import os
import platform
import sys

import discord


# Files Import
import secret
import static
from assets.create_tables import create_sql_tables
from utils.guilds.update_invites import update_invites

client = discord.Bot(intents=discord.Intents.all())

create_sql_tables()

""""def MyErrorHandler(message):
    static.err_message += message
    print(static.err_message)


sys.stderr.write = MyErrorHandler"""



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
                if platform.system() == 'Linux':
                    p = path.replace("/", ".") # Linux
                else:
                    p = path.replace("\\", ".") # Windows

                client.load_extension(f"{p}.{name[:-3]}")


client.run(secret.Test_bot_TOKEN)
