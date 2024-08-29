from connection_db import ConnectionDB
from sqlalchemy import create_engine, column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


db = ConnectionDB()

class Database:
    __engine = None
    __session = None
    __base = None
    
    def __init__(self):
        kedu=db.connect("EbenFemi", "08033191820", "localhost", "schooldb")
        self.__engine = create_engine(kedu)
    

