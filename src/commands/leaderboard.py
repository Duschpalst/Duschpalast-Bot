import discord
from PIL import ImageFont
from discord.ext import commands
from easy_pil import Editor

from static import SQL
from utils.user.get_user_xp_lvl import get_xp_lvl


class Leaderbord(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="leaderboard", description="Zeige dir top 10 von den Level an")
    async def cmd(self, ctx: discord.ApplicationContext):
        SQL.execute('SELECT user_id, xp FROM users ORDER BY xp DESC')
        res = SQL.fetchmany(10)

        f60 = ImageFont.truetype("assets/fonts/ARLRDBD.TTF", 60)

        background = Editor(f"assets/img/leaderboard.png")

        ima = Editor("assets/img/leaderboard.png")
        background.blend(image=ima, alpha=.5, on_top=False)

        y = 484
        for x in res:
            xp, lvl, percentage = await get_xp_lvl(xp=x[1])

            user_name = await self.bot.fetch_user(x[0])
            name = f"{str(user_name.name)[:15]}..." if len(str(user_name.name)) > 15 else str(user_name.name)

            background.text((300, y), name, font=f60, color="#EEEEEE", align="left")
            background.text((970, y), str(lvl), font=f60, color="#EEEEEE", align="right")
            y += 143

        card = discord.File(fp=background.image_bytes, filename="assets/img/leaderboard.png")
        await ctx.respond(file=card)


def setup(client):
    client.add_cog(Leaderbord(client))
