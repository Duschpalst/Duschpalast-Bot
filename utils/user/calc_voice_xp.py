import json
import time

import discord

import static
from static import *
from utils.user.lvl_up_rewards import lvl_up_rewards


async def calc_voice_xp(user):
    with open('assets/json/vc.json', 'r') as f:
        data = json.load(f)

    call_length = round(time.time()) - data[str(user.id)]
    SQL.execute(f'UPDATE users SET vc_time = vc_time + {call_length} WHERE user_id = {user.id}')
    db.commit()
    role = discord.utils.get(user.guild.roles, id=static.roles_id['booster'])
    multiplier = 1
    if role in user.roles:
        multiplier = static.booster_xp_multiplier

    xp = multiplier * ((call_length // 300 * call_xp_5min) + (call_length // 3600 * call_xp_60min))
    await lvl_up_rewards(user, xp)
    return xp
