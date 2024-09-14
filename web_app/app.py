from flask import Flask,render_template, request, redirect, url_for,flash
from form import AddAdmin
from generate import userid_generate
from db_record.cretedb import Admin
from werkzeug.security import check_password_hash
from db_record.database import session

app = Flask(__name__, template_folder='../templates', static_folder='../temp')
app.config['SECRET_KEY'] = 'secret'

@app.route('/')
@app.route('/index.html')
def login():
    
    return render_template('index.html')


@app.route('/admin.html')
def admin():
   
        return render_template('admin.html')
    
@app.route('/admin_reg.html')
def admin_reg():
    best = AddAdmin
    if best.validate_on_submit:
        user_id = userid_generate()
        passwd =Admin.set_password(best.password.data)
        admin = Admin(user_id=user_id, 
                      first_name=best.First_Name.data,
                      last_name=best.Last_Name.data,
                      password=passwd,photo=None)
        session.add(admin)
        session.commit()
        flash(f'Account created for {best.Last_Name.data}!', 'success')
    return render_template('admin_reg.html')

@app.route('/teacher-reg.html')
def teach_reg():
    return render_template('teacher-reg.html')

@app.route('/teacher.html')
def teacher():
    return render_template('teacher.html')

@app.route('/result.html')
def result():
    return render_template('result.html')


@app.route('/result_upload.html')
def result_upload():
    return render_template('result_upload.html')


@app.route('/student.html')
def student():
    return render_template('student.html')



if __name__ == "__main__":
    app.run(debug=True)
