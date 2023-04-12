import discord

from static import SQL, db


async def leave(member, client):
    SQL.execute(f'UPDATE users SET xp = 0 WHERE user_id = {member.id};')
    db.commit()