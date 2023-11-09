import discord

from static import SQL, db


async def first_write_check(user: discord.Member):
    SQL.execute(f'select user_id from users where user_id="{user.id}"')
    result_userid = SQL.fetchone()

    if result_userid is None:
        SQL.execute('insert into users(user_id, user_name) values(?,?)', (user.id, str(user),))
        db.commit()