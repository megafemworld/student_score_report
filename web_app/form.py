from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, PasswordField, IntegerField, StringField, SelectField, RadioField, SubmitField,FileField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, NumberRange,Length,EqualTo, ValidationError
from flask_wtf.file import FileField, FileRequired,FileAllowed



        


class AddAdmin(FlaskForm):
    First_Name = StringField('FirstName', validators=[DataRequired(), Length(min=1, max=19)])
    Last_Name = StringField('LastName', validators=[DataRequired(), Length(min=3, max=30)])
    photo = FileField('Upload_photo', validators=[ FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Register')
    
    def capital(self,First_Name):
        if not First_Name.data[0].isupper():  
            raise ValidationError(f'The {First_Name} must start with a capital letter.')

        
        
class AddTeacher(FlaskForm):
    First_Name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=25)])
    Last_Name = StringField('Last Name', validators=[DataRequired(),Length(min=3, max=25)])
    photo = FileField('Upload_photo', validators=[FileAllowed(['jpg', 'png'], 'Images only!'),FileRequired()])
    submit = SubmitField('Register')  
    

class LoginForm(FlaskForm):
    User_id = StringField('', validators=[DataRequired(),Length(min=3, max=25)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=3, max=25)])
    Login = SubmitField('Login In')



class AddStudent(FlaskForm):
    First_Name = StringField('First Name', validators=[DataRequired(),  Length(min=3, max=25)])
    Last_Name = StringField('Last Name', validators=[DataRequired(),  Length(min=3, max=25)])
    class_id = SelectField('Class', coerce=int)
    year_id = SelectField('Year', coerce=int)
    term_id = SelectField('Term', coerce=int)
    photo = FileField('Upload_photo', validators=[FileAllowed(['jpg', 'png'], 'Images only!'),FileRequired()])
    submit = SubmitField('Register')

# class Year(FlaskForm):
#     Name = StringField('Year', validators=[DataRequired()])
#     submit = SubmitField('Register')


# class studentclass(FlaskForm):
#     Name = StringField('Classes', validators=[DataRequired()])
#     submit = SubmitField('Register')

# class Term(FlaskForm):
#     Name = StringField('Term', validators=[DataRequired()])
#     submit = SubmitField('Register')

class Subjects(FlaskForm):
    Name = TextAreaField('Subjects (Comma-Separated)', validators=[DataRequired()])
    submit = SubmitField('Register')


class AssignSubject(FlaskForm):
    Teacher = StringField('Teacher ID', validators=[DataRequired()])
    Subjects = SelectField('Subjects',)
    Year = SelectField('Session', )
    Term = RadioField('Term', )
    submit = SubmitField('Register')



class StudentData(FlaskForm):
    Student_id = StringField('Student ID', render_kw={'readonly': True})
    Student_name = StringField('Student Name', render_kw={'readonly', True})
    CA = IntegerField('CA', validators=[DataRequired(), NumberRange(min=0, max=30)])
    Total = IntegerField('Total', validators=[DataRequired(), NumberRange(min=0, max=100)], render_kw={'readonly': True})
    
class CourseForm(FlaskForm):
    students = FieldList(FormField(StudentData), min_entries=1)
    submit = SubmitField('Upload Results')