from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, PasswordField, IntegerField, StringField, SelectField, RadioField, SubmitField,FileField
from wtforms.validators import DataRequired, NumberRange,Length,EqualTo
from flask_wtf.file import FileField, FileRequired,FileAllowed





class AddAdmin(FlaskForm):
    user_id = StringField('User_ID', validators=[DataRequired(), Length(min=7, max=7)])
    First_Name = StringField('FirstName', validators=[DataRequired(), Length(min=1, max=19)])
    Last_Name = StringField('LastName', validators=[DataRequired(), Length(min=3, max=30)])
    password = PasswordField('Password', validators=[DataRequired()])
    photo = FileField('Upload_photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Register')
    confirm_pass = PasswordField('Confirm-password', validators=[DataRequired(), EqualTo(password)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login In')

class AddTeacher(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    First_Name = StringField('First Name', validators=[DataRequired()])
    Last_Name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class AddStudent(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    First_Name = StringField('First Name', validators=[DataRequired()])
    Last_Name = StringField('Last Name', validators=[DataRequired()])
    class_name = RadioField('Class')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class Year(FlaskForm):
    Name = StringField('Year', validators=[DataRequired()])
    submit = SubmitField('Register')




class AssignSubject(FlaskForm):
    Teacher = StringField('Teacher ID', validators=[DataRequired()])
    Subjects = SelectField('Subjects',)
    Year = SelectField('Session', )
    Term = RadioField('Term', )
    submit = SubmitField('Register')

class Subjects(FlaskForm):
    Name = StringField('Subject', validators=[DataRequired()])
    submit = SubmitField('Register')

class StudentData(FlaskForm):
    Student_id = StringField('Student ID', render_kw={'readonly': True})
    Student_name = StringField('Student Name', render_kw={'readonly', True})
    CA = IntegerField('CA', validators=[DataRequired(), NumberRange(min=0, max=30)])
    Total = IntegerField('Total', validators=[DataRequired(), NumberRange(min=0, max=100)], render_kw={'readonly': True})
    
class CourseForm(FlaskForm):
    students = FieldList(FormField(StudentData), min_entries=1)
    submit = SubmitField('Upload Results')