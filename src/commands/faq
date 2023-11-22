import discord
from discord import Option, Embed
from discord.ext import commands


class Faq(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="faq", description="Hast du generelle Fragen?")
    async def cmd(self, ctx: discord.ApplicationContext):
        await ctx.respond(embed=Embed(
            color=discord.Color.green(),
            title="Klicke hier, um zum FAQ zu kommen",
            url='https://github.com/Duschpalst/Duschpalast-Bot#faq'
        ), ephemeral=True)


def setup(client):
    client.add_cog(Faq(client))
