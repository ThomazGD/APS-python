from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from app.models.metrics import UserMetrics, UserActivity
from datetime import datetime, timedelta
from . import main

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Obter métricas do usuário
    metrics = UserMetrics.query.filter_by(user_id=current_user.id).first()
    
    # Se o usuário não tiver métricas, criar um registro vazio
    if not metrics:
        metrics = UserMetrics(user_id=current_user.id)
        db.session.add(metrics)
        db.session.commit()
    
    # Obter atividades recentes
    recent_activities = UserActivity.query.filter_by(
        user_id=current_user.id
    ).order_by(UserActivity.created_at.desc()).limit(5).all()
    
    # Calcular estatísticas
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    
    weekly_activities = UserActivity.query.filter(
        UserActivity.user_id == current_user.id,
        UserActivity.created_at >= week_ago
    ).all()
    
    weekly_points = sum(act.points_earned for act in weekly_activities)
    
    return render_template('dashboard.html', 
                         metrics=metrics,
                         recent_activities=recent_activities,
                         weekly_points=weekly_points)

@main.route('/log-activity', methods=['POST'])
@login_required
def log_activity():
    data = request.get_json()
    
    activity_type = data.get('activity_type')
    description = data.get('description')
    points = float(data.get('points', 0))
    
    if not all([activity_type, description]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Criar nova atividade
    activity = UserActivity(
        user_id=current_user.id,
        activity_type=activity_type,
        description=description,
        points_earned=points
    )
    
    # Atualizar métricas do usuário
    metrics = UserMetrics.query.filter_by(user_id=current_user.id).first()
    if not metrics:
        metrics = UserMetrics(user_id=current_user.id)
        db.session.add(metrics)
    
    # Atualizar pontuação baseada no tipo de atividade
    if activity_type == 'water_saved':
        metrics.water_score += points
    elif activity_type == 'energy_saved':
        metrics.energy_score += points
    elif activity_type == 'sustainable_transport':
        metrics.mobility_score += points
    elif activity_type == 'sustainable_food':
        metrics.food_score += points
    elif activity_type == 'waste_reduction':
        metrics.waste_score += points
    elif activity_type in ['physical_activity', 'screen_time_reduction', 'sleep_quality']:
        metrics.wellbeing_score += points
    
    # Atualizar pontuação total e nível
    metrics.update_scores()
    
    # Salvar alterações
    db.session.add(activity)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'total_score': metrics.total_score,
        'level': metrics.level
    })

@main.route('/leaderboard')
@login_required
def leaderboard():
    # Obter os 10 melhores usuários por pontuação total
    top_users = db.session.query(
        User.username,
        UserMetrics.total_score,
        UserMetrics.level
    ).join(UserMetrics).order_by(
        UserMetrics.total_score.desc()
    ).limit(10).all()
    
    # Posição do usuário atual
    user_position = db.session.query(
        db.func.count(UserMetrics.id)
    ).filter(
        UserMetrics.total_score > (
            db.session.query(UserMetrics.total_score)
            .filter(UserMetrics.user_id == current_user.id)
            .scalar_subquery()
        )
    ).scalar() + 1
    
    return render_template('leaderboard.html', 
                         top_users=top_users,
                         user_position=user_position)
