from datetime import datetime
from random import randint

import discord
from discord import Embed
from discord.ext import commands

import static
from static import *
from utils.user.add_last_transaction import add_last_transaction


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
            emb = Embed(color=discord.Color.red(),
                        title="Du hast Bereits deine Tägliche Belohnung abgeholt!")
            emb.set_footer(text=static.standard_footer)
            await ctx.respond(embed=emb, ephemeral=True)
            return

        coins = randint(daily_coin_reward_min, daily_coin_reward_max)
        xp = randint(daily_xp_reward_min, daily_xp_reward_max)

        SQL.execute(f'UPDATE users SET coin = coin + {coins} WHERE user_id = {user.id};')
        SQL.execute(f'UPDATE users SET xp = xp + {xp} WHERE user_id = {user.id};')
        SQL.execute(f'UPDATE users SET daily = {now_date} WHERE user_id = {user.id};')
        db.commit()

        SQL.execute(f'SELECT coin FROM users WHERE user_id = {user.id}')
        res = SQL.fetchone()[0]

        emb = discord.Embed(
            title='Deine Täglichen Belohnungen',
            description='Hier sind deine täglichen Belohnungen:',
            color=0x3498db,
        )

        emb.add_field(name="XP", value=f"Du bekommst `{xp}` XP", inline=True)
        emb.add_field(
            name="Coins",
            value=f"Du bekommst `{coins}` Duschcoins <:duschcoin:1174139658712649729>",
            inline=False
        )
        emb.add_field(
            name="Gesamte Duschcoins",
            value=f"Deine Gesamten Duschcoins sind jetzt: `{res}` <:duschcoin:1174139658712649729>",
            inline=False
        )

        emb.set_footer(text=static.standard_footer)

        if not user.avatar:
            emb.set_thumbnail(url=user.default_avatar)
        else:
            emb.set_thumbnail(url=user.avatar.url)

        emb.timestamp = datetime.utcnow()

        await add_last_transaction(user, 'add', 'Tägiche Belohnung abgeholt', coins)
        await ctx.respond(embed=emb, ephemeral=True)


def setup(client):
    client.add_cog(Daily(client))
