from flask import Flask,render_template, request, redirect, url_for,flash, current_app, Blueprint,send_from_directory
from generate import userid_generate, pass_generate, teachid_generate,regno_generate,redirect_to_dashboard
from db_record.cretedb import Admin, Teacher, Student,Year,Class,Term,Subject
from werkzeug.security import check_password_hash
from db_record.database import session
from form import AddAdmin, AddTeacher, AddStudent,LoginForm,Subjects
from flask_login import LoginManager, login_required, current_user, login_user,logout_user

import logging
import os
import secrets



app = Flask(__name__, template_folder='../templates', static_folder='../temp')
app.config['SECRET_KEY'] = 'secret'


# @app.route('/')
# @app.route('/index.html')
# def login():
#     return render_template('index.html')



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
            flash(f"Account created for {jago.First_Name.data} {jago.Last_Name.data} was sucessful. userid ={teach_id} password = {password}", 'success')
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
            flash(f"Student: {cat.First_Name.data} {cat.Last_Name.data} Registration was sucessful. userid ={reg_no} password = {password}", 'success')
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

@app.route('/teacher.html')
def teacher():
    return render_template('teacher.html')

@app.route('/result.html')
def result():
    return render_template('result.html')


@app.route('/result_upload.html')
def result_upload():
    return render_template('result_upload.html')


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






if __name__ == "__main__":
    app.run(debug=True)
