#import schedule

#from loops.birthday_congratulate import birthday_congratulate
from loops.update_stats_channels import update_stats_channels


async def loops(client):
    #900 Second
    client.loop.create_task(update_stats_channels(client, 900))

    #client.loop.create_task(birthday_congratulate(client, 10))
