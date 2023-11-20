import os
from datetime import datetime

import discord
from discord import Embed
from discord.ext import commands
from discord.ui import View, Button, Select


class Help(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot: discord.Bot = bot
        self.guild = None


    @commands.slash_command(name="help", description="Brauchst du hilfe?")
    async def cmd(self, ctx: discord.ApplicationContext):
        self.guild: discord.Guild = ctx.guild

        await ctx.respond(embed=await self.start_page(), view=await self.view(), ephemeral=True)

    async def view(self):
        v = View(timeout=None)

        categories_list = [
            ["Startseite", "Kehre zur Sartseite zurück", "<:d_compass:1175897308911640686>"],
            ["Commands", "Befehle die jeder Nutzer ausführen kann.", "<:d_slashcommand:1176228551050154045>"],
            ["Wie das Level System funktioniert", "Zeige dir alles zum Level System an", "<:d_metrics:1176229778177658961>"],
            ["Wie das Coins System funktioniert", "Zeige dir alles zum Coins System an", "<:d_creditcard:1176229782833348709>"],
        ]

        categories = Select(
            placeholder=f"Kategorien",
            options=[discord.SelectOption(
                label=x[0],
                description=x[1],
                emoji=x[2],
                value=str(id)
            ) for id, x in enumerate(categories_list, 1)
            ],
            min_values=1,
            max_values=1
        )

        v.add_item(categories)


        button1 = Button(label="Ideen / Bugs", custom_id="ideas_bug", style=discord.ButtonStyle.blurple)
        button2 = Button(label="Frage nicht gefunden?", custom_id="question", style=discord.ButtonStyle.green)

        v.add_item(button1)
        v.add_item(button2)

        return v

    async def start_page(self):
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
            value=f"↣ Mitglier: `{len(self.guild.members)}`\n"
                  f"↣ Server Owner: \n`{self.guild.owner}`\n",
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

        """emb.add_field(
            name="> Emoji | "
        )"""

        return emb


    async def cmd_page(self):
        emb = Embed(
            color=0x36393F,  # 0x2f3136,
            title="",
            description='><:d_category:1175897311784742942> × Hier findest du **alle Befehle** die du nutzten kannst.',
        )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Help')

        #emb.add_field(
        #    name="> Emoji | "
        #)

        return emb


def setup(client):
    client.add_cog(Help(client))
