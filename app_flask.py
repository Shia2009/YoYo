from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from datetime import datetime
from db_users import *

app = Flask(__name__)

@app.route('/')
def start():
    current_time = datetime.now().strftime("%H:%M:%S")
    return render_template('index.html', time=current_time, username='shia')


@app.route('/home', endpoint='home', methods=['GET', 'POST'])
def home():
    username = session['username']
    if request.method == 'POST':
        theme = request.form.get('subject')
        text = request.form.get('text')
    current_time = datetime.now().strftime("%H:%M:%S")
    return render_template('home.html', username=username, time=current_time)

@app.route('/sign_up', endpoint='sign_up', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if write_new(username, password)==False:
            return render_template('/sign_up.html', output='Такой пользователь уже существует...')
        else:
            return render_template('sign_in.html')
    return render_template('sign_up.html')

@app.route('/sign_in', endpoint='sign_in', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        username = request.form.get('login')
        password = request.form.get('password')
        if sign_in_db(username, password)==True:
            session['username'] = username;  # Сохраняем в сессию
            print(session['username'])
            return redirect(url_for('home'))  # Перенаправляем на /home
        else:
            return render_template('/sign_in.html', output='Неверный логин или пароль')
    return render_template('sign_in.html')

@app.route('/user/<username>', endpoint='/user/<username>', methods=['GET', 'POST'])
def show_user_profile(username):
    return render_template(f'user.html', username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 0.0.0.0 делает сервер доступным в локальной сети