from datetime import datetime

import discord
from discord import Embed, default_permissions
from discord.ext import commands
from discord.ui import Select, View, InputText, Button

from static import SQL, invisible_character, db
from utils.user.cmd_reward import cmd_reward


class Welcome_Msg(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="welcome-msg", description="👋️ | Bearbeite die Willkommens Nachrichten")
    @default_permissions(kick_members=True)
    async def cmd(self, ctx):
        await cmd_reward(ctx)

        emb = Embed(
            color=0x2b2d31,
            title="",
            description='> <:d_settings:1175897310471913543> × Verwalte die **Willkommensnachricht** für **neue Mitglieder** auf dem Server für den **Allgemeinchat**.',
        )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Moderation', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Moderation')


        res = SQL.execute('SELECT COUNT(*) FROM general_welcome_msg;')
        count = res.fetchone()[0]
        emb.add_field(
            name="<:d_info:1175897319389016125> | Willkommensnachricht Infos",
            value=f"↣ Die Willkommensnachricht wird Random ausgewählt\n"
                  f"↣ Aktuelle Willkommensnachrichten: `{count}`\n",
            inline=True
        )

        emb.add_field(
            name=f"{invisible_character}\n{invisible_character}",
            value="> <:d_info:1175897319389016125> × Durch das **Klicken** auf die **Nachricht**, kannst du eine **Willkommensnachricht** für den Allgemeinchat Hinzufügen oder Löschen.",
            inline=False
        )


        adddel = Select(
            placeholder=f"➕➖ | Nachricht",
            options=[
                discord.SelectOption(
                    label="Hinzufügen",
                    description="Füge eine Willkommensnachricht dazu.",
                    emoji="<:d_greenplus:1179883173782503434>",
                    value="add"
                ),
                discord.SelectOption(
                    label="Entfernen",
                    description="Lösche eine Willkommensnachricht.",
                    emoji="<:d_redminus:1179883172431933470>",
                    value="delete"
                ),
            ],
            min_values=1,
            max_values=1
        )

        async def callback(interaction: discord.Interaction):
            if adddel.values[0] == "add":
                await interaction.response.send_modal(
                    self.add_Modal(title="Wie Lautet die neue Willkommensnachricht?", custom_id=f"None",
                                          bot=self.bot))

            else:
                await self.delete_msg(interaction)

        view = View(timeout=900)
        adddel.callback = callback
        view.add_item(adddel)

        await ctx.respond(embed=emb, view=view, ephemeral=True)



    class add_Modal(discord.ui.Modal):
        def __init__(self, bot, *args, **kwargs):
            super().__init__(
                InputText(
                    label="Deine Nachricht",
                    placeholder="Wenn der neue User gepingt werden soll schreibe: [Neuer User]",
                    style=discord.InputTextStyle.paragraph,
                    value=None if (txt := kwargs.get("custom_id")) == "None" else txt
                ),

                *args,
                **kwargs
            )
            self.bot = bot

        async def callback(self, interaction: discord.Interaction):
            await self.control_add(interaction, self.children[0].value, self.custom_id)


        async def control_add(self, interaction, txt, custom_id):
            emb = Embed(title="Bitte Lese Nochmal über die Willkommensnachricht drüber bevor du sie abschickst",
                        description=f"",
                        color=0x2b2d31)

            emb.timestamp = datetime.utcnow()
            emb.set_author(name='Duschpalast Bot | Moderation', icon_url=self.bot.user.avatar.url)
            emb.set_footer(text='Duschpalast Bot | Moderation')

            emb.add_field(name="Die Willkommensnachricht von dir:",
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

            async def add_btn_callback(interaction: discord.Interaction):
                if interaction.custom_id == "cancel":
                    emb_c = discord.Embed(title="Abgebrochen",
                                          description="<:d_cross:1176957164988924036> | Du kannst jetzt diese Nachricht Löschen",
                                          colour=0x2b2d31)

                    emb_c.timestamp = datetime.utcnow()
                    emb_c.set_author(name="Duschpalast Bot | Moderation",
                                     icon_url=self.bot.user.avatar.url)
                    emb_c.set_footer(text="Duschpalast Bot | Moderation")
                    await interaction.response.edit_message(embed=emb_c, view=None)

                elif interaction.custom_id == "edit":
                        await interaction.response.send_modal(
                            Welcome_Msg.add_Modal(title="Wie Lautet die neue Willkommensnachricht?", custom_id=f"{txt}", bot=self.bot))

                elif interaction.custom_id == "submit":
                    emb_s = discord.Embed(title="Erfolgreich gesendet",
                                          description="<:d_chat:1176956349045805279> | Die neue Willkommensnachricht ist erfolgreich eingegangen.",
                                          colour=0x2b2d31,
                                          timestamp=datetime.now())

                    emb_s.add_field(name="Die neue Willkommensnachricht:",
                                    value=f"```{txt}```",
                                    inline=False)

                    emb_s.set_author(name="Duschpalast Bot | Moderation",
                                     icon_url=self.bot.user.avatar.url)
                    emb_s.set_footer(text="Duschpalast Bot | Moderation")
                    await interaction.response.edit_message(embed=emb_s, view=None)


                    SQL.execute('INSERT INTO general_welcome_msg(msg) values(?)', (txt,))
                    db.commit()


            for button in buttons:
                button.callback = add_btn_callback

            if custom_id == "None":
                await interaction.response.send_message(embed=emb, view=v, ephemeral=True)
            else:
                await interaction.response.edit_message(embed=emb, view=v)



    async def delete_msg(self, interaction: discord.Interaction):
        res = SQL.execute('SELECT msg FROM general_welcome_msg')
        res = res.fetchall()

        emb = Embed(
            color=0x2b2d31,
            title="",
            description='> <:d_settings:1175897310471913543> × Hier ist die Liste der **Willkommensnachrichten** für **neue Mitglieder** auf dem Server für den **Allgemeinchat**.',
        )

        emb.timestamp = datetime.utcnow()
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_author(name='Duschpalast Bot | Moderation', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Moderation')

        for id, msg in enumerate(res, 1):
            emb.add_field(name=f"{id}:",
                          value=f"`{msg[0]}`",
                          inline=False)


        delete_id = Select(
            placeholder=f"➖ | Welche Nachricht soll gelöscht werden?",
            options=[
                discord.SelectOption(
                    label=f"{x+1}",
                    value=f"{x}"
                )for x in range(len(res))
            ],
            min_values=1,
            max_values=1
        )

        async def callback(interaction: discord.Interaction):
            msg = res[int(delete_id.values[0])][0]

            SQL.execute(f'DELETE FROM general_welcome_msg WHERE msg = "{msg}";')
            db.commit()

            emb_d = discord.Embed(title="Willkommensnachricht gelöscht",
                                  description="<:d_cross:1176957164988924036> | Du kannst jetzt diese Nachricht Löschen",
                                  colour=0x2b2d31)

            emb_d.timestamp = datetime.utcnow()
            emb_d.set_author(name="Duschpalast Bot | Moderation",
                             icon_url=self.bot.user.avatar.url)
            emb_d.set_footer(text="Duschpalast Bot | Moderation")
            await interaction.response.edit_message(embed=emb_d, view=None)

        view = View(timeout=300)
        delete_id.callback = callback
        view.add_item(delete_id)

        await interaction.response.edit_message(embed=emb, view=view)


def setup(client):
    client.add_cog(Welcome_Msg(client))
