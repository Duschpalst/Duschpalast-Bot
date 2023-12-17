import discord
from discord.ext import commands

from static import SQL, db


class Member_Events_Logger(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f'{member.name} ist dem Server beigetreten.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member.name} hat den Server verlassen.')

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            print(f'Die Rollen von {after.name} wurden aktualisiert.')

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            print(f'Der Name von {after.name} wurde geändert.')
        if before.avatar != after.avatar:
            print(f'Das Avatar von {after.name} wurde geändert.')

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        print(f'{user.name} wurde in {guild.name} verbannt.')

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        print(f'{user.name} wurde in {guild.name} entbannt.')

    @commands.Cog.listener()
    async def on_member_timeout(self, member):
        print(f'{member.name} wurde wegen Inaktivität entfernt.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member.name} wurde aus dem Server entfernt.')




def setup(client):
    client.add_cog(Member_Events_Logger(client))
