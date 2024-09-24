from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, BigInteger, Sequence, CheckConstraint
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

Base = declarative_base()







class Admin(Base,UserMixin):
    __tablename__ = 'admin'
    user_id = Column(String(40), primary_key=True, nullable=False, unique=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    password = Column(String(400), nullable=False)
    photo = Column(String(500), nullable=True)
    
    def set_password(self,password):
        self.password = generate_password_hash(password)
        return self.password
    
    def check_password(self,password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return self.user_id

class Student(Base,UserMixin):
    __tablename__ = 'student'
    reg_no = Column(String(400), nullable=False, unique=True, primary_key=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    photo = Column(String(500), nullable=False)
    password = Column(String(400), nullable=False)
    class_id = Column(Integer, ForeignKey('class.id'))
    term_id = Column(Integer, ForeignKey('term.id'))
    year_id = Column(Integer, ForeignKey('year.id'))
    
    
    def set_password(self,password):
        self.password = generate_password_hash(password)
        return self.password
    
    def check_password(self,password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return self.reg_no
        
    
class Teacher(Base,UserMixin):
    __tablename__ = 'teacher'
    teach_id = Column(String(400), primary_key=True, unique=True, nullable=False)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    password = Column(String(500), nullable=False)
    photo = Column(String(500), nullable=True)
    
    
    def set_password(self,password):
        self.password = generate_password_hash(password)
        return self.password
    
    def check_password(self,password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return self.teach_id

class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cls_name = Column(String(100), nullable=False, unique=True)
    
    # def __init__(self, *args, **kwargs):
    #     super(Class, self).__init__(*args, **kwargs)
    #     self.class_id.choices = [(cls.id, cls.cls_name) for cls in Class.query.all()]
    
class Term(Base):
    __tablename__ = 'term'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    
    def __init__(self, *args, **kwargs):
        super(Term, self).__init__(*args, **kwargs)
        self.term_id.choices = [(cls.id, cls.name) for cls in Term.query.all()]
    

class Year(Base):
    __tablename__ = 'year'
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(BigInteger, nullable=False, unique=True)
    
    # def __init__(self, *args, **kwargs):
    #     super(Year, self).__init__(*args, **kwargs)
    #     self.year_id.choices = [(cls.id, cls.year) for cls in Year.query.all()]
    
    
class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    
class Enrollment(Base):
    __tablename__ = 'enrollment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(400), ForeignKey('student.reg_no'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    student = relationship("Student", back_populates="subjects")
    subject = relationship("Subject", back_populates="students")
Student.subjects = relationship("Enrollment", order_by=Enrollment.id, back_populates="student")
Subject.students = relationship("Enrollment", order_by=Enrollment.id, back_populates="subject")

class TeachingAssignment(Base):
    __tablename__ = 'teaching_assignment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(String(400), ForeignKey('teacher.teach_id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    year_id = Column(Integer, ForeignKey('year.id'))
    term_id = Column(Integer, ForeignKey('term.id'))
    class_id = Column(Integer, ForeignKey('class.id'))
    teacher = relationship("Teacher", back_populates="subjects")
    subject = relationship("Subject", back_populates="teachers")

Teacher.subjects = relationship("TeachingAssignment", order_by=TeachingAssignment.id, back_populates="teacher")
Subject.teachers = relationship("TeachingAssignment", order_by=TeachingAssignment.id, back_populates="subject")

class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(400), ForeignKey('student.reg_no'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    class_id = Column(Integer, ForeignKey('class.id'))
    term_id = Column(Integer, ForeignKey('term.id'))
    year_id = Column(Integer, ForeignKey('year.id'))
    exam_score = Column(Integer, nullable=False)
    test_score = Column(Integer, nullable=False)
    grade = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    __table_args__ = (
        CheckConstraint('exam_score BETWEEN 0 AND 70', name='check_exam_score_range'),
        CheckConstraint('test_score BETWEEN 0 AND 30', name='check_test_score_range'),
    )
    
    student = relationship("Student", back_populates="scores")
    subject = relationship("Subject", back_populates="scores")
    

Student.scores = relationship("Score", order_by=Score.id, back_populates="student")
Subject.scores = relationship("Score", order_by=Score.id, back_populates="subject")

    



 
    

    