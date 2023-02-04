import asyncio


async def member_count(client, time):
    while True:
        all_channel = await client.fetch_channel(1055141450762952774)
        member_channel = await client.fetch_channel(1055141454730776686)
        bots_channel = await client.fetch_channel(1055141458774065212)
        m_count = 0
        b_count = 0
        for usr in member_channel.guild.members:
            if not usr.bot:
                m_count += 1
            elif usr.bot:
                b_count += 1

        await all_channel.edit(name=f"Alle Mitglieder: {len(member_channel.guild.members)}")
        await member_channel.edit(name=f"Mitglieder: {m_count}")
        await bots_channel.edit(name=f"Bots: {b_count}")

        await asyncio.sleep(time)