from flask import Flask, request, redirect, render_template, Blueprint, url_for, session
from ...extensions.extensions import login, mail
from flask_login import login_user
from ...models.models import User
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message
import random
from string import ascii_uppercase

login_bp = Blueprint('login_bp', __name__)
verification_bp = Blueprint('verification_bp', __name__)

login.login_view = 'login'

s = URLSafeTimedSerializer('ThisIsSecret')

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

codes = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in codes:
            break
    
    return code
                        
                        

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    session['login_username'] = username
    
    if request.method == 'POST':
       user = User.query.filter_by(username=username).first()
       
       if user is None or not user.check_password(password):
            print('Invalid username or password')
            return redirect(url_for('login_bp.login'))
       token = generate_unique_code(6)
       session['token'] = token
       user = User.query.filter_by(username=username).first()
       email = user.email
       msg = Message('verification', sender='nuutti.project@gmail.com', recipients=[email])
       msg.body = 'Here is your verify token {}'.format(token)
       mail.send(msg)
       return redirect(url_for('verification_bp.verification'))
        
    return render_template('login.html')



@verification_bp.route('/verification', methods=['GET', 'POST'])
def verification():
    token_input = request.form.get('token-input')
    if request.method == 'POST':
        user = User.query.filter_by(username=session['login_username']).first()
        if token_input == session['token']:
            login_user(user)
            return redirect(url_for('main_bp.main'))
    return render_template('verification.html')