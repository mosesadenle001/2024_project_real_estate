from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# Initialize Flask app and CSRF protection
app = Flask(__name__)
csrf = CSRFProtect(app)

# # Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate_listings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail(app)
migrate = Migrate(app, db)

# Import routes after initializing extensions to avoid circular imports
from project_real_estate import routes

# Import routes and error handlers
with app.app_context():
    from project_real_estate import routes, errors



# Create admin user
with app.app_context():
    from project_real_estate.models import User
    if not User.query.filter_by(email='admin@mail.com').first():
        hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
        admin = User(username='admin', email='admin@mail.com', password=hashed_password, is_admin=True)
        db.session.add(admin)
        db.session.commit()

