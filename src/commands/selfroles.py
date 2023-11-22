from io import BytesIO
import discord
import requests
from PIL import Image
from discord import Embed, default_permissions
from discord.ext import commands
from discord.ui import View, Button, InputText

from static import SQL, db
from src.user_interactions.self_roles import self_roles


class SelfRoles(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot
        global client
        client = bot

    @commands.slash_command(name="selfroles", description="🛠️ | Bearbeite die Self Roles")
    @default_permissions(kick_members=True)
    async def cmd(self, ctx: discord.ApplicationContext):
        view = View(timeout=30)
        button1 = Button(label="+ Gaming Option", custom_id="add_gaming_option", style=discord.ButtonStyle.green)
        button2 = Button(label="+ Programming Option", custom_id="add_programming_option",
                         style=discord.ButtonStyle.green)
        button3 = Button(label="- Gaming Option", custom_id="remove_gaming_option", style=discord.ButtonStyle.red)
        button4 = Button(label="- Programming Option", custom_id="remove_programming_option",
                         style=discord.ButtonStyle.red)

        button1.callback = btn_callback
        button2.callback = btn_callback
        button3.callback = btn_callback
        button4.callback = btn_callback

        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)

        await ctx.respond(embed=Embed(color=discord.Color.purple(), title="Was Möchstes du machen?"), ephemeral=True,
                          view=view)


def setup(client):
    client.add_cog(SelfRoles(client))


async def btn_callback(interaction):
    if interaction.custom_id.startswith("add_"):
        modal = AddModal(title="Erstelle eine Neue Self Role Option", custom_id=interaction.custom_id)
    elif interaction.custom_id.startswith("remove_"):
        modal = RemoveModal(title="Entferne eine Self Role Option", custom_id=interaction.custom_id)
    else:
        return

    await interaction.response.send_modal(modal)


class AddModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            InputText(
                label="Name",
                placeholder="Wie Soll die neue Rolle heiẞen?"
            ),

            InputText(
                label="Icon Id",
                placeholder="Ids auf: emoji.gg",
            ),

            InputText(
                label="Emoji Name",
                placeholder="Wie Soll der neue Emoji heiẞen?",
            ),

            *args,
            **kwargs
        )

    async def callback(self, interaction):
        await adding_option(self.children[0].value, self.children[1].value, self.children[2].value, interaction,
                            self.custom_id)


class RemoveModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            InputText(
                label="Name",
                placeholder="Wie heiẞt die Rolle die du entfernen möchtest?"
            ),

            *args,
            **kwargs
        )

    async def callback(self, interaction):
        await remove_option(self.children[0].value, interaction,
                            self.custom_id)


async def adding_option(name, icon_id, emoji_name, interaction, id):
    try:
        if emoji_name in str(interaction.guild.emojis) or name in str(interaction.guild.roles):
            await interaction.response.send_message(
                embed=Embed(color=discord.Color.red(), title="Dieser Name ist bereits belegt!"),
                ephemeral=True)
            return

        url = f'https://cdn3.emoji.gg/emojis/{icon_id}.png'
        r = requests.get(url, allow_redirects=True)
        img = Image.open(BytesIO(r.content), mode='r')
        b = BytesIO()
        img.save(b, format="PNG")
        await interaction.guild.create_custom_emoji(image=b.getvalue(), name=emoji_name)
    except:
        await interaction.response.send_message(
            embed=Embed(color=discord.Color.red(), title="Es ist ein Fehler aufgetreten!"),
            ephemeral=True)
        return

    role = await interaction.guild.create_role(name=name, permissions=discord.Permissions.none())
    options = {"add_gaming_option": 1015926714079133736, "add_programming_option": 1015926956144992327}
    await role.edit(position=(interaction.guild.get_role(options.get(id)).position - 1))

    options = {"add_gaming_option": "self_roles_games", "add_programming_option": "self_roles_programming"}
    SQL.execute(f'INSERT INTO {options.get(id)}(name, emoji_name, role_id) values(?,?,?);', (name.lower(), emoji_name, role.id))
    db.commit()

    await interaction.response.send_message(embed=Embed(color=discord.Color.green(), title="Erfolgreich!"),
                                            ephemeral=True)

    await self_roles(client)


async def remove_option(name, interaction, id):
    options = {"remove_gaming_option": "self_roles_games", "remove_programming_option": "self_roles_programming"}
    SQL.execute(f'SELECT * FROM {options.get(id)} WHERE LOWER(name) = "{name.lower()}";')
    res = SQL.fetchone()
    if res is None:
        await interaction.response.send_message(
            embed=Embed(color=discord.Color.red(), title="Dieser Name existiert nicht!"),
            ephemeral=True)
        return

    emoji = ""
    for i in client.guilds:
        emoji = discord.utils.get(i.emojis, name=res[1])
    await interaction.guild.delete_emoji(emoji)
    # await client.delete_role(interaction.guild, res[2])
    role = discord.utils.get(interaction.guild.roles, id=res[2])
    await role.delete()
    SQL.execute(f'DELETE FROM {options.get(id)} WHERE name = "{res[0]}";')
    db.commit()

    await interaction.response.send_message(embed=Embed(color=discord.Color.green(), title="Erfolgreich!"),
                                            ephemeral=True)

    await self_roles(client)

