import discord
from discord import Option, Embed, default_permissions
from discord.ext import commands

from utils.user.cmd_reward import cmd_reward


class Clear(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="clear", description="🗑️ | Lösche Nachrichten")
    @default_permissions(kick_members=True)
    async def cmd(self, ctx: discord.ApplicationContext, ammount: Option(int, "Anzahl", required=False)):
        await cmd_reward(ctx)

        ammount = ammount or 1000
        await ctx.respond(embed=Embed(color=discord.Color.green(), title="Done"), ephemeral=True)
        await ctx.channel.purge(limit=ammount)


def setup(client):
    client.add_cog(Clear(client))
