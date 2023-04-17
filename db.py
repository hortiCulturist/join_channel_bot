import sqlite3 as sqlt

db_name = 'user_database.db'


def start_db():
    base = sqlt.connect(db_name)
    base.execute('CREATE TABLE IF NOT EXISTS "User" ("id"	INTEGER NOT NULL UNIQUE,'
                 '"user_id"     INTEGER,'
                 '"channel_id"  INTEGER,'
                 'PRIMARY KEY("id" AUTOINCREMENT))')
    base.execute('CREATE TABLE IF NOT EXISTS "Channel" ("id"	INTEGER NOT NULL UNIQUE,'
                 '"channel_id"     INTEGER,'
                 '"channel_title"  BLOB,'
                 'PRIMARY KEY("id" AUTOINCREMENT))')
    base.execute('CREATE TABLE IF NOT EXISTS "Message" ("id"	INTEGER NOT NULL UNIQUE,'
                 '"title"       BLOB,'
                 '"chat_id"     INTEGER,'
                 '"message_id"  INTEGER,'
                 'PRIMARY KEY("id" AUTOINCREMENT))')
    base.execute('CREATE TABLE IF NOT EXISTS "User_ivent" ("id"	INTEGER NOT NULL UNIQUE,'
                 '"channel_id"      INTEGER,'
                 '"user_id"         INTEGER,'
                 'PRIMARY KEY("id" AUTOINCREMENT))')
    base.execute('CREATE TABLE IF NOT EXISTS "Welcome_post" ('
                 '"chat_id" INTEGER,'
                 '"message_id" INTEGER,'
                 'PRIMARY KEY("chat_id", "message_id"))')
    base.execute('CREATE TABLE IF NOT EXISTS "Button" ("id"	INTEGER NOT NULL UNIQUE,'
                 '"button_text"      BLOB,'
                 'PRIMARY KEY("id" AUTOINCREMENT))')
    base.commit()


def add_button(text):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT id FROM Button').fetchall()
        if len(data) >= 4:
            return False
        else:
            cur.execute('INSERT INTO Button VALUES (null, ?)', (text,))
            return True


def get_button():
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT * FROM Button').fetchall()
        if data is None:
            return False
        else:
            return data


def handler_button_words():
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT * FROM Button').fetchall()
        button_list = list()
        for button in data:
            button_list.append(button[1])
        return button_list


def update_button_text(button_id, button_text):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        cur.execute('UPDATE Button SET button_text = ? WHERE id = ?', (button_text, button_id))


def edit_welcome_post(chat_id, message_id):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM Welcome_post;')
        cur.execute('INSERT INTO Welcome_post VALUES (?, ?)', (chat_id, message_id))


def get_welcome_post():
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT * FROM Welcome_post').fetchall()
        return data


def add_await_user(channel_id, user_id):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT * FROM User_ivent WHERE channel_id = ? AND user_id = ?',
                           (channel_id, user_id)).fetchone()
        if data is None:
            cur.execute('INSERT INTO User_ivent VALUES (null, ?, ?)', (channel_id, user_id))
            return True
        else:
            return False


def inpt(user_id):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT * FROM User_ivent WHERE user_id = ?', (user_id,)).fetchone()
        if data is None:
            return False
        else:
            return data


def clear(user_id):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM User_ivent WHERE user_id = ?', (user_id,))


def add_channel(channel_id, channel_title):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT * FROM Channel where channel_id = ?', (channel_id,)).fetchone()
        if data is None:
            cur.execute('INSERT INTO Channel VALUES (null, ?, ?)', (channel_id, channel_title))
            return True
        else:
            return False


def add_user(user_id, channel_id):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT * FROM User WHERE user_id = ? AND channel_id = ?', (user_id, channel_id)).fetchone()
        if data is None:
            cur.execute('INSERT INTO User VALUES (null, ?, ?)', (user_id, channel_id))
            return True
        else:
            return False


def all_user():
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        users = cur.execute('SELECT user_id from User').fetchall()
    return users


def add_message(title, chat_id, message_id):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO Message VALUES (null, ?, ?, ?)', (title, chat_id, message_id))


def get_message():
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT * FROM Message').fetchall()
        if data is None:
            return False
        else:
            return data


def get_channel():
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT * FROM Channel').fetchall()
        if data is None:
            return False
        else:
            return data


def template_selection(ID):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT * FROM Message WHERE id = ?', (ID,)).fetchall()
        if data is None:
            return False
        else:
            return data


def get_users_in_channel_id(ID):
    with sqlt.connect(db_name) as conn:
        cur = conn.cursor()
        data = cur.execute('SELECT channel_id FROM Channel WHERE id = ?', (ID,)).fetchone()
        if data is None:
            return False
        else:
            info = cur.execute('SELECT user_id FROM User WHERE channel_id = ?', (data[0],)).fetchall()
            return info
