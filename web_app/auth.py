from flask import Flask, request, flash
from . import form

app = Flask(__name__)

@app.route('/signup/who', methods=['GET', 'POST'])
@login_required
def signup_who(who):
    # if user_id is not found in admin table, redirect
    if who == 'admin':
        if request.method == 'POST':
            #form data
        render_template('admin_signup.html')
    elif who == 'year':
        if request.method == 'POST':
            #form data
        render_template('year_signup.html')
    elif who == 'student':
        if request.method == 'POST':
            #form data
        render_template('student_signup.html')
    elif who == 'teacher':
        if request.method == 'POST':
            #form data
        render_template('teacher_signup.html')
    else:
        return "not found oooo", 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method = 'POST' && form.validate_on_form():
        user = form.user.data
        if user.lower().startswith("st"):
            pass
        else if user.lower().startswith("te"):
            pass
        else if user.lower().startswith("adm"):
            pass
        else:
            pass
    return render_template('login.html', form=form)
