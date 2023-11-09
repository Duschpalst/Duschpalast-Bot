from datetime import date, timedelta, datetime
from ast import literal_eval

import discord
from discord import Embed
from discord.ext import commands
from discord.ui import View, Button, InputText, Select

from static import SQL


class Protocol(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="protokoll", description="Benutzer Protokoll")
    async def cmd(self, ctx: discord.ApplicationContext):
        msg = await start_page(ctx.guild)
        await ctx.respond(embed=msg[0], view=msg[1], ephemeral=True)


def setup(client):
    client.add_cog(Protocol(client))


async def start_page(guild: discord.guild):
    view = View(timeout=None)
    button1 = Button(label="Protokoll anzeigen", custom_id="show", style=discord.ButtonStyle.green)
    button2 = Button(label="neues Protokoll", custom_id="add", style=discord.ButtonStyle.blurple)

    view.add_item(button1)
    view.add_item(button2)

    button1.callback = start_page_callback
    button2.callback = start_page_callback

    emb = discord.Embed(title="Protokoll Modul",
                        color=discord.Color.red(),
                        description="Hier hast du die Möglichkeit ein Protokoll,\neines Users anzuzeigen oder neue Protokolle zu erstellen.")
    emb.add_field(name="WICHTIG!!!",
                  value="```Schreibe die Protokolle ausführlich genug,\n damit die anderen die Protokolle verstehen.```")
    emb.set_footer(text=f"Solltest du irgendwelche fragen haben\nwende dich ans Dev Team\nUhrzeit:",
                   icon_url=guild.icon.url)
    emb.timestamp = datetime.now()

    return emb, view


async def start_page_callback(interaction: discord.Interaction):
    if interaction.custom_id == "show":
        await interaction.response.send_modal(UserModal(title="User", custom_id="show"))
    elif interaction.custom_id == "add":
        await interaction.response.send_modal(UserModal(title="User", custom_id="add"))


class UserModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            InputText(
                label="Name",
                placeholder="Wie fängt der User Name an?"
            ),

            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction):
        await user_dropdown(interaction, self.children[0].value, self.custom_id)


async def user_dropdown(interaction: discord.Interaction, letters, custom_id):
    res = 0
    for x in interaction.guild.members:
        if x.name.lower().startswith(letters.lower()) and not x.bot:
            res += 1

    emb = (await start_page(interaction.guild))[0]
    if res == 0:
        emb.add_field(name="**ERROR**",
                      value="**```Es wurde kein Nutzer gefunden\nProbiere es erneut```**",
                      inline=False)
        await interaction.response.edit_message(embed=emb)
        return
    elif res > 25:
        emb.add_field(name="**ERROR**",
                      value="**```Es wurde Zu viele Nutzer gefunden\nProbiere es erneut```**",
                      inline=False)
        await interaction.response.edit_message(embed=emb)
        return

    dropdown = Select(
        custom_id=custom_id,
        placeholder="👨👩 | Wähle den User",
        options=[discord.SelectOption(
            label=str(x),
            value=str(x.id)
        ) for x in interaction.guild.members if x.name.lower().startswith(letters.lower()) if not x.bot
        ])

    async def usr_callback(interaction: discord.Interaction):
        if interaction.custom_id == "show":
            await show_protocols(dropdown, interaction)
        elif interaction.custom_id == "add":
            await add_system_btn(dropdown.values[0], interaction)
            # await interaction.response.send_modal(AddModal(title="Neues Protokoll", custom_id=dropdown.values[0]))

    view = View(timeout=None)
    view.add_item(dropdown)
    dropdown.callback = usr_callback

    await interaction.response.edit_message(embed=(await start_page(interaction.guild))[0], view=view)


async def show_protocols(selectmenu, interaction: discord.Interaction):
    SQL.execute(f'SELECT protocol FROM users WHERE user_id = {selectmenu.values[0]};')
    res = SQL.fetchone()[0]

    if res:
        color = discord.Color.green()
    else:
        color = discord.Color.red()

    emb = discord.Embed(title="Protokoll Modul",
                        color=color,
                        description=f"Protokolle vom User: <@{selectmenu.values[0]}>")
    emb.set_footer(text=f"Solltest du irgendwelche fragen haben\nwende dich ans Dev Team\nUhrzeit:",
                   icon_url=interaction.guild.icon.url)
    emb.timestamp = datetime.now()

    if res:
        for x in literal_eval(res):
            emb.add_field(name=f"{x[0]}:",
                          value=f"Erstellt von: <@{x[1]}>\n__Bestrafung:__ `{x[2]}`\n```{x[3]}```",
                          inline=False)
    else:
        emb.add_field(name=f"ERROR",
                      value=f"```Der User hat noch keine Protokol einträge```",
                      inline=False)

    await interaction.response.edit_message(embed=emb, view=None)


async def add_system_btn(user, interaction: discord.Interaction, date_p=None, punishment=None, protocol=None):
    check = ["❌", "❌", "❌"]
    if date_p:
        check[0] = "✅"
    if punishment:
        check[1] = "✅"
    if protocol:
        check[2] = "✅"
    emb = discord.Embed(title="Protokoll Modul",
                        color=discord.Color.purple(),
                        description=f"Neues Protokoll für den User: <@{user}>")
    emb.add_field(name="Informationen:",
                  value=f"Datum: {check[0]}\nBestrafung: {check[1]}\n Protokoll: {check[2]}")
    emb.set_footer(text=f"Solltest du irgendwelche fragen haben\nwende dich ans Dev Team\nUhrzeit:",
                   icon_url=interaction.guild.icon.url)
    emb.timestamp = datetime.now()

    view = View(timeout=None)
    button1 = Button(label="Datum", custom_id="date", style=discord.ButtonStyle.blurple)
    button2 = Button(label="Bestrafung", custom_id="punish", style=discord.ButtonStyle.blurple)
    button3 = Button(label="Protokol", custom_id="protocol", style=discord.ButtonStyle.blurple, row=2)

    disabled = False
    if not date_p or not punishment or not protocol:
        disabled = True
    button4 = Button(label="Fertig", custom_id="done", style=discord.ButtonStyle.green, row=2, disabled=disabled)

    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)

    async def add_system_callback(interaction: discord.Interaction):
        if interaction.custom_id == "date":
            day = date.today()
            name = []
            for x in range(14):
                days = day - timedelta(days=x)
                tmp = []
                if days == day:
                    tmp.append("Heute")
                elif days == (day - timedelta(days=1)):
                    tmp.append("Gestern")
                else:
                    tmp.append(f"{days.day}.{days.month}.{days.year}")

                tmp.append(f"{days.day}.{days.month}.{days.year}")

                name.append(tmp)

            dropdown = Select(
                placeholder="📅Datum",
                options=[discord.SelectOption(
                    label=str(x[0]),
                    value=str(x[1])
                ) for x in name
                ])

            async def date_callback(interaction: discord.Interaction):
                await add_system_btn(user, interaction, dropdown.values[0], punishment, protocol)

            view = View(timeout=None)
            view.add_item(dropdown)
            dropdown.callback = date_callback

            await interaction.response.edit_message(view=view)
        elif interaction.custom_id == "punish":
            punishments = ["Verwarnung Ⅰ", "Verwarnung Ⅱ", "Verwarnung Ⅲ", "Warnung + Verwarung Ⅰ", "Warnung + Verwarung Ⅱ", "Warnung + Verwarung Ⅲ"]
            dropdown = Select(
                placeholder="⛓️Bestrafung",
                options=[discord.SelectOption(
                    label=x,
                    value=x
                ) for x in punishments
                ])

            async def punish_callback(interaction: discord.Interaction):
                await add_system_btn(user, interaction, date_p, dropdown.values[0], protocol)

            view = View(timeout=None)
            view.add_item(dropdown)
            dropdown.callback = punish_callback

            await interaction.response.edit_message(view=view)
        elif interaction.custom_id == "protocol":
            await interaction.response.send_modal(
                AddProtocolModal(title="Neues Protokoll", custom_id=f"[{user}, '{date_p}', '{punishment}', '{protocol}']"))
        elif interaction.custom_id == "done":
            SQL.execute(f'SELECT protocol FROM users WHERE user_id = {user};')
            arr = literal_eval(SQL.fetchone()[0])
            arr.append([f"{date_p}", interaction.user.id, f"{punishment}", f"{protocol}"])
            SQL.execute(f'UPDATE users SET protocol = "{arr}" WHERE user_id = {user};')
            await interaction.response.edit_message(embed=Embed(color=discord.Color.green(), title="Fertig"), view=None)

    button1.callback = add_system_callback
    button2.callback = add_system_callback
    button3.callback = add_system_callback
    button4.callback = add_system_callback

    await interaction.response.edit_message(embed=emb, view=view)


def get_val(kwargs):
    user, date_p, punishment, protocol = literal_eval(kwargs.get("custom_id"))
    if protocol == "None":
        protocol = None
    return protocol


class AddProtocolModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(

            InputText(
                label="Protokol eintrag",
                placeholder="Gib hier das Protokol für den User ein",
                value=get_val(kwargs)
            ),

            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction):
        user, date_p, punishment, creator = literal_eval(self.custom_id)
        if date_p == "None":
            date_p = None
        if punishment == "None":
            punishment = None

        await add_system_btn(user, interaction, date_p, punishment, self.children[0].value)
