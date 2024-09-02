from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship



base = declarative_base()



class Admin(base):
    __tablename__ = 'admin'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    password = Column(String, nullable=False)
    photo = Column(String, nullable=True)

class Student(base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    reg_no = Column(String, nullable=False, unique=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    password = Column(String, nullable=False)
    class_id = Column(Integer, ForeignKey('class.id'))
    term_id = Column(Integer, ForeignKey('term.id'))

class Teacher(base):
    __tablename__ = 'teacher'
    teach_id = Column(Integer, primary_key=True)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    photo = Column(String, nullable=True)

class Class(base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    cls_name = Column(String, nullable=False, unique=True)
    
class Term(base):
    __tablename__ = 'term'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    
class Subject(base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    
class Enrollment(base):
    __tablename__ = 'enrollment'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    student = relationship("Student", back_populates="subjects")
    subject = relationship("Subject", back_populates="students")

Student.subjects = relationship("Enrollment", order_by=Enrollment.id, back_populates="student")
Subject.students = relationship("Enrollment", order_by=Enrollment.id, back_populates="subject")

class TeachingAssignment(base):
    __tablename__ = 'teaching_assignment'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    teacher = relationship("Teacher", back_populates="subjects")
    subject = relationship("Subject", back_populates="teachers")

Teacher.subjects = relationship("TeachingAssignment", order_by=TeachingAssignment.id, back_populates="teacher")
Subject.teachers = relationship("TeachingAssignment", order_by=TeachingAssignment.id, back_populates="subject")

class Score(base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    subject_id = Column(Integer, ForeignKey('subject.id'))
    exam_score = Column(Integer, nullable=False)
    test_score = Column(Integer, nullable=False)
    student = relationship("Student", back_populates="scores")
    subject = relationship("Subject", back_populates="scores")

Student.scores = relationship("Score", order_by=Score.id, back_populates="student")
Subject.scores = relationship("Score", order_by=Score.id, back_populates="subject")

    



    

    
