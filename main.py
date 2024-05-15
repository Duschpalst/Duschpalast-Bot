# Library Import
import os
import platform
import sys

import discord

# Files Import
import secret
import static
from static import client
from assets.create_tables import create_sql_tables
from utils.guilds.update_invites import update_invites


create_sql_tables()

""""def MyErrorHandler(message):
    static.err_message += message
    print(static.err_message)


sys.stderr.write = MyErrorHandler"""


@client.event
async def on_ready():
    print("Ich bin on!")

    # Code that only works on the Main Bot and not the Test Bot
    if client.user.id == static.bot_id:
        await update_invites(client)


cogs_directory = ['src']

# Import all cogs Files
for directory in cogs_directory:
    for path, subdirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".py"):
                # Replacing directory separator based on the operating system
                if platform.system() == 'Linux':
                    p = path.replace("/", ".")  # Linux
                else:
                    p = path.replace("\\", ".")  # Windows or other

                client.load_extension(f"{p}.{name[:-3]}")


# Run the Bot or the Test Bot based on the operating system
if platform.system() == 'Linux':
    TOKEN = secret.TOKEN  # Linux
else:
    TOKEN = secret.Test_bot_TOKEN  # Windows or other

client.run(TOKEN)
