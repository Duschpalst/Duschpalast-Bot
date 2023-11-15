import asyncio

import discord.errors
from discord.ext import commands

import static


class Status_Changer(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Tasks {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(status_changer(self.bot, 30))


def setup(client):
    client.add_cog(Status_Changer(client))


async def status_changer(client, time):
    while True:
        try:
            await client.hange_presence(activity=discord.Game(name=f"👋 {static.new_user_name}"))
            await asyncio.sleep(time)
            await client.change_presence(activity=discord.Game(name="/faq für Fragen"))
            await asyncio.sleep(time)

        except discord.errors.DiscordServerError:
            continue
