import sqlite3
import os
import time

def tn(text: str):
    named_tuple = time.localtime()  # получаем struct_time
    time_string = time.strftime("%H:%M:%S", named_tuple)
    return print(fr'[{time_string}] {text}')


if os.name=='nt':
    path=os.path.dirname(os.path.abspath(__file__))
    DB_link=fr'{path}\storage\users.db'
elif os.name=='posix':
    path = os.path.dirname(os.path.abspath(__file__))
    DB_link=fr'{path}/storage/users.db'

def write_new(user, password):
    conn = sqlite3.connect(DB_link)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY, login TEXT, password TEXT, time TEXT)''')

    named_tuple = time.localtime()  # получаем struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    parametes = (str(user), str(password), str(time_string))#что записываем
    # Проверяем существование пользователя
    cursor.execute("SELECT login FROM users WHERE login = ?", (user,))
    if cursor.fetchone():
        return False
    else:
        cursor.execute("INSERT INTO users (login, password, time) VALUES (?, ?, ?)", parametes)
        tn('Новый пользователь зарегистрирован.')
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {user}
                                  (id INTEGER PRIMARY KEY, subject TEXT, notes TEXT, time TEXT)''')
    conn.commit()
    conn.close()
    tn('Новый пользователь зарегистрирован.')


def sign_in_db(login: str, password: str) -> bool:
    conn = sqlite3.connect(DB_link)
    cursor = conn.cursor()
    cursor.execute('''SELECT 1 FROM users WHERE login = ? AND password = ?''', (login, password))
    return cursor.fetchone() is not None  # True если пользователь найден, иначе False
    conn.commit()
    conn.close()

def new_post(author:str,theme:str, text:str):
    conn = sqlite3.connect(DB_link)
    cursor = conn.cursor()
    named_tuple = time.localtime()  # получаем struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    parametes = (str(theme), str(text), str(time_string))#что записываем
    cursor.execute(f"INSERT INTO {author} (subject, notes, time) VALUES (?, ?, ?)", parametes)
    conn.commit()
    conn.close()

def get_user_notes(username):
    """Получаем все записи пользователя из БД"""
    conn = sqlite3.connect(DB_link)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT subject, notes, time FROM {username} ORDER BY id DESC")
        notes = cursor.fetchall()
    except:
        return False
    conn.close()
    return notes

def get_all_usernames():
    """Получаем все имена пользователей из таблицы users"""
    conn = sqlite3.connect(DB_link)
    cursor = conn.cursor()

    # Получаем список всех логинов из таблицы users
    cursor.execute("SELECT login FROM users")
    usernames = [row[0] for row in cursor.fetchall()]

    conn.close()
    return usernames