import asyncio
import json

import discord.errors
from discord.ext import commands

import static


class Status_Changer(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Tasks {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.user.id == static.bot_id:
            self.bot.loop.create_task(status_changer(self.bot, 30))


def setup(client):
    client.add_cog(Status_Changer(client))


async def status_changer(client, time):
    while True:
        try:
            with open('assets/json/new_user.json', 'r') as f:
                data = json.load(f)
            await client.change_presence(activity=discord.Game(name=f"👋 {data['name']}"))
            await asyncio.sleep(time)

            await client.change_presence(activity=discord.Game(name="/help für Fragen"))
            await asyncio.sleep(time)

            guild: discord.Guild = (await client.fetch_channel(static.channels_id['all'])).guild
            events = await guild.fetch_scheduled_events()
            for event in events:
                if event.status.value == 2:
                    await client.change_presence(activity=discord.Activity(name="Event", type=5))
                    await asyncio.sleep(time)

        except discord.errors.DiscordServerError:
            continue
