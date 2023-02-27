#import schedule
import aiocron

#from tasks.birthday_congratulate import birthday_congratulate
from tasks.update_stats_channels import update_stats_channels
from tasks.treasure_probabilities import calc_treasure_probabilities


async def tasks(client):
    #900 Second
    client.loop.create_task(update_stats_channels(client, 900))

    #client.loop.create_task(birthday_congratulate(client, 10))


@aiocron.crontab('0 0 * * *')
async def every_day_tasks():
    await calc_treasure_probabilities()
