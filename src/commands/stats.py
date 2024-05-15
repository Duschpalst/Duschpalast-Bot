from datetime import timedelta, datetime
import discord
from discord.ext import commands
import requests
from PIL import ImageFont, Image
from easy_pil import Editor, load_image_async
from pilmoji import Pilmoji

from static import SQL, emojis
from utils.user.cmd_reward import cmd_reward
from utils.user.get_user_xp_lvl import get_xp_lvl


class Stats(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="stats", description="📊 | Zeige dir deine Stats vom Server an")
    async def cmd(self, ctx: discord.ApplicationContext):
        await cmd_reward(ctx)

        await ctx.response.defer()
        user: discord.User = ctx.user
        guild: discord.Guild = ctx.guild

        SQL.execute(f'SELECT coin, msg_count, vc_time FROM users WHERE user_id = {user.id}')
        coins, msg_count, vc_time = SQL.fetchone()

        xp, lvl, rxp, percentage = await get_xp_lvl(user)
        SQL.execute(f'SELECT COUNT(*) FROM users WHERE xp > {xp};')
        rank = SQL.fetchone()[0] + 1

        name, id = user.name ,user.id

        joined_at = user.joined_at.strftime("%d.%m.%Y")

        base = Pilmoji(Image.open(f"assets/img/stats.png").convert("RGBA"))
        background = Image.open(requests.get(str(guild.icon.url), stream=True).raw).resize((696, 696))
        background = background.crop((0, 100, 696, 377))
        ima = Editor(Image.new(mode="RGB", size=(696, 901)))

        name = f"{name[:15]}..." if len(name) > 15 else name

        f40 = ImageFont.truetype("assets/fonts/ARLRDBD.TTF", 40)
        f30 = ImageFont.truetype("assets/fonts/ARLRDBD.TTF", 30)
        f24 = ImageFont.truetype("assets/fonts/ARLRDBD.TTF", 24)


        base.text((280, 245), name, font=f40, color="#EEEEEE")
        base.text((270, 315), f"🆔: {id}", font=f24, color="#EEEEEE")


        base.text((65, 440), "Level 📈", font=f30, color="#eeeeee")
        base.text((65, 490), str(lvl), font=f30, color="#a0a0a0")

        base.text((65, 585), f"Coins {emojis['duschcoin']}", font=f30, color="#eeeeee")
        base.text((65, 635), str(coins), font=f30, color="#a0a0a0")

        base.text((65, 690), "Zeit in", font=f30, color="#eeeeee")
        base.text((65, 720), "Sprachkanälen ⌚", font=f30, color="#eeeeee")
        d = datetime(1, 1, 1) + timedelta(seconds=int(vc_time))
        base.text((65, 780), str("%d / %d:%d:%d" % (d.day - 1, d.hour, d.minute, d.second)), font=f30, color="#a0a0a0")


        base.text((405, 440), "Rank 📋", font=f30, color="#eeeeee")
        base.text((405, 490), str(rank), font=f30, color="#a0a0a0")

        base.text((405, 555), "Gesendete", font=f30, color="#eeeeee")
        base.text((405, 585), "Nachrichten 💬", font=f30, color="#eeeeee")
        base.text((405, 635), str(msg_count), font=f30, color="#a0a0a0")

        base.text((405, 715), "Joined 📲", font=f30, color="#eeeeee")
        base.text((405, 780), joined_at, font=f30, color="#a0a0a0")


        if not user.avatar:
            profile = await load_image_async(str(user.default_avatar))
        else:
            profile = await load_image_async(str(user.avatar.url))

        profile = Editor(profile).resize((215, 215)).circle_image()

        ima.paste(background, (0, 0))
        ima.paste(base.image, (0, 0))

        ima.paste(profile, (56, 158))

        card = discord.File(fp=ima.image_bytes, filename="stats.png")
        await ctx.followup.send(file=card)


def setup(client):
    client.add_cog(Stats(client))
