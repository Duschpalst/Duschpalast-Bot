import discord
from discord.ext import commands

import static
from utils.guilds.update_invites import update_invites


class On_Invite_Create(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_invite_create(self, member: discord.Member):
        if self.bot.user.id == static.bot_id:
            await update_invites(self.bot)



def setup(client):
    client.add_cog(On_Invite_Create(client))
