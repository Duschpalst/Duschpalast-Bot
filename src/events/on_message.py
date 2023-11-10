import discord
from discord.ext import commands

import static
from static import SQL, db
from utils.user.first_db_write_check import first_write_check
from utils.user.lvl_roles import lvl_roles


class On_Message(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        await first_write_check(message.author)

        role = discord.utils.get(message.guild.roles, id=static.boster_role)
        if role in message.author.roles:
            multiplier = 2
        else:
            multiplier = 1

        SQL.execute(f'UPDATE users SET xp = xp + {multiplier * 1} WHERE user_id = {message.author.id}')
        db.commit()

        if self.bot.user.id == static.bot_id:
            await lvl_roles(message.author)




def setup(client):
    client.add_cog(On_Message(client))
