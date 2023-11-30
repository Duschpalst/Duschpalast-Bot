from ast import literal_eval
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

    @commands.slash_command(name="wallet", description="🏧 | Zeige dir deine Duschcoins an")
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

        emb.add_field(name="**• Rang**",
                      value=f"Du bist auf Rang `{rank}` ",
                      inline=False)

        SQL.execute(f'SELECT transactions FROM users WHERE user_id = {user.id}')
        transactions = SQL.fetchone()[0]
        if transactions:
            transactions = literal_eval(transactions)
            t = ""
            for transac in transactions:
                emoji = "<:d_greenplus:1179883173782503434>" if transac[0] == 'add' else "<:d_redminus:1179883172431933470>"

                t += f"{emoji}`{transac[1]}` {transac[2]}\n"
        else:
            t = "Du hast bis jetzt noch Keine Transaktionen gemacht"

        emb.add_field(name="**• Letzte Transaktion📈📉**",
                      value=f"{t}",
                      inline=False)

        emb.set_footer(text=static.standard_footer)
        emb.timestamp = datetime.utcnow()

        await ctx.respond(embed=emb)

def setup(client):
    client.add_cog(Wallet(client))
