import discord
from discord.ext import commands

from static import SQL, db


class Message_Events_Logger(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot





def setup(client):
    client.add_cog(Message_Events_Logger(client))
