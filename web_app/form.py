from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, PasswordField, IntegerField, StringField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from wtforms import StringField, SelectField, RadioField, SubmitField, IntergerField, SubmitField
from wtforms.validators import DataRequired

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
    class_name = RadioField('Class', class_name)
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class Year(FlaskForm):
    Name = StringField('Year', validators=[DataRequired()])
    submit = SubmitField('Register')


class AddAdmin(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    First_Name = StringField('First Name', validators=[DataRequired()])
    Last_Name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class AssignSubject(FlaskForm):
    Teacher = StringField('Teacher ID', validators=[DataRequired()])
    Teacher_name = 
    Subjects = SelectField('Subjects', subjects)
    Year = SelectField('Session', years)
    Term = RadioField('Term', terms)
    submit = SubmitField('Register')

class Subjects(FlaskForm):
    Name = StringField('Subject', validators=[DataRequired()])
    submit = SubmitField('Register')

class StudentData(FlaskForm):
    Student_id = StringField('Student ID', render_kw={'readonly': True})
    Student_name = StringField('Student Name', render_kw={'readonly', True})
    CA = IntegerField('CA', validators=[DataRequired(), NumberRange(min=0, max=30)])
    Exam = IntegerField('Exam' validators=[DataRequired(), NumberRange(min=0, max=70)])
    Total = IntegerField('Total', validators=[DataRequired(), NumberRange(min=0, max=100)], render_kw={'readonly': True})
    
class CourseForm(FlaskForm):
    students = FieldList(FormField(StudentData), min_entries=1)
    submit = SubmitField('Upload Results')
