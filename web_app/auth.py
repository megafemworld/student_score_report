from flask import Flask, request

app = Flask(__name__)

@app.route('/signup/who', methods=['GET', 'POST'])
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
def login
