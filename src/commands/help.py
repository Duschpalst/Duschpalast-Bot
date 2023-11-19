import os
from datetime import datetime

import discord
from discord import Embed
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot: discord.Bot = bot

    @commands.slash_command(name="help", description="Brauchst du hilfe?")
    async def cmd(self, ctx: discord.ApplicationContext):
        guild: discord.Guild = ctx.guild

        emb = Embed(
            color=0x36393F, #0x2f3136,
            title="",
            description='> ️<:d_info:1175897319389016125> × Hier findest du **alle relevanten Informationen** zu den **Befehlen** und **weiteren Funktionen** dieses Discord-Bots.',
            )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Help')


        emb.add_field(
            name="<:d_staff:1175897436129079306> | Generelle Server Infos",
            value=f"↣ Mitglier: `{len(guild.members)}`\n"
                  f"↣ Server Owner: \n`{guild.owner}`\n",
            inline=True
        )

        cmd_count = 0
        for path, subdirs, files in os.walk('src/commands'):
            for name in files:
                if name.endswith(".py"):
                    cmd_count += 1

        emb.add_field(
            name="<:d_bot:1175897439375474690> | Generelle Bot Infos",
            value=f"↣ Commands: `{cmd_count}`\n"
                  f"↣ Ping: `{round(self.bot.latency * 1000)}ms`\n",
            inline=True
        )

        emb.add_field(
            name="> Emoji | "
        )

        await ctx.respond(embed=emb, ephemeral=True)


def setup(client):
    client.add_cog(Help(client))
