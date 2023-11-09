import discord


async def get_emoji(emoji_name, client):
    for i in client.guilds:
        emoji = discord.utils.get(i.emojis, name=emoji_name)
        return emoji