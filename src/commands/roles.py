import time

import discord
from discord import Option, Embed, default_permissions
from discord.ext import commands
from discord.utils import basic_autocomplete

from utils.user.cmd_reward import cmd_reward


class Roles(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot


    @commands.slash_command(name="roles", description="🔄 | Gebe/Lösche Jedem eine Rolle")
    @default_permissions(kick_members=True)
    async def cmd(self, ctx: discord.ApplicationContext,
                  givetake: Option(str, "Zuweisen oder Entfernen",
                                   autocomplete=basic_autocomplete(["Zuweisen", "Entfernen"]),
                                   required=True),
                  role: Option(discord.Role, "Role", required=True)):

        await cmd_reward(ctx)


        guild: discord.Guild = ctx.guild

        member_count = guild.member_count
        emb_title = await self.create_progress_bar(0,member_count, 0)

        if givetake == "Zuweisen":
            await ctx.respond(embed=Embed(color=discord.Color.green(),
                                          title=emb_title,
                                          description=f"Jeder Benutzer erhält die Rolle {role.mention}"),
                              ephemeral=True)

            t1 = time.perf_counter(), time.process_time()
            for count, usr in enumerate(guild.members, 1):
                if not usr.bot and not role in usr.roles:
                    await usr.add_roles(role, atomic=True)

                t2 = time.perf_counter(), time.process_time()
                await ctx.edit(
                    embed=Embed(color=discord.Color.green(),
                                title=await self.create_progress_bar(count, member_count, (t2[0] - t1[0])),
                                description=f"Jeder Benutzer erhält die Rolle {role.mention}"))



        elif givetake == "Entfernen":
            await ctx.respond(embed=Embed(color=discord.Color.green(),
                                          title=emb_title,
                                          description=f"Die Rolle {role.mention} wird von jedem Benutzer entfernt"),
                              ephemeral=True)

            t1 = time.perf_counter(), time.process_time()
            for count, usr in enumerate(guild.members, 1):
                if not usr.bot and role in usr.roles:
                    await usr.remove_roles(role)

                t2 = time.perf_counter(), time.process_time()
                await ctx.edit(
                    embed=Embed(color=discord.Color.green(),
                                title=await self.create_progress_bar(count, member_count, (t2[0] - t1[0])),
                                description=f"Die Rolle {role.mention} wird von jedem Benutzer entfernt"))


    async def create_progress_bar(self, member, member_count, seconds, total_length=10):
        filled_length = int(total_length * member / member_count)
        percentage = round((100 / member_count * member), 1)

        bar = f"|{'█' * filled_length}{' ' * (int((total_length - filled_length) * 3.2))}|"
        stats = f"{member}/{member_count} [{percentage}%] ({seconds:.2f}s)"
        return f"{bar} {stats}"

def setup(client):
    client.add_cog(Roles(client))
