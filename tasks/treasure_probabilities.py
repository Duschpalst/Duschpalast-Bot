from static import SQL, db


async def calc_treasure_probabilities():
    SQL.execute('SELECT user_id, msg_count FROM users')
    res = SQL.fetchall()

    all_count = 0

    for i in res:
        all_count += i[1]

    for i in res:
        if i[1] == 0:
            prob = 0
        else:
            prob = 100 // all_count * i[1]

        prob = min(prob, 30)

        print(f"user: {i[0]}  -  prob: {prob}")

        SQL.execute(f'UPDATE users SET treasure_prob = {prob} WHERE user_id = {i[0]}')
        SQL.execute(f'UPDATE users SET msg_count = 0 WHERE user_id = {i[0]}')

    db.commit()
