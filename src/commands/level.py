import discord
from PIL import ImageFont
from discord import Option, Embed
from discord.ext import commands
from easy_pil import Editor, load_image_async

import static
from utils.user.calc_voice_xp import calc_voice_xp
from utils.user.get_user_xp_lvl import get_xp_lvl
from static import SQL, db


class Level(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="level", description="Zeige dir dein Aktuelles Level an")
    async def cmd(self, ctx: discord.ApplicationContext, benutzter: Option(discord.Member, "Benutzer", required=False)):
        user = benutzter or ctx.author
        if user.bot:
            await ctx.respond(embed=Embed(color=discord.Color.red(), title="Der Benutzer ist ein Bot"), ephemeral=True)
            return

        xp, lvl, percentage = await get_xp_lvl(user)

        SQL.execute(f'SELECT COUNT(*) FROM users WHERE xp > {xp};')
        rank = SQL.fetchone()[0]

        f125 = ImageFont.truetype("assets/fonts/ARLRDBD.TTF", 125)
        f100 = ImageFont.truetype("assets/fonts/ARLRDBD.TTF", 100)
        f60 = ImageFont.truetype("assets/fonts/ARLRDBD.TTF", 60)

        background = Editor(f"assets/img/levelcard.png")
        if not user.avatar:
            profile = await load_image_async(str(user.default_avatar))
        else:
            profile = await load_image_async(str(user.avatar.url))

        profile = Editor(profile).resize((350, 350)).circle_image()

        ima = Editor("assets/img/levelcard.png")
        background.blend(image=ima, alpha=.5, on_top=False)

        background.paste(profile, (132, 187))

        if user.voice:
            Sxp = await calc_voice_xp(user) + xp
            xp, Slvl, Spercentage = await get_xp_lvl(xp=Sxp)

            if Slvl - lvl != 0:
                background.text((2000, 463), f"+{Slvl - lvl}", font=f125, color="#323981", align="left")
                percent = 100
            else:
                percent = Spercentage

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
            percentage=percentage,
            fill="#f10553",
            radius=16,
        )

        if user.discriminator == "0":
            user = user.name
        
        name = f"{str(user)[:20]}..." if len(str(user)) > 20 else str(user)
        background.text((1955, 50), f"Rank: #{rank + 1}", font=f125, color="#EEEEEE", align="right")
        background.text((725, 370), name, font=f100, color="#FFFFFF", align="left")
        background.text((725, 555), f"Level: {lvl}", font=f100, color="#f10553", align="left")
        background.text((1955, 555), f"{xp} / {250 + (lvl-1) * 10} XP", font=f60, color="#EEEEEE", align="right")

        card = discord.File(fp=background.image_bytes, filename="img/levelcard.png")
        await ctx.respond(file=card)


class RemoveLevel(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.has_permissions(kick_members=True)
    @commands.slash_command(name="remove-level", description="Lösche Level von einem User")
    async def cmd(self, ctx: discord.ApplicationContext, benutzter: Option(discord.Member, "Benutzer", required=True), rlvl: Option(int, "Zu Löschende Level", required=True, min_value=1)):
        user = benutzter
        if user.bot:
            await ctx.respond(embed=Embed(color=discord.Color.red(), title="Der Benutzer ist ein Bot"), ephemeral=True)
            return

        xp, lvl, percentage = await get_xp_lvl(user)

        rxp = rlvl * 250 + sum((lvl - i - 1) * 10 for i in range(rlvl))

        if rxp > xp:
            rxp = xp
            ylvl = 1
        else:
            xp, ylvl, percentage = await get_xp_lvl(xp=rxp)

        SQL.execute(f'UPDATE users SET xp = xp - {rxp} WHERE user_id = {user.id};')
        db.commit()

        await ctx.respond(embed=Embed(color=discord.Color.green(), title="Fertig", description=f"Altes Level: {lvl}\nGelöschte Level: {rlvl}\nJetziges Level: {ylvl}"), ephemeral=True)
        channel = await self.bot.fetch_channel(static.channels_id['log'])
        await channel.send(embed=Embed(color=discord.Color.red(), title=f"{ctx.author} Löschte Level vom User: {user}", description=f"Altes Level: {lvl}\nGelöschte Level: {rlvl}\nJetziges Level: {ylvl}"))


def setup(client):
    client.add_cog(Level(client))
    client.add_cog(RemoveLevel(client))
