import discord
from discord.ext import commands

from static import SQL, db


class Voice_Events_Logger(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if before.channel != after.channel:
            if after.channel is not None:
                print(f'{member.name} ist dem Sprachkanal {after.channel.name} beigetreten.')
            elif before.channel is not None:
                print(f'{member.name} hat den Sprachkanal {before.channel.name} verlassen.')
            else:
                print(f'{member.name} hat einen Sprachkanal betreten oder verlassen.')
        else:
            print(f'{member.name} hat den Sprachkanal {after.channel.name} gewechselt.')




def setup(client):
    client.add_cog(Voice_Events_Logger(client))
