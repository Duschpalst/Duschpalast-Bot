import json
import time

import discord


async def calc_voice_xp(member):
    with open('assets/json/vc.json', 'r') as f:
        data = json.load(f)

    call_length = round(time.time()) - data[str(member.id)]
    role = discord.utils.get(member.guild.roles, id=853208244721287179)
    multiplier = 1
    if role in member.roles:
        multiplier = 2

    return multiplier * ((call_length // 300 * 10) + (call_length // 3600 * 5))
