import discord

import static
from static import SQL, db
from utils.user.add_last_transaction import add_last_transaction
from utils.user.get_user_xp_lvl import get_xp_lvl


async def lvl_up_rewards(user: discord.User, xp_add):
    xp, lvl_before, rxp, percentage = await get_xp_lvl(user)
    xp, lvl_after, rxp, percentage = await get_xp_lvl(xp=(xp+xp_add))

    if lvl_before == lvl_after:
        return

    await add_last_transaction(user, 'add', 'Level up Belohnung', static.lvl_up_reward)
    SQL.execute(f'UPDATE users SET coin = coin + {static.lvl_up_reward} WHERE user_id = {user.id};')
    db.commit()