import json
import time

import discord
from PIL import ImageFont
from discord import Option, Embed
from discord.ext import commands
from easy_pil import Editor, load_image_async

from functions import calc_voice_xp
from static import SQL, db


class Level(commands.Cog):

    def __init__(self, bot):
        print(f"loaded {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="level", description="Zeige dir dein Aktuelles Level an")
    async def cmd(self, ctx, benutzter: Option(discord.member.Member, "Benutzer", required=False)):
        user = benutzter or ctx.author
        if user.bot:
            await ctx.respond(embed=Embed(color=discord.Color.red(), title="Der Benutzer ist ein Bot"), ephemeral=True)
            return
        SQL.execute(f'select user_id from users where user_id="{user.id}"')
        result_userid = SQL.fetchone()

        if result_userid is None:
            SQL.execute('insert into users(user_id, user_name) values(?,?)', (user.id, str(user),))
            db.commit()

        SQL.execute(f'SELECT xp FROM users WHERE user_id = {user.id};')
        xp = SQL.fetchone()[0]

        SQL.execute(f'SELECT COUNT(*) FROM users WHERE xp > {xp};')
        rank = SQL.fetchone()[0]

        if xp == 0:
            lvl = xp // 150 + 1
        else:
            lvl = (xp - 1) // 150 + 1

        f125 = ImageFont.truetype("fonts/ARLRDBD.TTF", 125)
        f100 = ImageFont.truetype("fonts/ARLRDBD.TTF", 100)
        f60 = ImageFont.truetype("fonts/ARLRDBD.TTF", 60)

        background = Editor(f"img/levelcard.png")
        if not user.avatar:
            profile = await load_image_async(str(user.default_avatar))
        else:
            profile = await load_image_async(str(user.avatar.url))

        profile = Editor(profile).resize((350, 350)).circle_image()

        ima = Editor("img/levelcard.png")
        background.blend(image=ima, alpha=.5, on_top=False)

        background.paste(profile, (132, 187))

        if user.voice:
            Sxp = await calc_voice_xp(user) + xp
            Slvl = ((Sxp - 1) // 150 + 1)

            if Slvl - lvl != 0:
                background.text((2000, 463), f"+{Slvl - lvl}", font=f125, color="#323981", align="left")
                percent = 100
            else:
                percent = 100 / 150 * (Sxp - 150 * (Slvl - 1))

            # if Sxp > 150:
            #    Sxp = 150

            background.bar(
                (709, 476),
                max_width=1260,
                height=61,
                percentage=percent,
                fill="#323981",
                radius=16,
            )

        background.bar(
            (709, 476),
            max_width=1260,
            height=61,
            percentage=100 / 150 * (xp - 150 * (lvl - 1)),
            fill="#f10553",
            radius=16,
        )

        name = f"{str(user)[:20]}..." if len(str(user)) > 20 else str(user)
        background.text((1955, 50), f"Rank: #{rank + 1}", font=f125, color="#EEEEEE", align="right")
        background.text((725, 370), name, font=f100, color="#FFFFFF", align="left")
        background.text((725, 555), f"Level: {lvl}", font=f100, color="#f10553", align="left")
        background.text((1955, 555), f"{xp} / {lvl * 150} XP", font=f60, color="#EEEEEE", align="right")

        card = discord.File(fp=background.image_bytes, filename="img/levelcard.png")
        await ctx.respond(file=card)


def setup(client):
    client.add_cog(Level(client))
