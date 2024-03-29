import asyncio
import calendar
from datetime import datetime

import aiohttp.client_exceptions
import pytz
from discord import Embed
from discord.ext import commands
import discord

import static


class Event_Reminder(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Tasks {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.user.id == static.bot_id:
            self.bot.loop.create_task(check_events(self.bot, 60))


def setup(client):
    client.add_cog(Event_Reminder(client))


async def check_events(client: discord.Client, time):
    while True:
        try:
            guild: discord.Guild = client.get_guild(static.duschpalast_guild_id)
            events = await guild.fetch_scheduled_events()

            
            utc = pytz.UTC
            now = datetime.now().replace(tzinfo=utc)

            for event in events:
                time_difference  = calendar.timegm(event.start_time.timetuple()) - calendar.timegm(now.timetuple())
                if -30 < time_difference < 30:
                    announcement = (
                        f"📢 **Aufgepasst, liebe <@&{static.roles_id['d-member']}>!** 🎉\n\n"
                        f"In Kürze wird ein Event stattfinden!\n\n"
                        f"**Event:** {event.name}\n"
                        f"**Startzeit:** <t:{calendar.timegm(event.start_time.timetuple())}:R>\n"
                        f"Schaut vorbei und erlebt gemeinsam mit uns unvergessliche Momente. Wir freuen uns auf eure Teilnahme!\n\n"
                        f"👉 Weitere Details findet ihr [hier]({event.url})."
                    )

                    event_channel = await client.fetch_channel(static.channels_id['news'])
                    await event_channel.send(announcement)

                    emb = Embed(color=0x00ffff,
                                title=f"**Bald findet das Event ```{event.name}``` statt!!**")

                    emb.set_author(name="Duschpalast",
                                   icon_url=guild.icon.url)

                    emb.set_footer(text=f"Dein Duschpalast Team",
                                   icon_url=guild.icon.url)
                    emb.add_field(
                        name="Du hattest dich als interessiert eingetragen, deshalb wären wir sehr erfreut, wenn du kommst.",
                        value=f"**[Klicke hier, um alles Informationen zum Event zu bekommen.]({event.url})**\nEvent Begin: <t:{calendar.timegm(event.start_time.timetuple())}:R>")

                    async for user in event.subscribers():
                        try:
                            await user.send(user.mention, embed=emb)
                        except discord.Forbidden:
                            continue

            await asyncio.sleep(time)

        except aiohttp.client_exceptions.ClientOSError as err:
            print(err)
            continue
