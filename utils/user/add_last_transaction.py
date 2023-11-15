from ast import literal_eval
import discord

from static import SQL, db


async def add_last_transaction(user: discord.Member, add_remove, reason, ammount):
    SQL.execute(f'SELECT transactions FROM users WHERE user_id = {user.id}')
    transactions = SQL.fetchone()[0]
    if transactions:
        transactions = literal_eval(transactions)
    else:
        transactions = []

    transac = [add_remove, reason, ammount]
    transactions.insert(0, transac)

    if len(transactions) > 3:
        transactions.pop()

    SQL.execute(f'UPDATE users SET transactions = {transactions} WHERE user_id = {user.id}')
    db.commit()
