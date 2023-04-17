import discord

from main import client


async def get_emoji(emoji_name):
    for i in client.guilds:
        emoji = discord.utils.get(i.emojis, name=emoji_name)
        return emoji