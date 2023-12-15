import discord

from static import SQL, db, cmd_xp


async def cmd_reward(ctx: discord.ApplicationContext):
    user: discord.User = ctx.author

    SQL.execute(f'UPDATE users SET xp = xp + {cmd_xp} WHERE user_id = {user.id};')
    db.commit()
