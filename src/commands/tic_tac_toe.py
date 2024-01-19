import json
from datetime import datetime

import discord
from discord import Option, Embed
from discord.ext import commands
from discord.ui import View, Button

from utils.guilds.get_emoji import get_emoji
from utils.user.cmd_reward import cmd_reward
from static import emojis


class TicTacToe(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Command {self.__cog_name__} Cog")
        self.bot = bot

    @commands.slash_command(name="tic-tac-toe", description="🎲 | Tic Tac Toe")
    async def cmd(self, ctx: discord.ApplicationContext, benutzter: Option(discord.Member, "Benutzer", required=True)):
        await cmd_reward(ctx)

        user2 = benutzter
        user1 = ctx.user
        if user1 == user2:
            await ctx.respond(
                embed=Embed(color=discord.Color.red(), title="Du kannst nicht gegen dich selber Spielen!"),
                ephemeral=True)
            return

        if user2.bot:
            await ctx.respond(
                embed=Embed(color=discord.Color.red(), title="Du kannst nicht gegen einen Bot Spielen!"),
                ephemeral=True)
            return

        if await self.exist_game(user1.id, user2.id):
            await ctx.respond(
                embed=Embed(color=discord.Color.red(), title="Ein Spiel gegen diesem Spieler besteht bereits!"),
                ephemeral=True)
            return

        view = View(timeout=None)
        button = []
        for i in range(9):
            button.append(Button(label="-", custom_id=str(i), style=discord.ButtonStyle.gray, row=i // 3))

        for i in button:
            view.add_item(i)
            i.callback = self.btn_callback

        emb = Embed(
            color=0x2b2d31,
            title="Tic Tac Toe",
            description=f'> {user1.mention} (X) **VS** {user2.mention} (0)',
        )

        emb.add_field(name="",
                      value=f"{emojis['member']} | {user1.mention} ist dran.")

        emb.timestamp = datetime.utcnow()
        emb.set_author(name='Duschpalast Bot | Games', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Games')

        interaction: discord.Interaction = await ctx.respond(embed=emb,
                                                             view=view)
        msg_id = (await interaction.original_response()).id
        await self.safe_game(msg_id, [user1.id, user2.id], 0)

    async def exist_game(self, user1_id, user2_id):
        with open('assets/json/tic-tac-toe.json', 'r') as f:
            data = json.load(f)

        for i in data:
            if data[i][0][0] == user1_id or data[i][0][0] == user2_id:
                if data[i][0][1] == user1_id or data[i][0][1] == user2_id:
                    return True

    async def safe_game(self, msg_id, users, turn):
        with open('assets/json/tic-tac-toe.json', 'r') as f:
            data = json.load(f)

        data[str(msg_id)] = [users, turn]
        with open('assets/json/tic-tac-toe.json', 'w') as f:
            json.dump(data, f)

    async def btn_callback(self, interaction: discord.Interaction):
        id = str(interaction.message.id)
        with open('assets/json/tic-tac-toe.json', 'r') as f:
            data = json.load(f)

        if interaction.user.id != data[id][0][data[id][1]]:
            await interaction.response.send_message(
                embed=Embed(color=discord.Color.red(), title="Du bist nicht dran oder spielst nicht mit!"),
                ephemeral=True)
            return

        view = View(timeout=None)
        button = []
        current_game = []

        row = 0
        for i in interaction.message.components:
            row += 1
            for x in i.children:
                if x.custom_id == interaction.custom_id:
                    if x.label != "-":
                        await interaction.response.send_message(
                            embed=Embed(color=discord.Color.red(), title="Das Feld ist bereits belegt!"),
                            ephemeral=True)
                        return

                    if data[id][1] == 0:
                        x.label = "X"
                        x.style = discord.ButtonStyle.blurple
                        turn = 1
                    elif data[id][1] == 1:
                        x.label = "0"
                        x.style = discord.ButtonStyle.green
                        turn = 0

                current_game.append(x.label)
                button.append(Button(label=x.label, custom_id=x.custom_id, style=x.style, row=row))

        win = await self.detect_win(current_game)
        draw = False
        if not "-" in current_game:
            draw = True

        for i in button:
            view.add_item(i)
            if not win and not draw:
                i.callback = self.btn_callback

        if win:
            txt = f"<@{data[id][0][win - 1]}> hat gewonnen!"
        elif draw:
            txt = "Das Spiel ist ein Unentschieden."
        else:
            txt = f"<@{data[id][0][turn]}> ist dran."

        emb = Embed(
            color=0x2b2d31,
            title="Tic Tac Toe",
            description=f'> <@{data[id][0][0]}> (X) **VS** <@{data[id][0][1]}> (0)',
        )

        emb.add_field(name="",
                      value=f"{emojis['member']} | {txt}")

        emb.timestamp = datetime.utcnow()
        emb.set_author(name='Duschpalast Bot | Games', icon_url=self.bot.user.avatar.url)
        emb.set_footer(text='Duschpalast Bot | Games')

        await interaction.response.edit_message(embed=emb,
                                                view=view)

        if win or draw:
            del data[id]
        else:
            data[id] = [data[id][0], turn]

        with open('assets/json/tic-tac-toe.json', 'w') as f:
            json.dump(data, f)

    async def detect_win(self, game):
        win_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        for i in win_combinations:
            if game[i[0]] == game[i[1]] and game[i[0]] == game[i[2]] and game[i[0]] != "-":
                if game[i[0]] == "X":
                    return 1
                elif game[i[0]] == "0":
                    return 2

        return False

def setup(client):
    client.add_cog(TicTacToe(client))

