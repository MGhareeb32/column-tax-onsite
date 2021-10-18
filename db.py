import sqlite3
import json

def init_db(app):
    con = sqlite3.connect('user_info.db')
    print('Database starting...')
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cur.fetchall()
    if ('user_info',) not in table_names:
        cur.execute('''
        CREATE TABLE user_info
        (id TEXT PRIMARY KEY, info_json TEXT)
        ''')
        update_user('user_1', {})
        update_user('user_2', {})
        update_user('user_3', {})
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = cur.fetchall()
    print(f'Tables {table_names}.')
    print('TABLE user_info')
    cur.execute(f'SELECT * FROM user_info;')
    for row in cur.fetchall():
        print(row)


def get_user_data(user_id):
    con = sqlite3.connect('user_info.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM user_info WHERE id = \'{user_id}\'')
    user_row = cur.fetchone()
    if user_row is not None:
        return json.loads(user_row[1])
    else:
        return {}


def update_user(user_id, user_data_json):
    con = sqlite3.connect('user_info.db')
    cur = con.cursor()
    sql = f'''
    INSERT OR REPLACE INTO user_info(id, info_json) VALUES
    (?, ?)
    '''
    cur.execute(sql, (user_id, json.dumps(user_data_json)))
    con.commit()
