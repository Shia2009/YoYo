from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import jsonify
from difflib import get_close_matches
from datetime import datetime
from db_users import *
from config import *

app = Flask(__name__)
app.secret_key = secret_key

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home', endpoint='home', methods=['GET', 'POST'])
def home():
    username = session.get('username')  # Получаем из сессии
    if request.method == 'POST':
        theme = request.form.get('subject')
        text = request.form.get('text')

        named_tuple = time.localtime()
        time_string = time.strftime("%H:%M:%S", named_tuple)

        new_post(username, theme, text)
    current_time = datetime.now().strftime("%H:%M:%S")
    return render_template('home.html', username=username, time=current_time)

@app.route('/sign_up', endpoint='sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if write_new(username, password)==False:
            return render_template('/sign_up.html', output='Такой пользователь уже существует...')
        else:
            return render_template('sign_in.html')
    return render_template('sign_up.html')

@app.route('/sign_in', endpoint='sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method=='POST':
        username = request.form.get('login')
        password = request.form.get('password')
        if sign_in_db(username, password)==True:
            session['username'] = username  # Сохраняем в сессию
            return redirect(url_for('home'))
        else:
            return render_template('sign_in.html', output='Неверный пароль или логин')
    return render_template('sign_in.html')

@app.route('/user/<username>', endpoint='/user/<username>', methods=['GET', 'POST'])
def show_user_profile(username):
    if get_user_notes(username)!=False:
        notes=get_user_notes(username)
    else:
        return 'Ошибка... (63 line /user)'
    return render_template(f'user.html', username=username, notes=notes)


@app.route('/search_user', endpoint='search_user', methods=['GET', 'POST'])
def search():
    if request.method=='POST':
        user = request.form.get('username')
        users=get_all_usernames()
        matches = get_close_matches(user, users, n=5, cutoff=0.4)#схожие юзеры доделать
        if user in users:
            exact_match=users[users.index(user)]
            return render_template(f'search_user.html',
                                   exact_match=exact_match)
    return render_template(f'search_user.html')

@app.route('/rooms', endpoint='rooms', methods=['GET', 'POST'])
def rooms_():
    username = session.get('username')  # Получаем из сессии
    rooms=get_all_rooms(username)
    return render_template(f'rooms.html',
                           username=username,
                           rooms=rooms)

@app.route('/create_room', endpoint='create_room', methods=['GET', 'POST'])
def create_room_():
    username = session.get('username')  # Получаем из сессии
    if request.method=='POST':
        name_room = request.form.get('name_room')
        create_room(username, name_room)
        return redirect(url_for('rooms'))
    return render_template(f'create_room.html', username=username)

@app.route('/room/<id>', endpoint='/room/<id>', methods=['GET', 'POST'])
def room_main(id):
    username = session.get('username')  # Получаем из сессии
    session['room_id']=id
    if request.method=='POST':
        message = request.form.get('message')
        if message not in ['', ' ', '  ', None]:
            new_message_room(id, username, message)
    messages=reverse_list(get_all_message_from_room(id))
    rooms=get_all_rooms(username)
    for room in rooms:
        if room[0]==id:
            name_room=room[1]
            session['name_room']=name_room
            break
    return render_template(f'room.html',id_room=id, name_room=name_room, messages=messages)

@app.route('/room/add_user/<id_room>', endpoint='/room/add_user/<id_room>', methods=['GET', 'POST'])
def add_user_to_room(id_room):
    user = request.form.get('username')
    name_room = session.get('name_room')
    if request.method == 'POST':
        users = get_all_usernames()
        if user in users:
            exact_match = users[users.index(user)]
            session['username_friend']=exact_match
            return render_template(f'add_user_to_room.html',
                                   name_room=name_room,
                                   exact_match=exact_match,
                                   id_room=id_room)
    return render_template(f'add_user_to_room.html', name_room=name_room)

@app.route('/room/add_user/confim/<username>_to_<id_room>', endpoint='/room/add_user/confim/<username>_to_<id_room>', methods=['GET', 'POST'])
def add_user_to_room_confim(username ,id_room):
    button_value = request.form.get('button')
    user_friend = session.get('username_friend')
    user = session.get('username')
    name_room = session.get('name_room')
    if button_value == 'add-user':
        add_new_member_to_room(id_room, user_friend)
        return redirect(url_for(f'rooms'))
    if get_user_notes(username)!=False:
        notes=get_user_notes(username)
    return render_template(f'confim_add_user_to_room.html',
                           name_room=name_room,
                           id_room=id_room,
                           username_friend=user_friend,
                           notes=notes)

@app.route('/room/remove_user/<id_room>', endpoint='/room/remove_user/<id_room>', methods=['GET', 'POST'])
def remove_user_from_room(id_room):
    user = request.form.get('username')
    name_room = session.get('name_room')
    if request.method == 'POST':
        users = get_all_usernames()
        if user in users:
            exact_match = users[users.index(user)]
            session['username_friend']=exact_match
            return render_template(f'remove_user_from_room.html',
                                   name_room=name_room,
                                   exact_match=exact_match,
                                   id_room=id_room)
    return render_template(f'remove_user_from_room.html', name_room=name_room)

@app.route('/room/remove_user/confim/<username>_from_<id_room>', endpoint='/room/remove_user/confim/<username>_from_<id_room>', methods=['GET', 'POST'])
def add_user_to_room_confim(username ,id_room):
    button_value = request.form.get('button')
    user_friend = session.get('username_friend')
    user = session.get('username')
    name_room = session.get('name_room')
    if button_value == 'remove-user':
        remove_member_from_room(id_room, user_friend)
        return redirect(url_for(f'rooms'))
        print('REMOVE'*8)
    if get_user_notes(username)!=False:
        notes=get_user_notes(username)
    return render_template(f'confim_delete_user_from_room.html',
                           name_room=name_room,
                           id_room=id_room,
                           username_friend=user_friend,
                           notes=notes)

@app.route('/room/add_room/', endpoint='/room/add_room/', methods=['GET', 'POST'])
def add_room_():
    username=session.get('username')
    if request.method == 'POST':
        room = request.form.get('username')
        rooms = get_all_rooms_id()
        rooms_name=get_all_rooms_name()
        if room in rooms:
            exact_match = rooms[rooms.index(room)]
            name_room=rooms_name[rooms.index(room)]
            session['name_room']=name_room
            return render_template(f'add_room.html',
                                   name_room=name_room,
                                   exact_match=exact_match,
                                   id_room=room,
                                   username=username)
    return render_template(f'add_room.html')

@app.route('/room/add_room/confim/<username>_to_<id_room>', methods=['GET', 'POST'])
def add_user_to_room_confim(username ,id_room):
    button_value = request.form.get('button')
    messages=get_all_message_from_room(id_room)
    name_room=session.get('name_room')
    if button_value=='join-room':
        print('123123123'*10)
        add_new_member_to_room(id_room, username)
        return redirect(url_for(f'rooms'))
    return render_template(f'confim_add_room.html',
                           username=username,
                           name_room=name_room,
                           messages=messages)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 0.0.0.0 делает сервер доступным в локальной сети