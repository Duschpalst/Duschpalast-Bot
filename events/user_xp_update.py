import json
import time

import discord

from functions.calc_voice_xp import calc_voice_xp
from static import SQL, db, get_client


async def first_write_check(user):
    SQL.execute(f'select user_id from users where user_id="{user.id}"')
    result_userid = SQL.fetchone()

    if result_userid is None:
        SQL.execute('insert into users(user_id, user_name) values(?,?)', (user.id, str(user),))
        db.commit()


async def voice_update(member, before: discord.VoiceState, after: discord.VoiceState):
    if member.bot:
        return
    await first_write_check(member)

    with open('storage/vc.json', 'r') as f:
        data = json.load(f)

    if not member.voice or after.channel.id == 843754571377147934 or after.self_deaf:
        try:
            SQL.execute(f'UPDATE users SET xp = xp + {await calc_voice_xp(member)} WHERE user_id = {member.id};')
            db.commit()

            del data[str(member.id)]
        except KeyError:
            return
    else:
        data[str(member.id)] = round(time.time())
    with open('storage/vc.json', 'w') as f:
        json.dump(data, f)


async def message_update(message):
    await first_write_check(message.author)

    role = discord.utils.get(message.guild.roles, id=853208244721287179)
    if role in message.author.roles:
        multiplier = 2
    else:
        multiplier = 1
    SQL.execute(f'UPDATE users SET msg_count = msg_count + 1 WHERE user_id = {message.author.id}')
    SQL.execute(f'UPDATE users SET xp = xp + {multiplier * 1} WHERE user_id = {message.author.id}')
    db.commit()
