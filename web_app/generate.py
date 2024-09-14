import random
from db_record.cretedb import Admin
from db_record.database import session
import os


def userid_generate():
    while True:
        randomNo = random.randint(10000, 99999)
        user_id = f"AD-{randomNo}"
        
        check_admin = session.query(Admin).filter_by(user_id=user_id).first()
        if not check_admin:
            return user_id
        


def save_upload():
    