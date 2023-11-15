from datetime import datetime
import discord
from discord import Embed
from discord.ext import commands

import static
from static import SQL


class Wallet(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="wallet", description="Zeige dir deine Duschcoins an")
    async def cmd(self, ctx: discord.ApplicationContext):
        user: discord.User = ctx.user
        SQL.execute(f'SELECT coin FROM users WHERE user_id = {user.id}')
        coins = SQL.fetchone()[0]

        SQL.execute(f'SELECT COUNT(*) FROM users WHERE coin > {coins};')
        rank = SQL.fetchone()[0] + 1

        emb = Embed(color=user.color,
                    title=f"{user.name}'s Duschcoin Wallet")

        if not user.avatar:
           emb.set_thumbnail(url=str(user.default_avatar))
        else:
            emb.set_thumbnail(url=str(user.avatar.url))

        emb.add_field(name="**• Duschcoins<:duschcoin:1174139658712649729>**",
                      value=f"**Du besitzt  `{coins}` Duschcoins**")

        emb.add_field(name="**• Rank**",
                      value=f"Du bist `{rank}` Rank",
                      inline=False)

        emb.add_field(name="**• Letzte Transaktion**",
                      value=f"Coming Soon",
                      inline=False)

        emb.set_footer(text=static.standard_footer)
        emb.timestamp = datetime.utcnow()

        await ctx.respond(embed=emb)

def setup(client):
    client.add_cog(Wallet(client))
