import discord
from discord.ext import commands
import calendar

import static



class On_Event_Create(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot

    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event: discord.ScheduledEvent):
        event_channel = await self.bot.fetch_channel(static.channels_id['news'])
        await event_channel.send(
            f"**Hey, liebe <@&{static.roles_id['d-member']}>! 🎉 Ein neues Event steht an!**\n\n"
            f"Wir freuen uns, euch mitteilen zu können, dass ein neues Event geplant wurde. Hier sind die Details:\n"
            f"**Event:** {event.name}\n"
            f"**Startzeit:** <t:{calendar.timegm(event.start_time.timetuple())}:R>\n"
            f"**Weitere Informationen:** [Klicke hier]({event.url})\n\n"
            f"Macht euch bereit und markiert euch den Termin! Wir freuen uns darauf, euch alle dort zu sehen. 🎮")




def setup(client):
    client.add_cog(On_Event_Create(client))
