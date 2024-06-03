from flask import Flask,session, render_template,make_response, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from bs4 import BeautifulSoup
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:password@db:5432/mydatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
IMAGE_DIR = "static/images"


# Модель пользователя
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Создаем базу данных
with app.app_context():
    db.create_all()

# Создаем пользователя Admin с паролем qwerty123
    if not User.query.filter_by(username='GregorHirsh').first():
        admin_user = User(username='GregorHirsh', password='qwerty123')
        db.session.add(admin_user)
        db.session.commit()
# Маршрут для отображения и обработки логин формы
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
                
        user = User.query.filter_by(username=username).first()
        if user:
            if 'X-Image' in request.headers:
                image = request.headers.get('X-Image')
            else:
                image = 'cat.jpeg'
            password  = hashlib.md5(password.encode('utf-8')).hexdigest()
            pass_user = hashlib.md5(user.password.encode('utf-8')).hexdigest()
            check = password == pass_user 
            if check:
                flash('Вы успешно вошли', 'success')
                session['logged_in'] = True  # Устанавливаем флаг авторизации в сессии
                response = make_response(redirect(url_for('profile')))
                response.headers['X-Image'] = image  # Устанавливаем нужный заголовок
                return response
            else:
                flash(f'Неверные учетные данные', 'error')
#            return redirect(url_for('profile'))
        else:
            
            flash(f'Неверные учетные данные', 'error')
    return render_template('login.html')




# Пример защищенной страницы
@app.route('/profile')
def profile():
    if session.get('logged_in'):
#        return render_template('profile.html')
            # Читаем содержимое файла profile.html
        if 'X-file' in request.headers:
            x_file = request.headers.get('X-File')
            file_content = None
            if x_file:
                if len(x_file) > 4:
                    x_file = x_file[:4]
                try:
                    with open(x_file, 'r') as file:
                        file_content = file.read()
                except FileNotFoundError:
                    file_content = None
            else:
                pass
        else:
            file_content = None
        return render_template('profile.html', file_content=file_content)   


    else:
        flash('Пожалуйста, авторизуйтесь', 'error')
        return redirect(url_for('login'))


# Пример защищенной страницы
@app.route('/index')
def index():
    return "Это защищенная страница. Только для авторизованных юзеров"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

