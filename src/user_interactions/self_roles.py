import math
import discord
from discord import Embed
from discord.ext import commands
from discord.ui import Select, View

import static
from static import SQL, self_roles_messages_id
from utils.guilds.get_emoji import get_emoji


class Self_Roles(commands.Cog):

    def __init__(self, bot):
        print(f"loaded User Interaction {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.user.id == static.bot_id:
            await self_roles(self.bot)


def setup(client):
    client.add_cog(Self_Roles(client))


async def callback(interaction, which, selectmenu):
    table = ""
    if which == "games":
        table = "self_roles_games"
    #elif which == "programming":
        #table = "self_roles_programming"
    elif which == "age":
        table = "self_roles_age"
    elif which == "gender":
        table = "self_roles_gender"

    SQL.execute(f'SELECT role_id FROM {table}')
    res = SQL.fetchall()
    all_roles = []
    for i in res:
        all_roles.append(i[0])

    for s in selectmenu:
        if s.values:
            for x in s.values:
                all_roles.remove(int(x))
                role = interaction.guild.get_role(int(x))
                await interaction.user.add_roles(role, reason="Self Role", atomic=True)

    # Remove not selected roles
    for i in all_roles:
        rolle = interaction.guild.get_role(i)
        if rolle in interaction.user.roles:
            await interaction.user.remove_roles(rolle, atomic=True)


async def self_roles(client):
    gender = [Select(
        placeholder="👨👩Geschlecht",
        options=[
            discord.SelectOption(
                label="Männlich",
                emoji="🚹",
                value="980585344909058120"
            ),
            discord.SelectOption(
                label="Weiblich",
                emoji="🚺",
                value="980585383739928617"
            ),
            discord.SelectOption(
                label="Divers",
                emoji="🚻",
                value="1015925190640816170"
            )
        ]
    )]

    async def gender_callback(interaction):
        await interaction.response.send_message(
            embed=Embed(color=discord.Color.green(), title="Updated"),
            ephemeral=True)
        await callback(interaction, "gender", gender)

    age = [Select(
        placeholder="🔞Alter",
        options=[
            discord.SelectOption(
                label="Unter 18",
                emoji=await get_emoji("Minderjhrig", client),
                value="1012375630760923266"
            ),
            discord.SelectOption(
                label="Über 18",
                emoji=await get_emoji("Volljhrig", client),
                value="1012375747173810236"
            )
        ]
    )]

    async def age_callback(interaction):
        await interaction.response.send_message(
            embed=Embed(color=discord.Color.green(), title="Updated"),
            ephemeral=True)
        await callback(interaction, "age", age)

    SQL.execute('SELECT * FROM self_roles_games ORDER BY LOWER(name);')
    res = SQL.fetchall()
    count_g = math.ceil(len(res) / 25)

    values = [res[i:i + 25] for i in range(0, len(res), 25)]

    games = []
    for i in range(count_g):
        games.append(Select(
            placeholder=f"🎮Spiele {i + 1}",
            options=[discord.SelectOption(
                label=x[0],
                emoji=await get_emoji(x[1], client),
                value=str(x[2])
            ) for x in values[i]
            ],
            min_values=0,
            max_values=len(values[i])
        ))

    async def games_callback(interaction):
        await interaction.response.send_message(
            embed=Embed(color=discord.Color.green(), title="Updated"),
            ephemeral=True)
        await callback(interaction, "games", games)

    """
    SQL.execute('SELECT * FROM self_roles_programming ORDER BY name;')
    res = SQL.fetchall()
    count_p = math.ceil(len(res) / 25)

    values = [res[i:i + 25] for i in range(0, len(res), 25)]

    programming = []
    for i in range(count_p):
        programming.append(Select(
            placeholder=f"💻Programmier Sprachen {i + 1}",
            options=[discord.SelectOption(
                label=x[0],
                emoji=await get_emoji(x[1], client),
                value=str(x[2])
            ) for x in values[i]
            ],
            min_values=0,
            max_values=len(values[i])
        ))

    async def programming_callback(interaction):
        await interaction.response.send_message(
            embed=Embed(color=discord.Color.green(), title="Updated"),
            ephemeral=True)
        await callback(interaction, "programming", programming)
    """

    view1_general = View(timeout=None)
    view1_general.add_item(gender[0])
    view1_general.add_item(age[0])
    gender[0].callback = gender_callback
    age[0].callback = age_callback

    view2_games = View(timeout=None)
    for x in range(count_g):
        games[x].callback = games_callback
        view2_games.add_item(games[x])

    """
    view3_programming = View(timeout=None)
    for x in range(count_p):
        programming[x].callback = programming_callback
        view3_programming.add_item(programming[x])
    """

    channel = await client.fetch_channel(static.channels_id['self_roles'])
    await (await channel.fetch_message(self_roles_messages_id[0])).edit("\n## __**Genereles:**__", view=view1_general)
    await (await channel.fetch_message(self_roles_messages_id[1])).edit("\n## __**Games:**__", view=view2_games)
    #await (await channel.fetch_message(self_roles_messages_id[2])).edit("\n## __**Programmierung:**__", view=view3_programming)
