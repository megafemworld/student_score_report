from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker
from cretedb import Admin, base



load_dotenv()






class Database:
    __engine = None
    __session= None

    def __init__(self,user, password,host,db_name):
        user = user
        password = password
        host = host
        db_name = db_name
        self.__engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db_name}")
      
    def engine(self):
        return self.__engine  
    def session(self):
        if self.__session is None:
            Session = sessionmaker(bind=self.__engine)
            self.__session = Session()
        return self.__session
    
    def creat(self):
        try:
            base.metadata.create_all(bind=self.__engine)
            print("created sucessfuly")
        except Exception as e:
            print(f"Reason being : {e}")
            
    def close(self):
        if self.__session:
            self.__session.close()
        if self.__engine:
            self.__engine.dispose()
        print("Session and engine closed successfully")
  
  
        
db = Database("eben","0267419026*Ee","localhost","schooldb")
db.creat()
session = db.session()

session.close()

# ab = db.engine()
# new_user = Admin(id=1,f_name="Alice", l_name="obi")
# session.add(new_user)
# session.commit()


    
    