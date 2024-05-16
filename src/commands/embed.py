import datetime

import discord
from discord import Option, Embed, default_permissions
from discord.ext import commands
from discord.ui import View, Button, InputText, Select

from static import emojis
from utils.user.cmd_reward import cmd_reward


class Embed(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="embed", description="🗑️ | Erstelle ein Embed")
    @default_permissions(kick_members=True)
    async def cmd(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel, "Channel", required=True)):
        await cmd_reward(ctx)

        msg = await start_page()
        await ctx.respond(embed=msg[0], view=msg[1], ephemeral=True)


def setup(client):
    client.add_cog(Embed(client))


async def start_page(embed_data: discord.Embed = None):
    emb = Embed(
        color=0x2b2d31,
        title="",
        description=f'> ️{emojis["EMOJI"]} × Hier kannst du ein **Embed** erstellen.',
    )

    emb.timestamp = datetime.now()
    emb.set_author(name='Duschpalast Bot | Embed', icon_url=self.bot.user.avatar.url)
    emb.set_footer(text='Duschpalast Bot | Embed')

    emb.add_field(
        name=f"{emojis['EMOJI']} | Erklärung",
        value=f"↣ 1: [Klicke Hier](https://embed.dan.onl/) oder unten auf den Knopf um auf die Webseite zu kommen um ein Embed zu erstellen\n"
              f'↣ 2: Sobald du zufrieden bist mit deinem Embed, wähle beim Output **"JSON representation"**\n'
              f'↣ 3: Kopiere dann den Kompletten Output\n'
              f'↣ 4: Klicken unten auf **Embed** und Füge den Eben Kopierten Code ein\n'
              f'↣ 5: Gucke dir dein Embed nochmal an, ob es dir gefällt\n'
              f'↣ 6: Sobald es dir gefällt, klicke auf **Fertig** und sende somit das Embed ab\n',
        inline=True
    )

    if embed_data:
        try:
            created_emb = discord.Embed(
                title=embed_data.get('title'),
                url=embed_data.get('url'),
                description=embed_data.get('description'),
                color=discord.Color(int(embed_data.get('color').strip('#'), 16))
            )

            if 'author' in embed_data:
                created_emb.set_author(name=embed_data['author'].get('name'), url=embed_data['author'].get('url'))

            if 'footer' in embed_data:
                created_emb.set_footer(text=embed_data['footer'].get('text'), icon_url=embed_data['footer'].get('icon_url'))

            if 'image' in embed_data:
                created_emb.set_image(url=embed_data['image'].get('url'))

            if 'thumbnail' in embed_data:
                created_emb.set_thumbnail(url=embed_data['thumbnail'].get('url'))

            if 'timestamp' in embed_data:
                created_emb.timestamp = datetime.utcfromtimestamp(embed_data['timestamp'] / 1000)

            for field in embed_data.get('fields', []):
                created_emb.add_field(name=field.get('name'), value=field.get('value'), inline=field.get('inline', False))


        except:
            error_emb = Embed(
                color=0xFF0000,
                title="",
                description=f'> ️{emojis["EMOJI"]} × Hier kannst du ein **Embed** erstellen.',
            )

    view = View(timeout=None)
    button1 = Button(label="Embed", custom_id="embed", style=discord.ButtonStyle.blurple)
    button2 = Button(label="Creator Webseite", url="https://embed.dan.onl/")
    button3 = Button(label="Fertig", custom_id="done", style=discord.ButtonStyle.green, disabled=(if not embed_data))

    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    button1.callback = btn_callback
    button2.callback = btn_callback
    button3.callback = btn_callback

    return emb


async def btn_callback(interaction: discord.Interaction):
    print(interaction)
    print(interaction.custom_id)
    if interaction.custom_id == "embed":
        await interaction.response.send_modal(EmbedModal(title="Embed Code"))


class EmbedModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            InputText(
                label="JSON Code",
                placeholder="Füge hier den JSON Code von https://embed.dan.onl/ ein",
                style=discord.TextStyle.long
            ),

            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction):
        print(interaction)
        print(self.children[0].value)

        await interaction.response.edit_message(embed=(await start_page(interaction.guild))[0], view=view)
