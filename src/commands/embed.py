import re
from ast import literal_eval
from datetime import datetime
import discord
from discord import Option, Embed, default_permissions
from discord.ext import commands
from discord.ui import View, Button, InputText

from static import emojis, client
from utils.user.cmd_reward import cmd_reward


class EmbedCreator(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="embed", description="🗑️ | Erstelle ein Embed")
    @default_permissions(kick_members=True)
    async def cmd(self, ctx: discord.ApplicationContext, channel: Option(discord.TextChannel, "Channel", required=True)):
        await cmd_reward(ctx)

        msg = await start_page(channel.id)
        await ctx.respond(embeds=msg[0], view=msg[1], ephemeral=True)


def setup(client):
    client.add_cog(EmbedCreator(client))


async def start_page(channel_id, embed_data=None):
    created_emb = None
    error_emb = None

    emb = Embed(
        color=0x2b2d31,
        title=f'{emojis["chat"]} × Hier kannst du ein **Embed** erstellen.',
        description=f'',
    )

    emb.timestamp = datetime.now()
    emb.set_author(name='Duschpalast Bot | Embed Creator', icon_url=client.user.avatar.url)
    emb.set_footer(text='Duschpalast Bot | Embed Creator')

    emb.add_field(
        name=f"{emojis['info']} | Erklärung",
        value="> **↣ 1:** [Klicke hier](https://embed.dan.onl/) oder unten auf den Knopf, um auf die Webseite zu gelangen und ein Embed zu erstellen.\n"
              "> **↣ 2:** Sobald du zufrieden bist mit deinem Embed, wähle beim Output **'JSON representation'**.\n"
              "> **↣ 3:** Kopiere dann den gesamten Output.\n"
              "> **↣ 4:** Klicke unten auf **Embed** und füge den zuvor kopierten Code ein.\n"
              "> **↣ 5:** Überprüfe dein Embed, ob es dir gefällt.\n"
              "> **↣ 6:** Wenn du zufrieden bist, klicke auf **Fertig** und sende das Embed ab.\n",
        inline=True
    )

    if embed_data:
        try:
            embed_data = re.sub(r'\btrue\b', 'True', embed_data)
            embed_data = literal_eval(embed_data)

            created_emb = Embed(
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
                title="Fehler",
                description=f'> ️{emojis["cross"]} × Ein **Fehler** ist aufgetreten. Bitte prüfe, ob du den **JSON-Code** richtig kopiert und eingefügt hast.',
            )

    view = View(timeout=None)
    button1 = Button(label="Embed", custom_id="embed", style=discord.ButtonStyle.blurple)
    button2 = Button(label="Creator Webseite", url="https://embed.dan.onl/")
    button3 = Button(label="Fertig", custom_id="done", style=discord.ButtonStyle.green, disabled=not bool(created_emb))

    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    async def btn_callback(interaction: discord.Interaction):
        if interaction.custom_id == "embed":
            await interaction.response.send_modal(EmbedModal(title="Embed Code", custom_id=str(channel_id)))
        elif interaction.custom_id == "done":
            selected_channel = await client.fetch_channel(channel_id)
            await selected_channel.send(embed=created_emb)

            await interaction.response.edit_message(embed=Embed(color=discord.Color.green(), title="Fertig"), view=None)

    button1.callback = btn_callback
    button2.callback = btn_callback
    button3.callback = btn_callback

    if created_emb:
        return [emb, created_emb], view
    elif error_emb:
        return [emb, error_emb], view
    else:
        return [emb], view


class EmbedModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(
            InputText(
                label="JSON-Code",
                placeholder="Füge hier den JSON-Code von https://embed.dan.onl/ ein",
                style=discord.InputTextStyle.long
            ),

            *args,
            **kwargs
        )

    async def callback(self, interaction: discord.Interaction):
        msg = await start_page(self.custom_id, self.children[0].value)
        await interaction.response.edit_message(embeds=msg[0], view=msg[1])
