import discord


async def get_emoji(emoji_name, bot):
    for i in bot.guilds:
        emoji = discord.utils.get(i.emojis, name=emoji_name)
        return emoji