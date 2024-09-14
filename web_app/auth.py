from flask import Flask, redirect, request, flash, render_template, url_for
from app import app
from flask_login import LoginManager, UserMixin, login_required, current_user
from functools import wraps
from form import CourseForm, LoginForm, AddTeacher, AddStudent, Year, AddAdmin, AssignSubject, Subjects, StudentData, CourseForm


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

# @app.route('/add/who', methods=['GET', 'POST'])
# @login_required
# @role_required('admin')
# def signup_who(who):

#     # if user_id is not found in admin table, redirect
#     if who == 'admin':
#         if request.method == 'POST':
#             #for
#             return render_template('admin_signup.html')
#     elif who == 'year':
#         if request.method == 'POST':
#             #form data
#             return render_template('year_signup.html')
#     elif who == 'student':
#         if request.method == 'POST':
#             #form data
#             return render_template('student_signup.html')
#     elif who == 'teacher':
#         if request.method == 'POST':
#             #form data
#             return render_template('teacher_signup.html')

# @app.route('/teacher')
# @login_required
# @role_required('teacher')
# def teacher():
#     class_subjects = {}
#     for subject in assigned_subjects:
#         class_name = subject['class_name']
#         subject_name = subject['subject_name']
#         if class_name in class_subjects:
#             class_subjects[class_name].append(subject_name)
#         else:
#             class_subjects[class_name] = [subject_name]

#     return render_template('teacher.html', class_subjects=class_subjects)

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
