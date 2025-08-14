import sqlite3
import os
import time
import random
import string

def tn(text: str):
    named_tuple = time.localtime()  # получаем struct_time
    time_string = time.strftime("%H:%M:%S", named_tuple)
    return print(fr'[{time_string}] {text}')


if os.name=='nt':
    path=os.path.dirname(os.path.abspath(__file__))
    DB_link=fr'{path}\storage\users.db'
    DB_link_rooms = fr'{path}\storage\rooms.db'
elif os.name=='posix':
    path = os.path.dirname(os.path.abspath(__file__))
    DB_link=fr'{path}/storage/users.db'
    DB_link_rooms = fr'{path}/storage/rooms.db'

def write_new(user, password):
    """Регистрация нового пользователя"""
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
    """Проверка логина и пароля """
    conn = sqlite3.connect(DB_link)
    cursor = conn.cursor()
    cursor.execute('''SELECT 1 FROM users WHERE login = ? AND password = ?''', (login, password))
    return cursor.fetchone() is not None  # True если пользователь найден, иначе False
    conn.commit()
    conn.close()

def new_post(author:str,theme:str, text:str):
    """Создание нового поста"""
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

def generate_id_room(length=random.randint(5,7)):
    """Создаем id комнаты"""
    # Собираем все возможные символы: буквы (верхний и нижний регистр) + цифры
    characters = string.ascii_letters + string.digits
    # Генерируем случайную строку заданной длины
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def create_room(admin, name_room):
    """Создаем комнату (чат)"""
    conn = sqlite3.connect(DB_link_rooms)
    cursor = conn.cursor()

    rooms=[]
    named_tuple = time.localtime()  # получаем struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    id_room=generate_id_room()
    parametes = (str(id_room), str(admin), str(name_room), f'{admin}', str(time_string), str(time_string))  # что записываем

    cursor.execute('''CREATE TABLE IF NOT EXISTS rooms
                                  (id TEXT,admin TEXT, name_room TEXT, members TEXT,time_create TEXT, time_last TEXT)''')
    cursor.execute("INSERT INTO rooms (id, admin, name_room, members ,time_create, time_last) VALUES (?, ?, ?, ?, ?, ?)",
                   parametes)

    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {id_room}
                                  (author TEXT, text TEXT, time TEXT)''')
    parametes_room = (str(admin), f"Я создал комнату !", str(time_string))  # что записываем
    cursor.execute(f"INSERT INTO {id_room} (author, text, time) VALUES (?, ?, ?)", parametes_room)

    conn.commit()
    conn.close()

def get_all_rooms():
    """Получаем все id и имена комнат (чатов) из таблицы rooms"""
    conn = sqlite3.connect(DB_link_rooms)
    cursor = conn.cursor()

    #получаем список всех id, name_room из таблицы rooms
    cursor.execute("SELECT id, name_room FROM rooms")
    rooms = cursor.fetchall()  #получаем список который выглядит как: [(id1, name1), (id2, name2), ...]

    conn.close()
    return rooms

def get_all_message_from_room(id_room):
    """Берет все сообщения с комнаты"""
    conn = sqlite3.connect(DB_link_rooms)
    cursor = conn.cursor()

    cursor.execute(f"SELECT author, text, time FROM {id_room}")
    parametres = cursor.fetchall()  # получаем список который выглядит как: [(author0, text0, time0), (id1, name1, time1), ...]

    conn.close()
    return parametres

def new_message_room(id_room ,author, text):
    """Новое сообщение в комнате"""
    conn = sqlite3.connect(DB_link_rooms)
    cursor = conn.cursor()
    named_tuple = time.localtime()  # получаем struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    parametes = (str(author), str(text), str(time_string))  # что записываем
    cursor.execute(f"INSERT INTO {id_room} (author, text, time) VALUES (?, ?, ?)", parametes)
    conn.commit()
    conn.close()

def reverse(list):
    """разворот порядка элементов списка"""
    return list[::-1]