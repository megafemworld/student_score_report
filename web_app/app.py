from flask import Flask,render_template, request, redirect, url_for,flash, current_app, Blueprint,send_from_directory
from generate import userid_generate, pass_generate, teachid_generate,regno_generate,redirect_to_dashboard
from db_record.cretedb import Admin, Teacher, Student,Year,Class,Term, TeachingAssignment, Subject, Score
from werkzeug.security import check_password_hash
from db_record.database import session
from form import AddAdmin, AddTeacher, AddStudent,LoginForm, StudentData, CourseForm,Subjects
from flask_login import LoginManager, login_required, current_user, login_user,logout_user
from sqlalchemy.orm import joinedload

import logging
import os
import secrets



app = Flask(__name__, template_folder='../templates', static_folder='../temp')
app.config['SECRET_KEY'] = 'secret'


# @app.route('/')
# @app.route('/index.html')
# def login():
#     return render_template('index.html')


class_id_to_name = {
    1: 'JSS1',
    2: 'JSS2',
    3: 'JSS3',
    4: 'SSS1',
    5: 'SSS2',
    6: 'SSS3',
    # Add more mappings if you have additional classes
}

class_name_to_id = {name: class_id for class_id, name in class_id_to_name.items()}

# Function to get class ID through class name
def get_class_id(class_name):
    return class_name_to_id.get(class_name)

def students_load(class_name):
    students_in_class = (
    session.query(Student)
    .join(Class)  # Join the Class table
    .filter(Class.cls_name == class_name)  # Filter by class name
    .all()  # Execute the query and get all results
)
    return students_in_class



login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(user_id):
    user = session.get(Admin, user_id) or session.get(Teacher, user_id) or session.get(Student, user_id)
    return user
    



def selectid(model):
    if model == Class:
        return [(obj.id, obj.cls_name) for obj in session.query(model).all()]
    elif model == Term:
        return [(obj.id, obj.name) for obj in session.query(model).all()]
    elif model == Year:
        return [(obj.id, obj.year) for obj in session.query(model).all()]
    else:
        return []

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
 
 


def save_pic(picdata):
    if picdata and picdata.filename:
        logging.info(f"Received file: {picdata.filename}")
        if not allowed_file(picdata.filename):
            logging.error('File type not allowed')
            raise ValueError('File type not allowed')

        rand = secrets.token_hex(4)
        _ , fphot = os.path.splitext(picdata.filename)
        picturegh = rand + fphot
        picturepath = os.path.join(current_app.root_path, 'temp', 'assest', 'assest_database', picturegh)
        os.makedirs(os.path.dirname(picturepath), exist_ok=True)

        picdata.save(picturepath)
        logging.info(f"File saved to: {picturepath}")
        return picturegh
    else:
        logging.error('No valid picture data received')
        raise ValueError('not a valid picture')
    
    
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(current_app.root_path, 'temp', 'assest', 'assest_database'), filename)
   

@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_to_dashboard(current_user)
    log = LoginForm()
    if log.validate_on_submit():
        # Extract form data
        amen = log.User_id.data
        jesu = log.password.data
        
        # Teacher login check
        if amen.startswith('TE-'):
            user = session.query(Teacher).filter_by(teach_id=amen).first()
            if user and user.check_password(jesu):
                login_user(user)
                return redirect(url_for('teacher'))
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
        
        # Admin login logic (as an example, assuming admin starts with 'AD-')
        elif amen.startswith('AD-'):
            user = session.query(Admin).filter_by(user_id=amen).first()
            print(f'{user}')
            if user and user.check_password(jesu):
                login_user(user)
                return redirect(url_for('admin'))  
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
            
        if amen.startswith('STU-'):
            user = session.query(Student).filter_by(reg_no=amen).first()
            if user and user.check_password(jesu):
                login_user(user)
                return redirect(url_for('result'))
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('login'))
            
        
        else:
            flash('Invalid user ID format', 'danger')
            return redirect(url_for('login'))

    # Render login page
    return render_template('index.html', log=log)


  




    
@app.route('/admin.html/admin_reg.html', methods=['POST','GET'])
def admin_reg():
    if current_user.__class__.__name__ != 'Admin':
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
    best = AddAdmin()
    if best.validate_on_submit():
        try:
            user_id = userid_generate()
            print(f'{user_id}')
            password = pass_generate(Admin)
            print(f'{password}')
            picture = save_pic(best.photo.data)
            
            admin = Admin(user_id=user_id, 
                      first_name=best.First_Name.data,
                      last_name=best.Last_Name.data,
                      password=None,photo=picture)
            admin.set_password(password)
            session.add(admin)
            session.commit()
            flash(f'Account created for {best.Last_Name.data}-', 'success')
            return redirect(url_for('admin_reg'))
        except Exception as e:
            logging.error(f"error creating account: {str(e)}")
            flash(f'Account creation failed!', 'danger')
    else:
        logging.error(f"Form validation errors: {best.errors}")
        print(f"{best.errors}")
        
    return render_template('admin_reg.html', best=best)

@app.route('/admin.html')
@login_required
def admin():
    imagefile = None
    if current_user.is_authenticated:
        imagefile = url_for('uploaded_file', filename=current_user.photo)
    return render_template('admin.html', imagefile=imagefile)

@app.route('/admin.html/teacher_reg.html', methods=['POST','GET'])
def teach_reg():
    if current_user.__class__.__name__ != 'Admin':
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
    jago = AddTeacher()
    if jago.validate_on_submit():
        try:
            teach_id = teachid_generate()
            print(f'{teach_id}')
            password = pass_generate(Teacher)
            print(f'{password}')
            picture = save_pic(jago.photo.data)
            teach = Teacher(teach_id=teach_id,
                            first_name=jago.First_Name.data,
                            last_name=jago.Last_Name.data,
                            password=None,photo=picture)
            teach.set_password(password)
            session.add(teach)
            session.commit()
            flash(f"Account created for {jago.First_Name.data} {jago.Last_Name.data} was sucessful", 'success')
            return redirect(url_for('teach_reg'))
        except Exception as e:
             logging.error(f"error creating account: {str(e)}")
             flash(f'Account creation failed!', 'danger')
    else:
        logging.error(f"Form validation errors: {jago.errors}")
        print(f"{jago.errors}")
            
    return render_template('teacher_reg.html', title='AddTeacher', jago=jago)


@app.route('/admin.html/student.html', methods=['GET','POST'])
def student():
    if current_user.__class__.__name__ != 'Admin':
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
    cat = AddStudent()
    cat.class_id.choices = selectid(Class) 
    cat.term_id.choices = selectid(Term)  
    cat.year_id.choices = selectid(Year)    
    if cat.validate_on_submit():
            reg_no= regno_generate()
            print(f'{reg_no}')
            password = pass_generate(Student)
            print(f'{password}')
            picture = save_pic(cat.photo.data)
            student = Student(reg_no=reg_no,
                              first_name=cat.First_Name.data,
                              last_name= cat.Last_Name.data,
                              photo=picture,
                              password = None,
                              class_id =cat.class_id.data,
                              term_id = cat.term_id.data,
                              year_id = cat.year_id.data)
            student.set_password(password)
            session.add(student)
            session.commit()
            flash(f"Student: {cat.First_Name.data} {cat.Last_Name.data} Registration was sucessful.", 'success')
            return redirect(url_for('student'))
    else:
        logging.error(f"Form validation errors: {cat.errors}")
        print(f"{cat.errors}")
    return render_template('student.html', cat=cat)

@app.route('/logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('login'))

# @app.route('/teacher.html')
# def teacher():
#     return render_template('teacher.html')

# @app.route('/result.html')
# def result():
#     return render_template('result.html')


# @app.route('/result_upload.html')
# def result_upload():
#     return render_template('result_upload.html')


@app.route('/admin.html/subject.html', methods=['GET', 'POST'])
def subject():
    form = Subjects()
    if form.validate_on_submit():
        subjects_input = form.Name.data
        print(f"Input from form: {subjects_input}")
        if isinstance(subjects_input, str):
            subjects_list = [subject.strip() for subject in subjects_input.split(',')]

            for subject_name in subjects_list:
                if subject_name: 
                    existing_subject = session.query(Subject).filter_by(name=subject_name).first()
                    if existing_subject:
                        flash(f'Subject "{subject_name}" already exists!', 'danger')
                    else:
                        new_subject = Subject(name=subject_name)
                        session.add(new_subject)

            session.commit()
            flash(f'Subjects added successfully! by Admin {current_user.first_name}', 'success')
            return redirect(url_for('subject')) 
        else:
            flash('Invalid input. Please enter subjects as a comma-separated string.', 'danger')
    return render_template('subject.html', form=form)


#fem

@app.route('/teacher', methods=['GET', 'POST'])
@login_required
def teacher():
    if current_user.__class__.__name__ != 'Teacher':
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
    class_subjects = {}
    teacher_id = current_user.teach_id
    
    selected_year = session.query(Year).first()
    selected_term = session.query(Term).first()
    
    
    if teacher_id:
        assigned_subjects = session.query(TeachingAssignment) \
            .filter(TeachingAssignment.teacher_id == teacher_id) \
            .options(joinedload(TeachingAssignment.subject)) \
            .all()
    else:
        assigned_subjects = []
    # Initialize class_subjects as a dictionary
    class_subjects = {}

    for assignment in assigned_subjects:
        class_name = class_id_to_name.get(assignment.class_id)  # Get the class name
        subject_name = assignment.subject.name  # Accessing the subject's name
        subject_id = assignment.subject.id      # Accessing the subject's ID
        
        if class_name in class_subjects:
            class_subjects[class_name].append({subject_name: subject_id})  # Store as dictionary
        else:
            class_subjects[class_name] = [{subject_name: subject_id}]  # Start new list with a dictionary

    # class_subjects = {
    # 'JSS1': ['Mathematics': 1, 'Physics': 2],
    # 'JSS2': ['Mathematics: 1', 'Physics: 2', 'Chemistry: 3'],
    # 'JSS3': ['Mathematics': 1', 'Physics': 2', 'Chemistry': 3]
    # }

    return render_template('teacher.html', class_subjects=class_subjects, assigned_subjects=assigned_subjects, selected_year=selected_year, selected_term=selected_term)

# @app.route('/result.html', methods=['GET', 'POST'])
# @login_required
# def result():
#     if current_user.__class__.__name__ != 'Student':
#         flash('You are not authorized to view this page', 'danger')
#         return redirect(url_for('login'))
#     student_id = current_user.get_id()
#     student_detail = session.query(Student).filter_by(reg_no=student_id).first()
#     if not student:
#         flash('Student not found', 'danger')
#         return redirect(url_for('login'))
#     student_name = student_detail.first_name + ' ' + student_detail.last_name
#     student_reg = student_detail.reg_no
#     student_class = student_detail.class_id
#     student_term = student_detail.term_id
#     student_year = student_detail.year_id

#     scores = session.query(Score).join(Student).join(Subject).filter(
#         Score.student_id == student_id,
#         Student.class_id == student_class,
#         Student.term_id == student_term,
#         Student.year_id == student_year
#     ).all()

#     return render_template('result.html' , scores=scores, student_name=student_name, student_id=student_id, student_class=student_class,student_term=student_term)

@app.route('/teacher/result_upload/<class_name>/<subject>/<int:year>/<int:term>', methods=['GET', 'POST'])
@login_required
def result_upload(class_name, subject, year, term):
    if current_user.__class__.__name__ != 'Teacher':
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
        
    class_name = request.view_args['class_name']
    class_name = class_name.upper()
    subject_id = request.view_args['subject']
    subject_name = session.query(Subject).get(subject_id).name
    year = int(request.view_args['year'])
    term = int(request.view_args['term'])
    teacher_id = current_user.get_id()
    # assigner = check_assign(class_name, subject, year, term, teacher_id)
    # if not assigner:
    #     flash('You are not authorized to view this page', 'danger')
    #     return redirect(url_for('login'))
    
    students = students_load(class_name)
    
    form = CourseForm()
    if request.method == 'GET':
        for student in students:
            student_form = StudentData()
            student_form.student_id.data = student.reg_no
            student_form.student_name.data = f"{student.first_name} {student.last_name}"
            form.students.append_entry(student_form) 
    for student_form in form.students:
        student_id = student_form.student_id.data
        exam_score = student_form.exam_score.data
        test_score = student_form.test_score.data
        grade = student_form.grade.data
        print(f"Student ID: {student_id}, Exam Score: {exam_score}, Test Score: {test_score}, Grade: {grade}")
           
    print(request.form)
    if form.validate_on_submit():
        print("Form submitted and valid!")
        for student_form in form.students:
            student_id = student_form.student_id.data
            exam_score = student_form.exam_score.data
            test_score = student_form.test_score.data
            grade = student_form.grade.data
            score = Score(
                student_id=student_id,
                subject_id=subject_id,
                exam_score=exam_score,
                test_score=test_score,
                year_id=year,
                class_id=get_class_id(class_name),
                term_id=term,
                grade=grade
            )
            session.add(score)
        session.commit()
        flash('Results uploaded successfully', 'success')
        return redirect(url_for('teacher'))
    else:
        print("Form not submitted or invalid", form.errors)
    return render_template('result_upload.html', form=form, students=students, class_name=class_name, subject_name=subject_name)



@app.route('/result.html', methods=['GET', 'POST'])
@login_required
def result():
    if current_user.__class__.__name__ != 'Student':
        flash('You are not authorized to view this page', 'danger')
        return redirect(url_for('login'))
    student_id = current_user.get_id()
    student_detail = session.query(Student).filter_by(reg_no=student_id).first()
    if not student:
        flash('Student not found', 'danger')
        return redirect(url_for('login'))
    student_name = student_detail.first_name + ' ' + student_detail.last_name
    student_reg = student_detail.reg_no
    student_class = student_detail.class_id
    student_term = student_detail.term_id
    student_year = student_detail.year_id

    scores = session.query(Score).join(Student).join(Subject).filter(
        Score.student_id == student_id,
        Student.class_id == student_class,
        Student.term_id == student_term,
        Student.year_id == student_year
    ).all()

    return render_template('result.html' , scores=scores, student_name=student_name, student_id=student_id, student_class=student_class,student_term=student_term)




if __name__ == "__main__":
    app.run(debug=True)
