from flask import session, Blueprint,render_template

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/main')
def main():
    return render_template('main.html')