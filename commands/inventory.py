import discord
from discord import Embed
from discord.ext import commands

from static import SQL, all_items, all_boosts
from utils.guilds.get_emoji import get_emoji


class Inventory(commands.Cog):

    def __init__(self, bot):
        print(f"loaded {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="inventory", description="Zeige dir dein Inventar an")
    async def cmd(self, ctx: discord.ApplicationContext):

        SQL.execute(f'SELECT inventory From users WHERE user_id = {ctx.author.id}')
        inv = eval(SQL.fetchone()[0])

        items = [f"**{inv['items'].count(i)}** x {i} :{all_items[i]}:" for i in all_items if i in inv['items']]
        items = "\n".join(items) if len(items) > 1 else "Keine Items im Inventar"

        boosts = [f"**{inv['boosts'].count(i)}** x {i} :{all_boosts[i]}:" for i in all_boosts if i in inv['boosts']]
        boosts = "\n".join(boosts) if len(boosts) > 1 else "Du besitz keine Boosts"

        emb = discord.Embed(title="Inventar", description="In deinem Inventar sind folgende Sachen", color=ctx.author.color)
        emb.add_field(name="Items", value=items)
        emb.add_field(name="Booster", value=boosts)
        emb.add_field(name="Guthaben", value=f"{inv['balance']} {await get_emoji('duschcoin')}")

        f = discord.File("./img/chest_inv.png")
        emb.set_thumbnail(url="attachment://chest_inv.png")
        await ctx.respond(file=f, embed=emb, ephemeral=True)



def setup(client):
    client.add_cog(Inventory(client))
