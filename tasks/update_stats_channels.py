import asyncio


async def update_stats_channels(client, time):
    while True:
        all_channel = await client.fetch_channel(1055141450762952774)
        member_channel = await client.fetch_channel(1055141454730776686)
        bots_channel = await client.fetch_channel(1055141458774065212)
        in_voice_channel = await client.fetch_channel(1071784772533223454)
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

        await asyncio.sleep(time)
