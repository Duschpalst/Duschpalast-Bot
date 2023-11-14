import discord
from discord import Embed
from discord.ext import commands

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

        emb = Embed(color=0x8000ff,
                    title=f"{user.name} Wallet")

        if not user.avatar:
           emb.set_thumbnail(url=str(user.default_avatar))
        else:
            emb.set_thumbnail(url=str(user.avatar.url))

        emb.add_field(name="**• Coins<:duschcoin:1095835086403940352>**",
                      value=f"**`{coins}`**")

        emb.add_field(name="**• Rank**",
                      value=f"`{rank}`",
                      inline=True)

        await ctx.respond(embed=emb)

def setup(client):
    client.add_cog(Wallet(client))
