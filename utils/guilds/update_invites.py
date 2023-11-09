import static


async def update_invites(client):
    guild = (await client.fetch_channel(static.channels_id['all'])).guild # Duschpalast Server
    static.invites = await guild.invites()