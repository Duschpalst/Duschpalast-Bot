from datetime import datetime
import discord
from discord import Embed
from discord.ext import commands

from static import SQL, db


class Server_Events_Logger(commands.Cog):

    def __init__(self, bot):
        print(f"loaded Event {self.__cog_name__} Cog")
        self.bot = bot
        self.log_channel = None


    @commands.Cog.listener()
    async def on_ready(self):
        self.log_channel = await self.bot.fetch_channel(1100879059480739932)


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        emb = Embed(color=0x3498db,
                    title="Es wurde eine Änderung am Server gemacht.")
        emb.timestamp = datetime.utcnow()
        emb.set_author(name=f'{channel.guild.owner}',
                       icon_url=channel.guild.owner.avatar.url)
        emb.add_field(name='Ein neuer Channel wurde erstellt:',
                      value=f'`{channel.name}`')

        log_channel = await self.bot.fetch_channel(1100879059480739932)
        await log_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        emb = Embed(color=0x3498db,
                    title="Es wurde eine Änderung am Server gemacht.")
        emb.timestamp = datetime.utcnow()

        async for entry in after.guild.audit_logs(action=discord.AuditLogAction.channel_update, limit=1):
            target_channel = entry.target
            if target_channel.id == after.id:
                emb.set_author(name=f'{entry.user}',
                               icon_url=entry.user.avatar.url)

        changes = ""

        if before.name != after.name:
            changes = f'Name: `{before.name}` ➔ `{after.name}`'

        if before.category != after.category:
            old_category = self.bot.get_channel(before.category_id)
            new_category = self.bot.get_channel(after.category_id)
            changes = (f'Channel: {after.mention}\n'
                       f'Kategorie: `{old_category.name}` ➔ `{new_category.name}`')

        # Check for permission overwrites changes
        if before.overwrites != after.overwrites:
            for bef, aft in zip(before.overwrites.items(), after.overwrites.items()):
                if bef[1] != aft[1]:
                    changed_overwrites = []
                    for perm in discord.Permissions.VALID_FLAGS:
                        before_permission = getattr(bef[1], perm)
                        after_permission = getattr(aft[1], perm)

                        if before_permission != after_permission:
                            changed_overwrites.append(f'** - {perm.replace("_", " ").title()} ➔ `{after_permission}`**\n')

                    changes = (f"Channel: {after.mention}\n"
                               f"Für: {aft[0].mention}\n" + ''.join(changed_overwrites))


        print(changes)

        if changes:
            emb.add_field(name='Ein Channel wurde aktualisiert:',
                          value=changes)

            #log_channel = await self.bot.fetch_channel(1100879059480739932)
            await self.log_channel.send(embed=emb)


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        emb = Embed(color=0x3498db,
                    title="Es wurde eine Änderung am Server gemacht.")
        emb.timestamp = datetime.utcnow()

        async for entry in channel.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=1):
            target_channel = entry.target
            if target_channel.id == channel.id:
                emb.set_author(name=f'{entry.user}',
                               icon_url=entry.user.avatar.url)

        emb.add_field(name='Ein Channel wurde gelöscht:',
                      value=f'`{channel.name}`')

        log_channel = await self.bot.fetch_channel(1100879059480739932)
        await log_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        emb = Embed(color=0x3498db,
                    title="Es wurde eine Änderung am Server gemacht.")
        emb.timestamp = datetime.utcnow()
        emb.set_author(name=f'{role.guild.owner}',
                       icon_url=role.guild.owner.avatar.url)
        emb.add_field(name='Eine neue Rolle wurde erstellt:',
                      value=f'`{role.name}`')

        log_channel = await self.bot.fetch_channel(1100879059480739932)
        await log_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        emb = Embed(color=0x3498db,
                    title="Es wurde eine Änderung am Server gemacht.")
        emb.timestamp = datetime.utcnow()

        async for entry in role.guild.audit_logs(action=discord.AuditLogAction.role_delete, limit=1):
            target_role = entry.target
            if target_role.id == role.id:
                emb.set_author(name=f'{entry.user}',
                               icon_url=entry.user.avatar.url)

        emb.add_field(name='Eine Rolle wurde gelöscht:',
                      value=f'`{role.name}`')

        log_channel = await self.bot.fetch_channel(1100879059480739932)
        await log_channel.send(embed=emb)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        pass




def setup(client):
    client.add_cog(Server_Events_Logger(client))
