from flask import Flask
from .extensions.extensions import db, login, mail
from decouple import config
from .routes.auth.login import login_bp, verification_bp
from .routes.auth.signup import signup_bp, authentication_bp
from .routes.main.main import main_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_user_auth.db'
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')
app.config['MAIL_SERVER'] = config('MAIL_SERVER')
app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
app.config['MAIL_DEFAULT_SENDER'] = config('MAIL_DEFAULT_SENDER')
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_MAX_EMAIL'] = None
app.config['MAIL_ASCII_ATTACHMENT'] = False

db.init_app(app)
login.init_app(app)
mail.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(authentication_bp)
app.register_blueprint(main_bp)
app.register_blueprint(verification_bp)