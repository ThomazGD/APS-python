from datetime import datetime
from app import db

class UserMetrics(db.Model):
    __tablename__ = 'user_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Pontuações por categoria
    water_score = db.Column(db.Float, default=0.0)
    energy_score = db.Column(db.Float, default=0.0)
    mobility_score = db.Column(db.Float, default=0.0)
    food_score = db.Column(db.Float, default=0.0)
    waste_score = db.Column(db.Float, default=0.0)
    wellbeing_score = db.Column(db.Float, default=0.0)
    
    # Pontuação total
    total_score = db.Column(db.Float, default=0.0)
    
    # Nível do usuário
    level = db.Column(db.Integer, default=1)
    
    # Data da última atualização
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    def update_scores(self):
        # Atualiza a pontuação total baseada nas pontuações individuais
        self.total_score = (
            self.water_score +
            self.energy_score +
            self.mobility_score +
            self.food_score +
            self.waste_score +
            self.wellbeing_score
        )
        
        # Atualiza o nível com base na pontuação total
        self.level = min(100, max(1, int(self.total_score // 100) + 1))
        
        self.last_updated = datetime.utcnow()
        
    def __repr__(self):
        return f'<UserMetrics for user {self.user_id}>'

class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    activity_type = db.Column(db.String(50))  # Ex: 'water_saved', 'energy_saved', etc.
    description = db.Column(db.String(200))
    points_earned = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserActivity {self.activity_type} - {self.points_earned} points>'
