import asyncio

import discord.errors
from discord.ext import commands

import static


class Update_Stats_Channel(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Tasks {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.user.id == 1054069404410855466:
            self.bot.loop.create_task(update_stats_channels(self.bot, 900))


def setup(client):
    client.add_cog(Update_Stats_Channel(client))


async def update_stats_channels(client, time):
    while True:
        try:
            await asyncio.sleep(time)
            all_channel = await client.fetch_channel(static.channels_id['all'])
            member_channel = await client.fetch_channel(static.channels_id['member'])
            bots_channel = await client.fetch_channel(static.channels_id['bots'])
            in_voice_channel = await client.fetch_channel(static.channels_id['in_voice'])
            guild = all_channel.guild
            m_count = 0
            b_count = 0
            in_vc_count = 0
            for usr in guild.members:
                if not usr.bot:
                    m_count += 1
                else:
                    b_count += 1

                if usr.voice:
                    in_vc_count += 1

            await all_channel.edit(name=f"Alle Mitglieder: {len(guild.members)}")
            await member_channel.edit(name=f"Mitglieder: {m_count}")
            await bots_channel.edit(name=f"Bots: {b_count}")
            await in_voice_channel.edit(name=f"Im Channel: {in_vc_count}")

        except discord.errors.DiscordServerError:
            continue
