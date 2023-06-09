from flask import Flask, request, render_template, redirect, Blueprint, url_for, session
from ...extensions.extensions import db, mail
from ...models.models import User
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Message

signup_bp = Blueprint('signup_bp', __name__)
authentication_bp = Blueprint('authentication_bp', __name__)
s = URLSafeTimedSerializer('ThisIsSecret')

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    session['username_auth'] = request.form.get('username')
    email= request.form.get('email')
    session['password_auth'] = request.form.get('password')
    session['email_auth'] = email

    if request.method == 'POST':
        token = s.dumps(email, salt='authentication')
        msg = Message('Authentication', sender='nuutti.project@gmail.com', recipients=[email])
        link = url_for('authentication_bp.authentication', token=token, _external=True)
        msg.body = 'Click this link to verify your account {}'.format(link)
        mail.send(msg)

    return render_template('signup.html')

@authentication_bp.route('/authentication/<token>', methods=['GET', 'POST'])
def authentication(token):
    try:
        s.loads(token, salt='authentication', max_age=3600)
    except SignatureExpired:
        return render_template('signatureExpired.html')
    
    if request.method == 'POST':
        user = User(email=session['email_auth'], username=session['username_auth'])
        user.set_password(session['password_auth'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login_bp.login'))
    
    return render_template("authentication.html", token=token)