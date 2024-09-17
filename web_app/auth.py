from flask import Flask, redirect, request, flash, render_template, url_for
from app import app
from flask_login import LoginManager, login_required, current_user, login_user
from form import CourseForm, LoginForm, AddTeacher, AddStudent, Year, AddAdmin, AssignSubject, Subjects, StudentData, CourseForm


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    admin = admin.query.get(user_id)
    if admin:
        return admin
    teacher = teacher.query.get(user_id)
    if teacher:
        return teacher
    Student = student.query.get(user_id)
    if Student:
        return Student
    return None


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username.startswith('AD_'):
        admin = admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            login_user(admin)
            return redirect(url_for('admin'))
    if username.startswith('TE_'):
        teacher = teacher.query.filter_by(username=username).first()
        if teacher and teacher.check_password(password):
            login_user(teacher)
            return redirect(url_for('teacher'))
    if username.startswith('ST_'):
        student = student.query.filter_by(username=username).first()
        if student and student.check_password(password):
            login_user(student)
            return redirect(url_for('student'))
    flash('Invalid username or password', 'danger')
    return redirect(url_for('login'))

'''
@app.route('admin_reg', methods=['GET', 'POST'])
@login_required
def admin_reg():
    """sign up for admin, teacher, student or year"""
    if current_user.role != 'admin':
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
    form = AddAdmin()
    if form.validate_on_submit():
        pass

@app.route('student_reg', methods=['GET', 'POST'])
@login_required
def admin_reg():
    """sign up for admin, teacher, student or year"""
    if current_user.role != 'admin':
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
    form = AddAdmin()
    if form.validate_on_submit():
        pass

@app.route('student_reg', methods=['GET', 'POST'])
@login_required
def admin_reg():
    """sign up for admin, teacher, student or year"""
    if current_user.role != 'admin':
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
    form = AddAdmin()
    if form.validate_on_submit():
        pass

'''

@app.route('/teacher', methods=['GET', 'POST'])
@login_required
def teacher():
    if current_user.role != 'teacher':
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
    class_subjects = {}
    teacher_id = current_user.get_id()
    selected_year = request.form.get('year')
    selected_term = request.form.get('term')
    
    years = db.session.query(year).all()
    terms = db.session.query(term).all()
    
    year_id = selected_year
    term_id = selected_term
    
    if teacher_id:
        assigned_subjects = db.session.query(TeachingAssignment)\
            .filter(TeachingAssignment.teacher_id == user_id)\
            .filter(TeachingAssignment.year_id == year_id)\
            .filter(TeachingAssignment.term_id == term_id)\
            .options(joinedload(TeachingAssignment.subject))\
            .all()
    else:
        assigned_subjects = []
    
    for subject in assigned_subjects:
        class_name = subject['class_name']
        subject_name = subject['subject_name']
        if class_name in class_subjects:
            class_subjects[class_name].append(subject_name)
        else:
            class_subjects[class_name] = [subject_name]

    return render_template('teacher.html', class_subjects=class_subjects, years=years, terms=terms)

# @app.route('/teacher/result_upload/<class_name>/<subject>/<year:int>/<term:int>', methods=['GET', 'POST'])
# @login_required
# @role_required('teacher')
# def teacher_upload():
#     class_name = request.view_args['class_name']
#     subject = request.view_args['subject']
#     year = int(request.view_args['year'])
#     term = int(request.view_args['term'])
#     if request.method == 'POST' or request.method == 'GET':
#         check_assign(class_name, subject, year, term)
#         #form data
#         students = [
#             {'id': '1', 'username': 'st_student_user', 'first_name': 'Faith', 'last_name': 'Chike', 'password': 'password', 'class_name': 'JSS1', 'year_name': '2024/2025'},
#             {'id': '2', 'username': 'st_student_user', 'first_name': 'Hajarat', 'last_name': 'Bello', 'password': 'password', 'class_name': 'JSS2', 'year_name': '2024/2025'},
#             {'id': '3', 'username': 'st_student_user', 'first_name': 'Dayo', 'last_name': 'Bola', 'password': 'password', 'class_name': 'JSS3', 'year_name': '2024/2025'},
#             {'id': '4', 'username': 'st_student_user', 'first_name': 'Ibrahim', 'last_name': 'Buhari', 'password': 'password', 'class_name': 'JSS1', 'year_name': '2024/2025'}
#         ]

#         form = CourseForm()

#         if request.method == 'GET':
#             for student in students:
#                 student_form = StudentData(
#                     student_id=student['id'],
#                     student_name=student['first_name'] + ' ' + student['last_name']
#                 )
#                 form.students.append_entry(student_form)

#     return render_template('result_upload.html', form=form)
