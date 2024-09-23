import random
from db_record.cretedb import Admin, Teacher, Student
from db_record.database import session
import os
import string
from wtforms import ValidationError
from flask import redirect,url_for





def userid_generate():
    while True: 
            randomNo = random.randint(10000, 99999)
            user_id = f"AD-{randomNo}"
        
            check_admin = session.query(Admin).filter_by(user_id=user_id).first()
            if not check_admin:
                return user_id
            
def teachid_generate():
     while  True:          
        randomNo = random.randint(10000, 99999)
        teach_id = f"TE-{randomNo}"
        
        check_admin = session.query(Teacher).filter_by(teach_id=teach_id).first()
        if not check_admin:
            return teach_id
        
def regno_generate():
     while  True:          
        randomNo = random.randint(1000000, 999999999)
        reg_no = f"STU-{randomNo}-Alx"
        
        check_admin = session.query(Student).filter_by(reg_no=reg_no).first()
        if not check_admin:
            return reg_no
        
def pass_generate( danku):
    while True:
        
        Noba = [random.choice(string.digits)for _ in range(9)]
        letter = [random.choice(string.ascii_letters)for _ in range(2)]
        symbol = ['#','%','*','!','$','&','+','?','@','/']
        sym = random.choice(symbol)
        
        pask = letter + Noba + [sym]
        
        random.shuffle(pask)
        password = ''.join(pask)
        check_admin = session.query(danku).filter_by(password=password).first()
        if not check_admin:
            return password

def redirect_to_dashboard(user):
    """Redirect the user to their respective dashboard based on their role."""
    if isinstance(user, Admin):
        return redirect(url_for('admin'))
    elif isinstance(user, Teacher):
        return redirect(url_for('teacher'))
    elif isinstance(user, Student):
        return redirect(url_for('result'))
    else:
        # Default redirect if the role is unknown
        return redirect(url_for('login'))
# def save_upload():
    