import discord


async def join(member, client):
    await client.change_presence(activity=discord.Game(name=f"👋 {member}"))