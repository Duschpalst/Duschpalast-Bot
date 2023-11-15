import json
import discord
from discord.ext import commands
import time

import static
from static import SQL, db
from utils.user.calc_voice_xp import calc_voice_xp
from utils.user.first_db_write_check import first_write_check
from utils.user.lvl_roles import lvl_roles


class On_Voice_State_Update(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        bcg = before.channel.guild if before.channel else None
        acg = after.channel.guild if after.channel else None

        if not (bcg != acg or before.self_deaf or after.self_deaf) or member.bot:
            return

        await first_write_check(member)

        with open('assets/json/vc.json', 'r') as f:
            data = json.load(f)

        if not member.voice or after.channel.id == static.channels_id['afk'] or after.self_deaf:
            try:
                SQL.execute(f'UPDATE users SET xp = xp + {await calc_voice_xp(member)} WHERE user_id = {member.id};')
                db.commit()

                del data[str(member.id)]
            except KeyError:
                return
        else:
            data[str(member.id)] = round(time.time())
        with open('assets/json/vc.json', 'w') as f:
            json.dump(data, f)

        if self.bot.user.id == static.bot_id:
            await lvl_roles(member)


def setup(client):
    client.add_cog(On_Voice_State_Update(client))
