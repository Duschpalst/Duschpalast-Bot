import discord

from static import SQL, db
from utils.user.get_user_xp_lvl import get_xp_lvl


async def lvl_up_rewards(user: discord.User, xp_add):
    xp, lvl_before, percentage = await get_xp_lvl(user)
    xp, lvl_after, percentage = await get_xp_lvl(xp=(xp+xp_add))

    if lvl_before == lvl_after:
        return

    SQL.execute(f'UPDATE users SET coin = coin + 100 WHERE user_id = {user.id};')
    db.commit()