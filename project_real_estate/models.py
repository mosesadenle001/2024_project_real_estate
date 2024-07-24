from datetime import datetime
from project_real_estate import db, login_manager
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask import current_app

#Initialize all database models
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    properties = db.relationship('Property', backref='owner', lazy=True)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)   #added for admin user

    def __repr__(self):
        return f"User('{self.username}', '{self.email}',{self.properties}"

    def get_reset_token(self, expires_sec=1700):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        token = s.dumps({'user_id': str(self.id)}).decode('utf-8')
        return token  # string

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"property('{self.title}', '{self.date_posted}', '{self.location}', '{self.price}', '{self.property_type}')"
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    property = db.relationship('Location', backref='properties', lazy=True)
    #image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    def __repr__(self):
        return f"Property('{self.title}', '{self.date_posted}')"

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    property = db.relationship('Property', backref='locations', lazy=True)
    def __repr__(self):
        return f"Location('{self.name}', '{self.description}')"

