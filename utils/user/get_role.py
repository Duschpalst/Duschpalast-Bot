import discord

import static
from static import client


async def get_role_by_id(id):
    guild: discord.Guild = client.get_guild(static.duschpalast_guild_id)
    return discord.utils.get(guild.roles, id=id)


async def get_role_by_name(name):
    guild: discord.Guild = client.get_guild(static.duschpalast_guild_id)
    return discord.utils.get(guild.roles, name=name)
