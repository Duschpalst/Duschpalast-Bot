from static import SQL, db


def create_sql_tables():
    SQL.execute('CREATE TABLE IF NOT EXISTS color_picker('
	            'name TEXT NOT NULL UNIQUE,'
                'emoji TEXT,'
	            'role_id INTEGER NOT NULL UNIQUE);')

    SQL.execute('CREATE TABLE IF NOT EXISTS self_roles_gender('
                'name TEXT NOT NULL UNIQUE,'
                'role_id INTEGER NOT NULL UNIQUE);')

    SQL.execute('CREATE TABLE IF NOT EXISTS self_roles_age('
                'name TEXT NOT NULL UNIQUE,'
                'role_id INTEGER NOT NULL UNIQUE);')

    SQL.execute('CREATE TABLE IF NOT EXISTS self_roles_games('
                'name TEXT NOT NULL UNIQUE,'
                'emoji_name TEXT NOT NULL UNIQUE,'
                'role_id INTEGER NOT NULL UNIQUE);')

    SQL.execute('CREATE TABLE IF NOT EXISTS self_roles_programming('
                'name TEXT NOT NULL UNIQUE,'
                'emoji_name TEXT NOT NULL UNIQUE,'
                'role_id INTEGER NOT NULL UNIQUE);')

    SQL.execute('CREATE TABLE IF NOT EXISTS users('
                'user_id INTEGER NOT NULL UNIQUE,'
                'user_name TEXT NOT NULL,'
                'xp INTEGER DEFAULT 0,'
                'coin INTEGER DEFAULT 0,'
                'transactions TEXT,'
                'protocol TEXT,'
                'msg_count INTEGER DEFAULT 0,'
                'vc_time INTEGER DEFAULT 0,'
	            'daily TEXT);')

    db.commit()
