import asyncio
from datetime import date

from static import SQL


async def birthday_congratulate(client, time):
    while True:
        SQL.execute('SELECT user_id, birthday FROM users WHERE birthday IS NOT NULL')
        res = SQL.fetchall()
        for x in res:
            print(x)
            if date.today() == x[1]:
                print(f"{x} birthday")

        await asyncio.sleep(time)