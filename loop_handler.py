import schedule

from loops.birthday_congratulate import birthday_congratulate
from loops.member_count import member_count


async def loops(client):
    #900 Second
    client.loop.create_task(member_count(client, 900))

    #client.loop.create_task(birthday_congratulate(client, 10))
