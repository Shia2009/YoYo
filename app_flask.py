from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from difflib import get_close_matches
from datetime import datetime
from db_users import *
from config import *

app = Flask(__name__)
app.secret_key = secret_key

@app.route('/')
def start():
    current_time = datetime.now().strftime("%H:%M:%S")
    return render_template('index.html', time=current_time, username='shia')


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


@app.route('/search_user', endpoint='/search_user', methods=['GET', 'POST'])
def search():
    if request.method=='POST':
        user = request.form.get('username')
        users=get_all_usernames()
        matches = get_close_matches(user, users, n=5, cutoff=0.4)#схожие юзеры
        if user in users:
            exact_match=users[users.index(user)]
            return render_template(f'search_user.html',
                                   exact_match=exact_match)
    return render_template(f'search_user.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 0.0.0.0 делает сервер доступным в локальной сети