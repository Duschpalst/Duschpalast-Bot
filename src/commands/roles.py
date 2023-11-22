import discord
from discord import Option, Embed, default_permissions
from discord.ext import commands
from discord.utils import basic_autocomplete


class Roles(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot


    @commands.slash_command(name="roles", description="🔄 | Gebe/Lösche Jedem eine Rolle")
    @default_permissions(kick_members=True)
    async def cmd(self, ctx, givetake: Option(str, "Give or Take", autocomplete=basic_autocomplete(["Give", "Take"]), required=True), role: Option(discord.Role, "Role", required=True)):
        guild: discord.Guild = ctx.guild
        if givetake == "Give":
            await ctx.respond(embed=Embed(color=discord.Color.green(), title="Fertig",
                                          description=f"Jeder User kriegt die Role {role.mention}"),
                              ephemeral=True)
            for i in guild.members:
                await i.add_roles(role, atomic=True)
        elif givetake == "Take":
            await ctx.respond(embed=Embed(color=discord.Color.green(), title="Fertig",
                                          description=f"Jedem User wird die Role {role.mention} weggenommen"),
                              ephemeral=True)
            for i in guild.members:
                await i.remove_roles(role)


        #else:
        #    await ctx.respond(embed=Embed(color=discord.Color.red(), title="Error"),
        #                      ephemeral=True)


def setup(client):
    client.add_cog(Roles(client))
