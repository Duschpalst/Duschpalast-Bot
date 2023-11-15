from datetime import datetime
from random import randint

import discord
from discord import Embed
from discord.ext import commands

from static import SQL, db


class Daily(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="daily", description="Hole dir deine Tägliche belohnung ab")
    async def cmd(self, ctx: discord.ApplicationContext):
        user = ctx.user
        SQL.execute(f'SELECT daily FROM users WHERE user_id = {user.id}')
        date = SQL.fetchone()[0]

        now_date = datetime.now().date().strftime("%d.%m")

        if date == now_date:
            await ctx.respond(embed=Embed(color=discord.Color.red(), title="Du hast Bereits deine Tägliche Belohnung abgeholt!"), ephemeral=True)
            return

        coins = randint(50, 100)
        xp = randint(15, 50)

        SQL.execute(f'UPDATE users SET coin = coin + {coins} WHERE user_id = {user.id};')
        SQL.execute(f'UPDATE users SET xp = xp + {xp} WHERE user_id = {user.id};')
        SQL.execute(f'UPDATE users SET daily = {now_date} WHERE user_id = {user.id};')
        db.commit()

        await ctx.respond(embed=Embed(color=discord.Color.green(), title=f"Du erhälst `{xp}` XP und `{coins}` Duschcoins<:duschcoin:1174139658712649729>"), ephemeral=True)


def setup(client):
    client.add_cog(Daily(client))
