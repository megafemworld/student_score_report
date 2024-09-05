from flask import Flask, request, flash, render_template
from flask_login import LoginManager, UserMixin, login_required, current_user
from functools import wraps
from . import form

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


users = {
    'admin_user': {'id': '1', 'username': 'adm_admin_user', 'password': 'password'},
    'teacher_user': {'id': '2', 'username': 'te_teacher_user', 'password': 'password'},
    'student_user': {'id': '3', 'username': 'st_student_user', 'password': 'password'}
}


def get_user_role(username):
    if username.startswith('adm'):
        return 'admin'
    elif username.startswith('te'):
        return 'teacher'
    elif username.startswith('st'):
        return 'student'
    else:
        return 'unknown'

class UserLogin(UserMixin):
    def __init__(self, id, username, role):
        self.id = user.id
        self.username = user.username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    if user['id'] == user_id:
        return UserLogin(user[id], user['username'], get_user_role(user['username']))

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Login to access')
            if current_user.role != role_required:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/add/who', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def signup_who(who):
    
    # if user_id is not found in admin table, redirect
    if who == 'admin':
        if request.method == 'POST':
            #for
            return render_template('admin_signup.html')
    elif who == 'year':
        if request.method == 'POST':
            #form data
            return render_template(year_signup.html)
    elif who == 'student':
        if request.method == 'POST':
            #form data
            return render_template('student_signup.html')
    elif who == 'teacher':
        if request.method == 'POST':
            #form data
            return render_template('teacher_signup.html')
    else:
        return "not found oooo", 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = form.LoginForm()
    if request.method == 'POST' and form.validate_on_form():
        user = form.user.data
        if user.lower().startswith("st"):
            if user and user['password'] == password:
                user_obj = UserLogin(user['id'], user['username'], get_user_role(user['username']))
        elif user.lower().startswith("te"):
            if user and user['password'] == password:
                user_obj = UserLogin(user['id'], user['username'], get_user_role(user['username']))
            pass
        elif user.lower().startswith("adm"):
            if user and user['password'] == password:
                user_obj = UserLogin(user['id'], user['username'], get_user_role(user['username']))
        else:
            pass
    return render_template('login.html', form=form)

@app.route('/teacher')
@login_required
@role_required('teacher')
def teacher():
    return render_template('teacher.html')

