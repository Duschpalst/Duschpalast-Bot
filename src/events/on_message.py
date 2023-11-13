import discord
from discord.ext import commands

import static
from static import SQL, db
from utils.user.first_db_write_check import first_write_check
from utils.user.lvl_roles import lvl_roles
from utils.user.lvl_up_rewards import lvl_up_rewards


class On_Message(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        user = message.author
        if user.bot:
            return

        await first_write_check(user)

        role = discord.utils.get(message.guild.roles, id=static.boster_role)
        if role in user.roles:
            xp = 2
        else:
            xp = 1

        await lvl_up_rewards(user, xp)

        SQL.execute(f'UPDATE users SET xp = xp + {xp} WHERE user_id = {user.id}')
        SQL.execute(f'UPDATE users SET msg_count = msg_count + 1 WHERE user_id = {user.id}')
        db.commit()

        if self.bot.user.id == static.bot_id:
            await lvl_roles(user)




def setup(client):
    client.add_cog(On_Message(client))
