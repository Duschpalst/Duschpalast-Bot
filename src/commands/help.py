from ast import literal_eval
from datetime import datetime

import discord
from discord import Embed
from discord.ext import commands
from discord.ui import View, Button, Select, InputText

from static import *


class Help(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot: discord.Bot = bot
        self.guild = None


    @commands.slash_command(name="help", description="❓ | Benötigst du Hilfe?")
    async def cmd(self, ctx: discord.ApplicationContext):
        self.guild: discord.Guild = ctx.guild

        admin = ctx.author.guild_permissions.kick_members
        await ctx.respond(embed=await self.start_page(), view=await self.view(admin), ephemeral=True)


    async def view(self, admin=False):
        v = View(timeout=900)

        categories_list = [
            ["Startseite", "Kehre zur Startseite zurück.", "<:d_compass:1175897308911640686>"],
            ["Allgemein Commands", "Allgemeine Befehle die jeder Nutzer nutzen kann.", "<:d_slashcommand:1176228551050154045>"],
            ["Wie das Level System funktioniert", "Zeige dir alles zum Level System an.", "<:d_metrics:1176229778177658961>"],
            ["Wie das Duschcoins System funktioniert", "Zeige dir alles zum Duschcoins System an.", "<:d_creditcard:1176229782833348709>"],
            ["Games (Cooming Soon)", "Zeige dir alles zu Games an.", "<:d_bughunter:1175897321532305529>"]
        ]

        admin_categories_list = [
            ["Moderation Commands", "Befehle für Moderation des Servers.", "<:d_settings:1175897310471913543>"],
        ]

        if admin:
            categories_list.extend(admin_categories_list)


        categories = Select(
            placeholder=f"📂 | Kategorien",
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
            categories_mapping = {
                "0": self.start_page,
                "1": self.cmd_page,
                "2": self.lvl_page,
                "3": self.coins_page,
                "4": self.start_page,
                "5": self.moderation_page,
            }
            emb = await categories_mapping.get(categories.values[0], self.start_page)()
            await interaction.response.edit_message(embed=emb)



        categories.callback = callback
        v.add_item(categories)


        button1 = Button(label="Ideen / Bugs", custom_id="ideas_bug", style=discord.ButtonStyle.blurple)
        button2 = Button(label="Frage nicht gefunden?", custom_id="question", style=discord.ButtonStyle.green)

        v.add_item(button1)
        v.add_item(button2)

        button1.callback = self.standard_btn_callback
        button2.callback = self.standard_btn_callback

        return v


    async def start_page(self):
        emb = Embed(
            color=0x2b2d31,
            title="",
            description='> ️<:d_info:1175897319389016125> × Hier findest du **alle relevanten Informationen** zu den **Befehlen** und **weiteren Funktionen** dieses Discord-Bots.',
            )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Help')

        emb.add_field(
            name="<:d_staff:1175897436129079306> | Generelle Server Infos",
            value=f"↣ Mitglieder: `{len(self.guild.members)}`\n"
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

        emb.add_field(
            name=f"{invisible_character}\n{invisible_character}",
            value="> <:d_info:1175897319389016125> × Durch das **Klicken** auf die **Kategorien**, siehst du alle Kategorien zur der du **Hilfe** bekommen kannst!",
            inline=False
        )

        return emb


    async def cmd_page(self):
        emb = Embed(
            color=0x2b2d31,  # 0x2f3136,
            title="",
            description='> <:d_category:1175897311784742942> × Hier findest du **alle Befehle** die du nutzten kannst. (Optional) [Verpflichtend]',
        )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Help')

        for cmd in basic_cmds:
            cmd_name, cmd_options = cmd[0].split(" ", 1) if len(cmd[0].split(" ", 1)) == 2 else (cmd[0], "")
            cmd_id = next((command.id for command in self.bot.commands if command.name == cmd_name), 1)

            emb.add_field(
                name="",
                value=f"</{cmd_name}:{cmd_id}> {cmd_options}\n{cmd[1]}",
                inline=False
            )

        return emb

    async def lvl_page(self):
        emb = Embed(
            color=0x2b2d31,  # 0x2f3136,
            title="",
            description='> <:d_metrics:1176229778177658961> × Hier findest du alle wichtige **Informationen** und **Befehle** zum Level System. (Optional) [Verpflichtend]',
        )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Help')

        emb.add_field(
            name="<:d_metrics:1176229778177658961> | Level-System:",
            value=f"↣ Basis-XP für ein Level: `250 XP`\n"
                  f"↣ XP-Inkrement pro Level: `10 XP`",
            inline=True
        )

        emb.add_field(
            name="<:d_creditcard:1176229782833348709> | XP verdienen:",
            value=f"↣ Booster: XP * 2\n"
                  f"↣ Pro Nachricht: `1 XP`\n"
                  f"↣ Pro 5 Min im Sprachkanal: `10 XP`\n"
                  f"↣ `+5 XP` pro Stunde\n"
                  f"Durch </daily:1175468452123783270>: Täglich `15-50` XP",
            inline=True
        )

        emb.add_field(
            name="<:d_slashcommand:1176228551050154045> | Befehle für das Level-System",
            value="",
            inline=False
        )

        for cmd in lvl_cmds:
            cmd_name, cmd_options = cmd[0].split(" ", 1) if len(cmd[0].split(" ", 1)) == 2 else (cmd[0], "")
            cmd_id = next((command.id for command in self.bot.commands if command.name == cmd_name), 1)

            emb.add_field(
                name="",
                value=f"</{cmd_name}:{cmd_id}> {cmd_options}\n{cmd[1]}",
                inline=False
            )

        return emb


    async def coins_page(self):
        emb = Embed(
            color=0x2b2d31,  # 0x2f3136,
            title="",
            description='> <:d_creditcard:1176229782833348709> × Hier findest du alle wichtige **Informationen** und **Befehle** zum Duschcoin System. (Optional) [Verpflichtend]',
        )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Help')

        emb.add_field(
            name="<:d_creditcard:1176229782833348709> | Duschcoins verdienen:",
            value=f"↣ Pro Level-Up: `100` Duschcoins\n"
                  f"↣ Durch </daily:1175468452123783270>: Täglich `50-100` Duschcoins",
            inline=True
        )

        emb.add_field(
            name="<:d_slashcommand:1176228551050154045> | Befehle für Duschcoins",
            value="",
            inline=False
        )

        for cmd in coins_cmds:
            cmd_name, cmd_options = cmd[0].split(" ", 1) if len(cmd[0].split(" ", 1)) == 2 else (cmd[0], "")
            cmd_id = next((command.id for command in self.bot.commands if command.name == cmd_name), 1)

            emb.add_field(
                name="",
                value=f"</{cmd_name}:{cmd_id}> {cmd_options}\n{cmd[1]}",
                inline=False
            )

        return emb


    async def moderation_page(self):
        emb = Embed(
            color=0x2b2d31,  # 0x2f3136,
            title="",
            description='> <:d_settings:1175897310471913543> × Hier findest du alle wichtigen **Befehle** für die Moderation des Servers. (Optional) [Verpflichtend]',
        )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Help')

        for cmd in admin_cmds:
            cmd_name, cmd_options = cmd[0].split(" ", 1) if len(cmd[0].split(" ", 1)) == 2 else (cmd[0], "")
            cmd_id = next((command.id for command in self.bot.commands if command.name == cmd_name), 1)

            emb.add_field(
                name="",
                value=f"</{cmd_name}:{cmd_id}> {cmd_options}\n{cmd[1]}",
                inline=False
            )

        return emb



    async def standard_btn_callback(self, interaction: discord.Interaction):
        if interaction.custom_id == "ideas_bug":
            await interaction.response.send_modal(self.ibq_Modal(title="Wie Lautet deine Idee oder dein Bug", custom_id="['ideas_bug', 'None']", bot=self.bot))
        elif interaction.custom_id == "question":
            await interaction.response.send_modal(self.ibq_Modal(title="Wie Lautet Frage?", custom_id="['question', 'None']", bot=self.bot))


    # Ideas Bug Question Modal
    class ibq_Modal(discord.ui.Modal):
        def __init__(self, bot, *args, **kwargs):
            super().__init__(
                InputText(
                    label="Deine Nachricht",
                    placeholder="Schreibe hier...",
                    style=discord.InputTextStyle.paragraph,
                    value=None if (txt := literal_eval(kwargs.get("custom_id"))[-1]) == "None" else txt
                ),

                *args,
                **kwargs
            )
            self.bot = bot

        async def callback(self, interaction: discord.Interaction):
            await self.control_ibq(interaction, self.children[0].value, self.custom_id)


        async def control_ibq(self, interaction, txt, custom_id):
            emb = Embed(title="Bitte Lese Nochmal über deine Nachricht drüber bevor du sie abschickst",
                        description=f"",
                        color=0x2b2d31)

            emb.timestamp = datetime.utcnow()
            emb.set_author(name='Duschpalast Bot | Help', icon_url=self.bot.user.avatar.url)
            emb.set_footer(text='Duschpalast Bot | Help')

            emb.add_field(name="Deine Nachricht:",
                          value=f"```{txt}```",
                          inline=False)


            v = View(timeout=60)

            buttons = [
                Button(label="Abbrechen", custom_id="cancel", style=discord.ButtonStyle.red),
                Button(label="Bearbeiten", custom_id="edit", style=discord.ButtonStyle.blurple),
                Button(label="Senden", custom_id="submit", style=discord.ButtonStyle.green)
            ]

            for button in buttons:
                v.add_item(button)

            async def help_btn_callback(interaction: discord.Interaction):
                if interaction.custom_id == "cancel":
                    emb_c = discord.Embed(title="Abgebrochen",
                                          description="<:d_cross:1176957164988924036> | Du kannst jetzt diese Nachricht Löschen",
                                          colour=0x2b2d31)

                    emb_c.timestamp = datetime.utcnow()
                    emb_c.set_author(name="Duschpalast Bot | Help",
                                     icon_url=self.bot.user.avatar.url)
                    emb_c.set_footer(text="Duschpalast Bot | Help")
                    await interaction.response.edit_message(embed=emb_c, view=None)

                elif interaction.custom_id == "edit":
                    if literal_eval(custom_id)[0] == "ideas_bug":
                        await interaction.response.send_modal(
                            Help.ibq_Modal(title="Wie Lautet deine Idee oder dein Bug", custom_id=f"['ideas_bug', '{txt}']", bot=self.bot))
                    elif literal_eval(custom_id)[0] == "question":
                        await interaction.response.send_modal(
                            Help.ibq_Modal(title="Wie Lautet Frage?", custom_id=f"['question', '{txt}']", bot=self.bot))

                elif interaction.custom_id == "submit":
                    emb_s1 = discord.Embed(title="Erfolgreich gesendet",
                                          description="<:d_chat:1176956349045805279> | Vielen Dank, Wir haben deine Nachricht bekommen und werden diese jetzt bearbeiten",
                                          colour=0x2b2d31,
                                          timestamp=datetime.now())

                    emb_s1.add_field(name="Deine Nachricht an uns:",
                                    value=f"```{txt}```",
                                    inline=False)

                    emb_s1.set_author(name="Duschpalast Bot | Help",
                                     icon_url=self.bot.user.avatar.url)
                    emb_s1.set_footer(text="Duschpalast Bot | Help")
                    await interaction.response.edit_message(embed=emb_s1, view=None)


                    if literal_eval(custom_id)[0] == "ideas_bug":
                        title = "Es wurde eine Idee / Bug eingereicht"
                    else:
                        title = "Es wurde eine Frage gestellt"

                    emb_s2 = Embed(title=title,
                                description=f"Von: {interaction.user.mention}",
                                color=0x2b2d31)

                    emb_s2.timestamp = datetime.utcnow()
                    emb_s2.set_author(name='Duschpalast Bot', icon_url=self.bot.user.avatar.url)
                    emb_s2.set_footer(text='Duschpalast Bot')

                    emb_s2.add_field(name="Nachricht:",
                                  value=f"```{txt}```",
                                  inline=False)

                    channel = await self.bot.fetch_channel(channels_id['team'])
                    await channel.send(embed=emb_s2)

            for button in buttons:
                button.callback = help_btn_callback

            if literal_eval(custom_id)[-1] == "None":
                await interaction.response.send_message(embed=emb, view=v, ephemeral=True)
            else:
                await interaction.response.edit_message(embed=emb, view=v)



def setup(client):
    client.add_cog(Help(client))
