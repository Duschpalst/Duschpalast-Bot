import os
from datetime import datetime

import discord
from discord import Embed
from discord.ext import commands
from discord.ui import View, Button, Select

from static import basic_cmds, lvl_cmds, coins_cmds, admin_cmds


class Help(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot: discord.Bot = bot
        self.guild = None


    @commands.slash_command(name="help", description="Brauchst du hilfe?")
    async def cmd(self, ctx: discord.ApplicationContext):
        self.guild: discord.Guild = ctx.guild

        if ctx.author.guild_permissions.kick_members:
            admin = True
        else:
            admin = False

        await ctx.respond(embed=await self.start_page(), view=await self.view(admin), ephemeral=True)

    async def view(self, admin=False):
        v = View(timeout=900)

        categories_list = [
            ["Startseite", "Kehre zur Sartseite zurück", "<:d_compass:1175897308911640686>"],
            ["Commands", "Befehle die jeder Nutzer ausführen kann.", "<:d_slashcommand:1176228551050154045>"],
            ["Wie das Level System funktioniert", "Zeige dir alles zum Level System an", "<:d_metrics:1176229778177658961>"],
            ["Wie das Duschcoins System funktioniert", "Zeige dir alles zum Duschcoins System an", "<:d_creditcard:1176229782833348709>"],
        ]

        admin_categories_list = [
            ["Moderation Commands", "Noch nichts eingefügt", "<:d_settings:1175897310471913543>"],
        ]

        if admin:
            for i in admin_categories_list:
                categories_list.append(i)


        categories = Select(
            placeholder=f"Kategorien",
            options=[discord.SelectOption(
                label=x[0],
                description=x[1],
                emoji=x[2],
                value=str(id)
            ) for id, x in enumerate(categories_list, 0)
            ],
            min_values=1,
            max_values=1
        )

        async def callback(interaction: discord.Interaction):
            if categories.values[0] == "0":
                emb = await self.start_page()
            elif categories.values[0] == "1":
                emb = await self.cmd_page()
            elif categories.values[0] == "2":
                emb = await self.lvl_page()
            elif categories.values[0] == "3":
                emb = await self.coins_page()
            elif categories.values[0] == "4":
                emb = await self.moderation_page()

            else:
                emb = await self.start_page()

            await interaction.response.edit_message(embed=emb)



        categories.callback = callback
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
            description='> <:d_category:1175897311784742942> × Hier findest du **alle Befehle** die du nutzten kannst. (Optional) [Verpflichtend]',
        )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Help')

        for cmd in basic_cmds:
            cmd_name, cmd_options = cmd[0].split(" ", 1)
            cmd_id = 1
            for command in self.bot.commands:
                if command.name == cmd_name:
                    cmd_id = command.id

            emb.add_field(
                name="",
                value=f"</{cmd_name}:{cmd_id}> {cmd_options}\n{cmd[1]}",
                inline=False
            )

        return emb

    async def lvl_page(self):
        emb = Embed(
            color=0x36393F,  # 0x2f3136,
            title="",
            description='> <:d_metrics:1176229778177658961> × Hier findest du alle wichtige **Informationen** und **Befehle** zum Level System. (Optional) [Verpflichtend]',
        )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Help')

        emb.add_field(
            name="EMOJI | Level-System:",
            value=f"↣ Basis-XP für ein Level: `250 XP`\n"
                  f"↣ XP-Inkrement pro Level: `10 XP`",
            inline=True
        )

        emb.add_field(
            name="EMOJI | XP verdienen:",
            value=f"↣ Booster: XP * 2\n"
                  f"↣ Pro Nachricht: `1 XP`\n"
                  f"↣ Pro 5 Min im Sprachkanal: `10 XP`\n"
                  f"↣ `+5 XP` pro Stunde\n"
                  f"Durch </daily:1175468452123783270>: Täglich `15-50` XP",
            inline=True
        )

        emb.add_field(
            name="EMOJI | Level Commands",
            value="",
            inline=False
        )

        for cmd in lvl_cmds:
            cmd_name, cmd_options = cmd[0].split(" ", 1)
            cmd_id = 1
            for command in self.bot.commands:
                if command.name == cmd_name:
                    cmd_id = command.id

            emb.add_field(
                name="",
                value=f"</{cmd_name}:{cmd_id}> {cmd_options}\n{cmd[1]}",
                inline=False
            )

        return emb


    async def coins_page(self):
        emb = Embed(
            color=0x36393F,  # 0x2f3136,
            title="",
            description='> <:d_creditcard:1176229782833348709> × Hier findest du alle wichtige **Informationen** und **Befehle** zum Duschcoin System. (Optional) [Verpflichtend]',
        )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Help')

        emb.add_field(
            name="EMOJI | Duschcoins verdienen:",
            value=f"↣ Pro Level-Up: `100` Duschcoins\n"
                  f"↣ Durch </daily:1175468452123783270>: Täglich `50-100` Duschcoins",
            inline=True
        )

        emb.add_field(
            name="EMOJI | Duschcoins Commands",
            value="",
            inline=False
        )

        for cmd in coins_cmds:
            cmd_name, cmd_options = cmd[0].split(" ", 1)
            cmd_id = 1
            for command in self.bot.commands:
                if command.name == cmd_name:
                    cmd_id = command.id

            emb.add_field(
                name="",
                value=f"</{cmd_name}:{cmd_id}> {cmd_options}\n{cmd[1]}",
                inline=False
            )

        return emb


    async def moderation_page(self):
        emb = Embed(
            color=0x36393F,  # 0x2f3136,
            title="",
            description='> <:d_settings:1175897310471913543> × Hier findest du alle wichtigen **Befehle** für die Moderation. (Optional) [Verpflichtend]',
        )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Help')

        for cmd in admin_cmds:
            cmd_name, cmd_options = cmd[0].split(" ", 1)
            cmd_id = 1
            for command in self.bot.commands:
                if command.name == cmd_name:
                    cmd_id = command.id

            emb.add_field(
                name="",
                value=f"</{cmd_name}:{cmd_id}> {cmd_options}\n{cmd[1]}",
                inline=False
            )

        return emb


def setup(client):
    client.add_cog(Help(client))
