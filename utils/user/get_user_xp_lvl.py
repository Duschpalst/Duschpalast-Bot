import discord

from static import SQL
from utils.user.first_db_write_check import first_write_check


async def get_xp_lvl(user: discord.Member =None, xp=None):
    if xp is None:
        await first_write_check(user)

        SQL.execute(f'SELECT xp FROM users WHERE user_id = {user.id};')
        xp = SQL.fetchone()[0]

    base_xp = 250
    xp_increase = 10
    rxp = xp
    lvl = 1

    while rxp >= base_xp:
        rxp -= base_xp
        base_xp += xp_increase
        lvl += 1

    percentage = 100 / base_xp * rxp

    return xp, lvl, percentage
