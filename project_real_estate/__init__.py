# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from flask_mail import Mail
# import os
# from flask_migrate import Migrate
#
# #let us configure Flask and SQLAlchemy for the project
#
# db = SQLAlchemy()
# bcrypt = Bcrypt()
# login_manager = LoginManager()
# login_manager.login_view = 'routes.login'
# login_manager.login_message_category = 'info'
# mail = Mail()
# migrate = Migrate(db)
#
# # Initialize Flask extensions with the project_real_estate instance
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate_listings.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
# db.init_app(app)
# bcrypt.init_app(app)
# login_manager.init_app(app)
# mail.init_app(app)
# migrate.init_app(app, db)  # Correctly initialize the migration with project_real_estate and db
#
# from project_real_estate import routes


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)

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


