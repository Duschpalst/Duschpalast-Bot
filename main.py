# Es kann sein das die Datei nicht mit der Datei auf dem Server übereinstimmt da bei Test zwecken Funktionen deaktiviert werden oder umgeschrieben werden

# Library Import
import os

import discord

# Files Import
import secret
from events.user_xp_update import voice_update, message_update
from loop_handler import loops
from static import var_client
from events.on_join import join
from storage.create_tables import create_sql_tables
from user_interactions.self_roles import self_roles

intents = discord.Intents.all()
client = discord.Bot(intents=intents)

create_sql_tables()


@client.event
async def on_ready():
    print("Ich bin on!")
    await var_client(client)
    #await self_roles(client)
    #await loops(client)


@client.event
async def on_member_join(member):
    await join(member, client)


@client.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel:
        bcg = before.channel.guild
    else:
        bcg = None

    if after.channel:
        acg = after.channel.guild
    else:
        acg = None

    if bcg != acg:
        await voice_update(member, before, after)


@client.event
async def on_message(message):
    if message.author.bot:
        return
    await message_update(message)


commands_directory = ['commands', 'money_system/commands']

# Import all commands Files
for directory in commands_directory:
    for path, subdirs, files in os.walk(directory):
        for name in files:
            if name.endswith(".py"):
                p = path.replace("/", ".")
                # p = path.replace("\\", ".")
                client.load_extension(f"{p}.{name[:-3]}")


client.run(secret.Test_bot_TOKEN)
