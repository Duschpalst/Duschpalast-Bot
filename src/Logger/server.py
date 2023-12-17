import discord
from discord.ext import commands

from static import SQL, db


class Server_Events_Logger(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        print(channel.guild.owner_id)
        print(f'Ein neuer Kanal wurde erstellt: {channel.name} in Server: {channel.guild.name}')

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        print(f'Ein Kanal wurde aktualisiert: {before.name} in Server: {before.guild.name}')

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        print(f'Ein Kanal wurde gelöscht: {channel.name} in Server: {channel.guild.name}')

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        print(f'Eine neue Rolle wurde erstellt: {role.name} in Server: {role.guild.name}')

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        print(f'Eine Rolle wurde aktualisiert: {before.name} in Server: {before.guild.name}')

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        print(f'Eine Rolle wurde gelöscht: {role.name} in Server: {role.guild.name}')

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        print(f'Der Server wurde aktualisiert: {before.name}')




def setup(client):
    client.add_cog(Server_Events_Logger(client))
