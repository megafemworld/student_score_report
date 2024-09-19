from flask import Flask, redirect, request, flash, render_template, url_for
from flask_login import LoginManager, login_required, current_user, login_user
from form import CourseForm, LoginForm, AddTeacher, AddStudent, Year, AddAdmin, AssignSubject, Subjects, StudentData, CourseForm
from app import db, app
from db_record.createdb import Admin, Teacher, Student, TeachingAssignment, Subject, Class, Term, Year, Score
# from models import Result, Score, TeachingAssignment


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def check_assign(class_name, subject_name, year_name, term_name, teacher_id):
    assignment = db.session.query(TeachingAssignment) \
        .join(Subject, TeachingAssignment.subject_id == Subject.id) \
        .join(Class, TeachingAssignment.class_id == Class.id) \
        .join(Term, TeachingAssignment.term_id == Term.id) \
        .join(Year, TeachingAssignment.year_id == Year.id) \
        .filter(TeachingAssignment.teacher_id == teacher_id) \
        .filter(Subject.name == subject_name) \
        .filter(Class.cls_name == class_name) \
        .filter(Term.name == term_name) \
        .filter(Year.year == year_name) \
        .options(
            joinedload(TeachingAssignment.subject),
            joinedload(TeachingAssignment.class_),
            joinedload(TeachingAssignment.term),
            joinedload(TeachingAssignment.year)
        ) \
        .first()

    return assignment

def students_load(class_name, year_name, term_name):
    students = db.session.query(Student.first_name, Student.last_name, Student.reg_no) \
        .join(Class, Student.class_id == Class.id) \
        .join(Year, Student.year_id == Year.id) \
        .join(Term, Student.term_id == Term.id) \
        .filter(Class.cls_name == class_name) \
        .filter(Year.year == year_name) \
        .filter(Term.name == term_name) \
        .all()

    return students

    

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
            .filter(TeachingAssignment.teacher_id == teacher_id)\
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


    class_subjects = {
    'JSS1': ['Mathematics'],
    'JSS2': ['Mathematics', 'Physics'],
    'JSS3': ['Mathematics']
    }

    return render_template('teacher.html', class_subjects=class_subjects, years=years, terms=terms, year_id=year_id, term_id=term_id)

@app.route('/teacher/result_upload/<class_name>/<subject>/<year:int>/<term:int>', methods=['GET', 'POST'])
@login_required
def result_upload():
    if current_user.role != teacher:
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
        
    class_name = request.view_args['class_name']
    subject = request.view_args['subject']
    year = int(request.view_args['year'])
    term = int(request.view_args['term'])
    teacher_id = current_user.get_id()
    assigner = check_assign(class_name, subject, year, term, teacher_id)
    if not assigner:
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
    
    students = students_load(class_name, year, term)
    
    form = CourseForm()
    for student in students:
        student_form = StudentData(
            student_id=student.reg_no,
            student_name=f"{student.first_name} {student.last_name}"
        )
        form.students.append_entry(student_form)

    if form.validate_on_submit():
        for student_form in form.students:
            student_id = student_form.student_id.data
            exam_score = student_form.exam_score.data
            test_score = student_form.test_score.data
            grade = student_form.grade.data
            score = Score(
                student_id=student_id,
                subject_id=assigner.subject_id,
                exam_score=exam_score,
                test_score=test_score,
                grade=grade
            )
            db.session.add(score)
        db.session.commit()
        flash('Results uploaded successfully', 'success')
        return redirect(url_for('teacher'))
    return render_template('result_upload.html', form=form, students=students)

@app.route('/student', methods=['GET', 'POST'])
@login_required
def result():
    if current_user.role != student:
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
    student_id = current_user.get_id()
    student_detail = db.session.query(Student).filter_by(reg_no=student_id).first()
    if not student:
        flash('Student not found', 'danger')
        return redirect(url_for('login'))
    student_name = student_detail.first_name + ' ' + student_detail.last_name
    student_reg = student_detail.reg_no
    student_class = student_detail.class_id
    student_term = student_detail.term_id
    student_year = student_detail.year_id

    scores = db.session.query(Score).join(Student).join(Subject).filter(
        Score.student_id == student_id,
        Student.class_id == student_class,
        Student.term_id == student_term,
        Student.year_id == student_year
    ).all()

    return render_template('result.html' , scores=scores, student_name=student_name, student_id=student_id, student_class=student_class,student_term=student_term)

    
    
    
    
    