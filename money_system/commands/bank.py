from datetime import datetime

import discord
from discord.ext import commands
from discord.ui import View, Button


class Bank(commands.Cog):

    def __init__(self, bot):
        print(f"loaded {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="bank", description="Öffne das Bank Interface")
    async def cmd(self, ctx):
        view = View(timeout=None)
        buttons = [Button(label="Aktuelle Coins anzeigen", custom_id="cash", style=discord.ButtonStyle.blurple),
                   Button(label="Coins auszahlen", custom_id="cash_out", style=discord.ButtonStyle.green)]

        for btn in buttons:
            view.add_item(btn)
            btn.callback = globals()[f'{btn.custom_id}_callback']

        emb = discord.Embed(title="Bank Modul",
                            color=discord.Color.blurple(),
                            description=f"Willkommen in der Bank {ctx.author.mention}")
        emb.add_field(name="Was möchtest du machen?", value=" ")
        emb.set_footer(text=f"Solltest du irgendwelche fragen haben\nwende dich ans Dev Team\nUhrzeit:",
                       icon_url=ctx.guild.icon.url)
        emb.timestamp = datetime.now()

        await ctx.respond(embed=emb, view=view, ephemeral=True)


def setup(client):
    client.add_cog(Bank(client))


async def cash_callback(interaction: discord.Interaction):
    print("Cash")


async def cash_out_callback(interaction: discord.Interaction):
    print("Cash out")