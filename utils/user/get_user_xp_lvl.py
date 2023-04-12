import discord

from static import SQL, db


async def get_xp_lvl(user: discord.Member):
    SQL.execute(f'select user_id from users where user_id="{user.id}"')
    result_userid = SQL.fetchone()

    if result_userid is None:
        SQL.execute('insert into users(user_id, user_name) values(?,?)', (user.id, str(user),))
        db.commit()

    SQL.execute(f'SELECT xp FROM users WHERE user_id = {user.id};')
    xp = SQL.fetchone()[0]

    if xp == 0:
        lvl = xp // 150 + 1
    else:
        lvl = (xp - 1) // 150 + 1

    return xp, lvl