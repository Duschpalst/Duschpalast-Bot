import discord
from discord.ext import commands

from static import SQL, db


class On_Leave(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_leave(self, member: discord.Member):
        SQL.execute(f'Delete From users WHERE user_id = {member.id};')
        db.commit()




def setup(client):
    client.add_cog(On_Leave(client))
