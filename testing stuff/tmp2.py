import asyncio
import datetime
import json
import os
import sqlite3

import discord
from discord.utils import get

import secret

intents = discord.Intents.all()
client = discord.Bot(intents=intents)

"""DIR = os.path.dirname(__file__)
db = sqlite3.connect(os.path.join(DIR, "./storage/tmp.db"))
SQL = db.cursor()"""


@client.event
async def on_ready():
    print("Ich bin on!")


class Poll_channel_dropdown(discord.ui.View):
    @discord.ui.user_select(#.channel_select(
        placeholder="📚 | Wähle einen Kanal",
        min_values=1,
        max_values=1
    )
    async def Poll_channel_callback(self, select, interaction: discord.Interaction):
        with open('data/polls.json', 'r') as f:
            data = json.load(f)

        data[str(interaction.guild.id)]['pollchannel'] = int(select.values[0].id)

        with open("data/polls.json", 'w') as f:
            json.dump(data, f, indent=4)

        channel = data[str(interaction.guild.id)]['pollchannel']
        title = data[str(interaction.guild.id)]['polltitle']
        desc = data[str(interaction.guild.id)]['polldescription']

        embed = discord.Embed(title="Poll Modul - Einrichtung",
                              description="Hier hast du die möglichkeit eine Abstimmung zu erstellen,\n welche dann vom Team durchgeführt werden kann.\nSolltest du irgendwelche"
                                          "fragen haben\nwende dich an <@852878080447741952>!",
                              color=discord.Color.red())
        embed.add_field(name="Abstimmungs Titel", value=title)
        embed.add_field(name="Abstimmungs Beschreibung", value=desc, inline=False)
        embed.add_field(name="Abstimmungs Kanal", value=f"<#{channel}>", inline=False)
        embed.set_footer(text="Poll Modul - Einrichtung", icon_url=interaction.guild.icon.url)
        embed.timestamp = datetime.datetime.now()
        await interaction.response.edit_message(embed=embed, view = verwaltungs_buttons())


class Poll_view_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Abstimmungs-Titel",
                placeholder="Titel setzten ...",
                required=True,
                style=discord.InputTextStyle.short
            )
        ),

        self.add_item(
            discord.ui.InputText(
                label="Abstimmungs-Beschreibung",
                placeholder="Beschreibung setzten ...",
                required=True,
                style=discord.InputTextStyle.long
            )
        )

    async def callback(self, interaction: discord.Interaction):
        with open("data/polls.json", 'r') as f:
            data = json.load(f)

        data[str(interaction.guild.id)]['polltitle'] = self.children[0].value
        data[str(interaction.guild.id)]['polldescription'] = self.children[1].value

        with open("data/polls.json", 'w') as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(title="Poll Modul - Einrichtung",
                              description="Hier hast du die möglichkeit eine Abstimmung zu erstellen,\n welche dann vom Team durchgeführt werden kann.\nSolltest du irgendwelche"
                                          "fragen haben\nwende dich an <@852878080447741952>!",
                              color=discord.Color.red())
        embed.add_field(name="Abstimmungs Titel", value=self.children[0].value)
        embed.add_field(name="Abstimmungs Beschreibung", value=self.children[1].value, inline=False)
        embed.set_footer(text="Poll Modul - Einrichtung", icon_url=interaction.guild.icon.url)
        embed.timestamp = datetime.datetime.now()
        await interaction.response.edit_message(embed=embed, view = verwaltungs_buttons())


class auswahl_emotes_dropdown(discord.ui.View):
    @discord.ui.select(
        placeholder="📚 | Wähle Auswahlen aus",
        min_values=2,
        max_values=9,
        options=[
            discord.SelectOption(
                emoji="<:1_:1067159121226367078>",
                label="Wähle diese Zahl",
                value="1"
            ),
            discord.SelectOption(
                emoji="<:2_:1067159124481167370>",
                label="Wähle diese Zahl",
                value="2"
            ),
            discord.SelectOption(
                emoji="<:3_:1067159126448279632>",
                label="Wähle diese Zahl",
                value="3"
            ),
            discord.SelectOption(
                emoji="<:4_:1067159131087188061>",
                label="Wähle diese Zahl",
                value="4"
            ),
            discord.SelectOption(
                emoji="<:5_:1067159133918351430>",
                label="Wähle diese Zahl",
                value="5"
            ),
            discord.SelectOption(
                emoji="<:6_:1067159136892104776>",
                label="Wähle diese Zahl",
                value="6"
            ),
            discord.SelectOption(
                emoji="<:7_:1067159138624344134>",
                label="Wähle diese Zahl",
                value="7"
            ),
            discord.SelectOption(
                emoji="<:8_:1067159144118890697>",
                label="Wähle diese Zahl",
                value="8"
            ),
            discord.SelectOption(
                emoji="<:9_:1067159150531989574>",
                label="Wähle diese Zahl",
                value="9"
            )
        ]
    )
    async def select_callback(self, select, interaction: discord.Interaction):

        embed = discord.Embed(title="Abstimmung wurde erstellt!",
                              description=f"Es wurde erfolgreich eine Abstimmung erstellt!",
                              color=discord.Color.green())
        await interaction.response.edit_message(embed=embed, view = None)

        with open("data/polls.json", 'r') as f:
            data = json.load(f)

        title = data[str(interaction.guild.id)]['polltitle']
        description = data[str(interaction.guild.id)]['polldescription']
        channel = data[str(interaction.guild.id)]['pollchannel']

        embed = discord.Embed(title=title, description=f"```{description}```", color=discord.Color.red())
        embed.set_footer(text=title, icon_url=interaction.guild.icon.url)
        embed.set_author(name="Eine Neue Abstimmung", icon_url=interaction.guild.icon.url)
        embed.add_field(name="Information!",
                        value="> Um an der Abstimmung teilnehmen zu können,\nmust du unten deine Stimme auswählen!")
        embed.timestamp = datetime.datetime.now()
        c = await client.fetch_channel(channel)
        msg = await c.send(embed=embed)

        if "1" in interaction.data['values']:
            await msg.add_reaction("1️⃣")
        if "2" in interaction.data['values']:
            await msg.add_reaction("2️⃣")
        if "3" in interaction.data['values']:
            await msg.add_reaction("3️⃣")
        if "4" in interaction.data['values']:
            await msg.add_reaction("4️⃣")
        if "5" in interaction.data['values']:
            await msg.add_reaction("<:5_:1067159133918351430>")
        if "6" in interaction.data['values']:
            await msg.add_reaction("<:6_:1067159136892104776>")
        if "7" in interaction.data['values']:
            await msg.add_reaction("<:7_:1067159138624344134>")
        if "8" in interaction.data['values']:
            await msg.add_reaction("<:8_:1067159144118890697>")
        if "9" in interaction.data['values']:
            await msg.add_reaction("<:9_:1067159150531989574>")


class verwaltungs_buttons(discord.ui.View):
    @discord.ui.button(
        label="Abstimmungs Text",
        style=discord.ButtonStyle.blurple,
    )
    async def text_callback(self, button, interaction: discord.Interaction):
        Modal = Poll_view_modal(title="Abstimmungstext Modal")
        await interaction.response.send_modal(Modal)

    @discord.ui.button(
        label="Abstimmungs Kanal",
        style=discord.ButtonStyle.blurple
    )
    async def channel_callback(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=Poll_channel_dropdown())

    @discord.ui.button(
        label="Abstimmung auswahl",
        style=discord.ButtonStyle.blurple,
        row=1
    )
    async def auswahl_callback(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message(view=auswahl_emotes_dropdown())


@client.slash_command(name="create-poll")
async def _create_poll_(ctx: discord.ApplicationContext):
    with open("data/polls.json", 'r') as f:
        data = json.load(f)

    data[str(ctx.guild.id)] = {}
    data[str(ctx.guild.id)]['msgid'] = "None"
    data[str(ctx.guild.id)]['polltitle'] = "None"
    data[str(ctx.guild.id)]['polldescription'] = "None"
    data[str(ctx.guild.id)]['pollchannel'] = 0

    embed = discord.Embed(title="Poll Modul - Einrichtung",
                          description="Hier hast du die möglichkeit eine Abstimmung zu erstellen,\n welche dann vom Team durchgeführt werden kann.\nSolltest du irgendwelche"
                                      "fragen haben\nwende dich an <@852878080447741952>!",
                          color=discord.Color.red())
    embed.add_field(name="WICHTIG!!!!!!!",
                    value="Schreibe in die Beschreibung die Auswahlen rein!\n**Beispiel**\n```<emote> -> Auswahl 1\n<emote> -> Auswahl 2\n...```")
    embed.set_footer(text="Poll Modul - Einrichtung", icon_url=ctx.guild.icon.url)
    embed.timestamp = datetime.datetime.now()
    await ctx.respond(embed=embed, view=verwaltungs_buttons(), ephemeral=True)

    with open("data/polls.json", 'w') as f:
        json.dump(data, f, indent=4)


client.run(secret.Test_bot_TOKEN)

