import discord
from PIL import ImageFont
from discord.ext import commands
from easy_pil import Editor

from static import SQL, get_client


class Leaderbord(commands.Cog):

    def __init__(self, bot):
        print(f"loaded {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="leaderboard", description="Zeige dir top 10 von den Level an")
    async def cmd(self, ctx):
        SQL.execute('SELECT user_id, xp FROM users ORDER BY xp DESC')
        res = SQL.fetchmany(10)

        f60 = ImageFont.truetype("fonts/ARLRDBD.TTF", 60)

        background = Editor(f"img/leaderboard.png")

        ima = Editor("img/leaderboard.png")
        background.blend(image=ima, alpha=.5, on_top=False)

        y = 484
        for x in res:
            if x[1] == 0:
                lvl = x[1] // 150 + 1
            else:
                lvl = (x[1] - 1) // 150 + 1

            client = await get_client()
            user_name = await client.fetch_user(x[0])
            name = f"{str(user_name.name)[:15]}..." if len(str(user_name.name)) > 15 else str(user_name.name)

            background.text((300, y), name, font=f60, color="#EEEEEE", align="left")
            background.text((970, y), str(lvl), font=f60, color="#EEEEEE", align="right")
            y += 143

        card = discord.File(fp=background.image_bytes, filename="img/leaderboard.png")
        await ctx.respond(file=card)


def setup(client):
    client.add_cog(Leaderbord(client))
