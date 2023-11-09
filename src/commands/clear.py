import discord
from discord import Option, Embed
from discord.ext import commands


class Clear(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="clear", description="Lösche Nachrichten")
    async def cmd(self, ctx: discord.ApplicationContext, ammount: Option(int, "Anzahl", required=False)):
        ammount = ammount or 1000
        await ctx.respond(embed=Embed(color=discord.Color.green(), title="Done"), view=None)
        await ctx.channel.purge(limit=ammount)


def setup(client):
    client.add_cog(Clear(client))
