import datetime

import discord
from discord import Option, Embed
from discord.ext import commands
from discord.ui import View, Button

from static import get_client, SQL, db


class Birthday(commands.Cog):

    def __init__(self, bot):
        print(f"loaded {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="set-birthday", description="Setze dein Geburtstag fest")
    async def cmd(self, ctx, day: Option(int, "DD", required=True, max_value=31, min_value=1), month: Option(int, "MM", required=True, max_value=12, min_value=1), year: Option(int, "YYYY", required=True, max_value=datetime.date.today().year, min_value=(datetime.date.today().year - 100))):
        view = View(timeout=60)
        button1 = Button(label="Bestätigen", custom_id=f"confirm {day}-{month}-{year}", style=discord.ButtonStyle.green)
        button2 = Button(label="Abbrechen", custom_id="cancel", style=discord.ButtonStyle.red)

        view.add_item(button1)
        view.add_item(button2)

        button1.callback = btn_callback
        button2.callback = btn_callback

        await ctx.respond(embed=Embed(color=discord.Color.purple(), title=f"{day} / {month} / {year}", description="Stimmt das so?"), ephemeral=True, view=view)


def setup(client):
    client.add_cog(Birthday(client))


async def btn_callback(interaction):
    client = await get_client()
    if interaction.custom_id == "cancel":
        color = discord.Color.red()
        txt = "Abbgebrochen"

    elif interaction.custom_id.startswith("confirm"):
        color = discord.Color.green()
        txt = "Bestätigt"
        #date = interaction.custom_id[8:].split("-")

        SQL.execute(f'select user_id from users where user_id="{interaction.user.id}"')
        result_userid = SQL.fetchone()

        if result_userid is None:
            SQL.execute('insert into users(user_id, user_name) values(?,?)', (interaction.user.id, str(interaction.user),))

        SQL.execute(f'UPDATE users SET birthday = "{interaction.custom_id[8:]}" WHERE user_id = {interaction.user.id}')
        db.commit()

    await interaction.response.edit_message(embed=Embed(color=color, title=txt), view=None)
