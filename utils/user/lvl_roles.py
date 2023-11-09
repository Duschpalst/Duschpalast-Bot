import discord

import static
from utils.user.get_user_xp_lvl import get_xp_lvl


async def lvl_roles(member: discord.Member):
    xp, lvl, percentage = await get_xp_lvl(member)

    if lvl < 25:
        result = 0
    else:
        result = (lvl // 25) if lvl < 100 else 4

    lvl_role = member.guild.get_role(static.lvl_roles_id[result])

    if lvl_role in member.roles:
        return

    for i in static.lvl_roles_id:
        remove_roles = member.guild.get_role(i)
        await member.remove_roles(remove_roles)

    await member.add_roles(lvl_role, atomic=True)