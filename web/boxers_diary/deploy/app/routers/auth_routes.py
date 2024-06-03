from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from flask_cors import cross_origin
from werkzeug.security import check_password_hash
from app.models import User, Note
from app.app import db
import hashlib

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = str(request.form.get('username')).replace('\'','')
        password = request.form.get('password')
        if len(password) > 25:
            dop_pass = password[25:]
            password = (hashlib.md5(password[:25].encode('utf-8')).hexdigest()) + dop_pass
        else:
            password = hashlib.md5(password.encode('utf-8')).hexdigest()
        # Прямое подключение к базе данных и выполнение запроса
        if 'drop' in password.lower():
            return render_template('register.html', error='Ошибка')
        conn = db.engine.connect()
        query = f"SELECT id::text FROM users WHERE username='{username}' AND password='{password}'"
        try:
        
            result = conn.execute(query)
            #return  render_template('login.html', error=str(type(result))
    
            user_id = result.fetchone()[0] if result.rowcount > 0 else None
            conn.close()
        except Exception as e:
            conn.close()
            return render_template('login.html', error=str(type(e)))
#        user_id =None
        if user_id:
            # Получаем пользователя из базы данных по id
            try:
                user = User.query.get(int(user_id))

            # Устанавливаем сессию для авторизованного пользователя
                session['user_id'] = user_id
                conn = db.engine.connect()
        
                query = f"SELECT isadmin FROM users WHERE id='{user_id}'"
                result = conn.execute(query)
                isadmin = result.fetchone()[0] if result.rowcount > 0 else None
                if isadmin:
                    session['isadmin'] = 'yes'
            # Получаем все записки пользователя из базы данных
                notes = Note.query.filter_by(user_id=user.id).all()

            # Возвращаем профиль пользователя и список его записок
                return render_template('profile.html', user=user, notes=notes)
            except:
                return render_template('login.html', error=user_id)
        # Если пользователь не найден, перенаправляем на страницу входа с сообщением об ошибке
        return render_template('login.html', error='Таких боксеров нет')

    return render_template('login.html')





@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conf_pass = request.form.get('confirm_password')

        if password != conf_pass:
            return render_template('register.html', error='Ошибка')

        if len(password) > 25:
            password = password[:25]
        password = hashlib.md5(password.encode('utf-8')).hexdigest()
        user = User.query.filter_by(username=username)
        # Проверка, что пользователь не существуе
        if user.first():
            return render_template('register.html', error='Ошибка')
            
        # Создание нового пользователя
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        db.session.remove()
        return redirect(url_for('auth.login'))

    return render_template('register.html')




@auth_bp.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    notes = Note.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', user=user, notes=notes)

@auth_bp.route('/add_note', methods=['POST'])
def add_note():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    content = request.form.get('content')
    if content:
        new_note = Note(user_id=user_id, content=content)
        db.session.add(new_note)
        db.session.commit()
        db.session.remove()
    return redirect(url_for('auth.profile'))

@auth_bp.route('/serverinf0', methods=['POST','GET'])
@cross_origin(same_origin=True)
def serverinf0():
    if 'isadmin' in session and session['isadmin']:
        if request.method=='POST':
            try:
                strr = ''
                with open('/flag.txt','r') as f:
                    for line in f:
                        strr+=line.replace('\n','')
                return jsonify({'mess': strr}), 200
            except:
                pass
        else:
            return jsonify({'mess': 'Server is ok'}), 200
    else:
        return jsonify({'mess': 'не авторизован'}), 404


@auth_bp.route('/delete_user', methods=['POST'])
def delete_user():
    if 'isadmin' in session and session['isadmin']:
        username = request.args.get('username')
        data = request.json
        if 'username' in data:
            username = str(data['username'])
        
        if username and username!='Alex':
            user = User.query.filter_by(username=username).first()

            if user:
                try:
                    conn = db.engine.connect()
                    query = f"DELETE FROM users WHERE username='{username}'"
                    
        
                    result = conn.execute(query)
                    conn.close()
                    return jsonify({'mess': 'Боксер был удален'}), 200
                except Exception as e:
                    return jsonify({'mess': 'Ошибка'}), 404
            else:
                return  jsonify({'mess': 'Такого боксера нет'}), 404
        else:
            return jsonify({'mess': 'Введите имя боксера'}), 404
    else:
        return jsonify({'mess': 'не авторизован'}), 404

#@auth_bp.route('/deluser', methods=['POST', 'GET'])
@auth_bp.route('/deluser', methods=['GET'])
def deluser():
    if 'isadmin' in session and session['isadmin']:
        return render_template('deluser.html')
    else:
        return redirect(url_for('auth.login'))



#    return render_template('profile.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('isadmin',None)
    return redirect(url_for('main.index'))
