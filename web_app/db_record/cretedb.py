from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, func, BigInteger, Sequence
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash



base = declarative_base()



class Admin(base):
    __tablename__ = 'admin'
    user_id = Column(String(40), primary_key=True, nullable=False, unique=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    password = Column(String(100), nullable=False)
    photo = Column(String(500), nullable=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        return self.password

class Student(base):
    __tablename__ = 'student'
    reg_no = Column(String(400), nullable=False, unique=True, primary_key=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    password = Column(String(100), nullable=False)
    class_id = Column(Integer, ForeignKey('class.id'))
    term_id = Column(Integer, ForeignKey('term.id'))
    year_id = Column(Integer, ForeignKey('year.id'))
    
class Teacher(base):
    __tablename__ = 'teacher'
    teach_id = Column(String(400), primary_key=True, unique=True, nullable=False)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    password = Column(String(100), nullable=False)
    photo = Column(String(500), nullable=True)

class Class(base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cls_name = Column(String(100), nullable=False, unique=True)
    
class Term(base):
    __tablename__ = 'term'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

class Year(base):
    __tablename__ = 'year'
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(BigInteger, nullable=False, unique=True)
    
class Subject(base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    
class Enrollment(base):
    __tablename__ = 'enrollment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(400), ForeignKey('student.reg_no'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    student = relationship("Student", back_populates="subjects")
    subject = relationship("Subject", back_populates="students")
Student.subjects = relationship("Enrollment", order_by=Enrollment.id, back_populates="student")
Subject.students = relationship("Enrollment", order_by=Enrollment.id, back_populates="subject")

class TeachingAssignment(base):
    __tablename__ = 'teaching_assignment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(String(400), ForeignKey('teacher.teach_id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    teacher = relationship("Teacher", back_populates="subjects")
    subject = relationship("Subject", back_populates="teachers")

Teacher.subjects = relationship("TeachingAssignment", order_by=TeachingAssignment.id, back_populates="teacher")
Subject.teachers = relationship("TeachingAssignment", order_by=TeachingAssignment.id, back_populates="subject")

class Score(base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(String(400), ForeignKey('student.reg_no'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    exam_score = Column(Integer, nullable=False)
    test_score = Column(Integer, nullable=False)
    grade = Column(String(2), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    student = relationship("Student", back_populates="scores")
    subject = relationship("Subject", back_populates="scores")

Student.scores = relationship("Score", order_by=Score.id, back_populates="student")
Subject.scores = relationship("Score", order_by=Score.id, back_populates="subject")

    



    

    
