import discord
from discord import Option, Embed
from discord.ext import commands


class Test(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="test", description="Test")
    async def cmd(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"**<@&1064167873154646086> In einer Stunde findet ein Event statt!!** \nhttps://discord.gg/Wu9CVP73?event=1171906934836834384")


def setup(client):
    client.add_cog(Test(client))
