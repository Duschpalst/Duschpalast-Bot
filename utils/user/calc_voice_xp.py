import json
import time

import discord

import static
from static import SQL, db


async def calc_voice_xp(user):
    with open('assets/json/vc.json', 'r') as f:
        data = json.load(f)

    call_length = round(time.time()) - data[str(user.id)]
    SQL.execute(f'UPDATE users SET vc_time = vc_time + {call_length} WHERE user_id = {user.id}')
    db.commit()
    role = discord.utils.get(user.guild.roles, id=static.boster_role)
    multiplier = 1
    if role in user.roles:
        multiplier = 2

    return multiplier * ((call_length // 300 * 10) + (call_length // 3600 * 5))
