from flask import render_template, redirect, request, flash, jsonify
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

import datetime
import json

from app import app, db
from app.models import *


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')
    
    
@app.route('/bots', methods=['GET', 'POST'])
@login_required
def bots():
    bots = Bot.query.all()
    
    return render_template('bots.html', bots=bots)


@app.route('/bot/<int:id>', methods=['GET', 'POST'])
@login_required
def bot(id):
    bot = Bot.query.filter_by(id=id).first()
    data = Data.query.filter_by(token=bot.token).order_by(Data.timestamp.desc()).all()

    formatted_data = [{'timestamp': d.timestamp, 'members': json.loads(d.data)['members'], 'active_members': json.loads(d.data)['active_members']} for d in data]
    formatted_data.reverse()
    
    last_data = json.loads(data[-1].data)
    return render_template('bot.html', bot=bot, last_data=last_data, data=formatted_data)


@app.route('/bot/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def bot_edit(id):
    if request.method == 'POST':
        name = request.form['name']
        token = request.form['token']
        
        bot = Bot.query.filter_by(id=id).first()
        old_token =  bot.token
        
        bot.name = name
        bot.token = token
        
        data = Data.query.filter_by(token=old_token).all()
        for d in data:
            d.token = token
            
        db.session.commit()
        return redirect(f'/bot/{id}')
    else:
        bot = Bot.query.filter_by(id=id).first()
        return render_template('bot_edit.html', bot=bot)



@app.route('/bot/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def bot_delete(id):
    bot = Bot.query.filter_by(id=id).first()
    db.session.delete(bot)
    data = Data.query.filter_by(token=bot.token).all()
    for d in data:
        db.session.delete(d)
    db.session.commit()
    return redirect('/bots')


@app.route('/bots/new_bot', methods=['GET', 'POST'])
@login_required
def new_bot():  
    if request.method == 'POST':
        name = request.form['name']
        token = request.form['token']

        bot = Bot(name=name, token=token)
        
        try:
            db.session.add(bot)
            db.session.commit()
            flash("Бот успешно добавлен")
            return redirect('/bots')
        except:
            flash("При добавление бота произошла ошибка")
            return redirect('/bots/new_bot')
    else:
        return render_template('register_bot.html')
    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            
            next_page = request.args.get('next')
            flash('Вы успешно вошли')
            return redirect(next_page or '/')
        else:
            flash('Неверные логин или пароль')
            return redirect('/login')
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        if len(request.form['login']) > 4 and len(request.form['password']) > 4 and request.form['password']:
            hash = generate_password_hash(request.form['password'])
            new_user = User(login=request.form['login'], password=hash) # type: ignore
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Успешная регистрация")
                login_user(new_user, remember=True)
                return redirect('/')
            except:
                flash("При регистрации произошла ошибка")
            
        else:
            flash("Неверные поля")
            
    else:
        return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из системы")
    return redirect('/')





# -----API----- #
@app.route('/api/generate_token', methods=['GET'])
def return_token():
    token = generate_token()
    return jsonify({'token': token})



@app.route('/api/get_info', methods=['POST'])
def get_info():
    token = request.headers.get('token')
    
    data = request.json
    data = json.dumps(data)
    timestamp = datetime.datetime.now()
    
    new_data = Data(token=token, data=data, timestamp=timestamp)
    
    db.session.add(new_data)
    db.session.commit()
    
    return {
        "status": "OK"
    }
    
