from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from app import db
from app.models.user import User
from app.models.metrics import UserMetrics
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Usuário ou senha inválidos', 'error')
            return redirect(url_for('auth.login'))
            
        login_user(user)
        next_page = request.args.get('next')
        
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
            
        return redirect(next_page)
        
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validações
        if password != confirm_password:
            flash('As senhas não conferem', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(username=username).first() is not None:
            flash('Nome de usuário já está em uso', 'error')
            return redirect(url_for('auth.register'))
            
        if User.query.filter_by(email=email).first() is not None:
            flash('E-mail já está em uso', 'error')
            return redirect(url_for('auth.register'))
            
        # Criar novo usuário
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Criar métricas iniciais para o usuário
        metrics = UserMetrics(user=user)
        
        db.session.add(user)
        db.session.add(metrics)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
