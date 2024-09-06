from flask import Flask, redirect, request, flash, render_template, url_for
"""
Renders the teacher page with assigned subjects categorized by class.
Returns:
    rendered template: The HTML template for the teacher page.
"""
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


assigned_subjects = [
    {'id': '1', 'teacher_id': '1', 'subject_name': 'Mathematics', 'class_name': 'JSS1', 'term_name': '1', 'year_name': '2024/2025'},
    {'id': '2', 'teacher_id': '1', 'subject_name': 'Mathematics', 'class_name': 'JSS2', 'term_name': '2', 'year_name': '2024/2025'},
    {'id': '3', 'teacher_id': '1', 'subject_name': 'Mathematics', 'class_name': 'JSS3', 'term_name': '3', 'year_name': '2024/2025'},
    {'id': '4', 'teacher_id': '1', 'subject_name': 'Physics', 'class_name': 'JSS2', 'term_name': '2', 'year_name': '2024/2025'}
]

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


def check_assign(class_name, subject, year, term):
    for assigned_subject in assigned_subjects:
        if assigned_subject['class_name'] == class_name and assigned_subject['subject_name'] == subject and assigned_subject['year_name'] == year and assigned_subject['term_name'] == term and assigned_subject['teacher_id'] == current_user.id:
            pass
        else:
            flash('Subject not assigned to you.', 'danger')

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
    class_subjects = {}
    for subject in assigned_subjects:
        class_name = subject['class_name']
        subject_name = subject['subject_name']
        if class_name in class_subjects:
            class_subjects[class_name].append(subject_name)
        else:
            class_subjects[class_name] = [subject_name]
    
    return render_template('teacher.html', class_subjects=class_subjects)

@app.route('/teacher/result_upload/<class_name>/<subject>/<year:int>/<term:int>', methods=['GET', 'POST'])
@login_required
@role_required('teacher')
def teacher_upload():
    class_name = request.view_args['class_name']
    subject = request.view_args['subject']
    year = int(request.view_args['year'])
    term = int(request.view_args['term'])
    if request.method == 'POST' or request.method == 'GET':
        check_assign(class_name, subject, year, term)
        #form data
        students = [
    {'id': '1', 'username': 'st_student_user', 'first_name': 'Faith', 'last_name': 'Chike', 'password': 'password', 'class_name': 'JSS1', 'year_name': '2024/2025'},
    {'id': '2', 'username': 'st_student_user', 'first_name': 'Hajarat', 'last_name': 'Bello', 'password': 'password', 'class_name': 'JSS2', 'year_name': '2024/2025'},
    {'id': '3', 'username': 'st_student_user', 'first_name': 'Dayo', 'last_name': 'Bola', 'password': 'password', 'class_name': 'JSS3', 'year_name': '2024/2025'}
    {'id': '4', 'username': 'st_student_user', 'first_name': 'Ibrahim', 'last_name': 'Buhari', 'password': 'password', 'class_name': 'JSS1', 'year_name': '2024/2025'}
]
        
        if request.method == 'POST':
            for student in students:
                student_form = form.StudentData()
                student_form.student_id.data = student['id']
                student_form.student_name.data = student['first_name'] + ' ' + student['last_name']
                form.StudentData.append_entry(student_form)
        
        
        if form.validate_on_submit():
            for student_form in form.students:
                student_id = student_form.student_id.data
                ca = student_form.ca.data
                exam = student_form.exam.data
                total = ca + exam
                # save to database
        return render_template('result_upload.html', form=form, students=students)