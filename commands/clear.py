import discord
from discord import Option, Embed
from discord.ext import commands

from permissions import perms


class Clear(commands.Cog):

    def __init__(self, bot):
        print(f"loaded {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="leaderboard", description="Zeige dir top 10 von den Level an")
    async def cmd(self, ctx, ammount: Option(int, "Anzahl", required=False)):
        if not await perms.check(ctx.author, 1):
            await ctx.respond(embed=Embed(color=discord.Color.red(), title="Du hast keine Rechte für den Befehl!"), ephemeral=True)
            return
        ammount = ammount or 1000
        await ctx.channel.purge(limit=ammount)
        await ctx.respond(embed=Embed(color=discord.Color.green(), title="Done"), view=None)


def setup(client):
    client.add_cog(Clear(client))
