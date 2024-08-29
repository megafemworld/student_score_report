import MySQLdb


# class connection_db:
#     def __init__(self):
#         self.connection = None
        
#     def connect(self, host, user, password, db):
#         try:
#             self.connection = MySQLdb.connect(
#             host=self.host,
#             user=self.user,
#             password=self.password,
#             db=self.db
#             )
#             return self.connection
#         except MySQLdb.OperationalError as e:
#             print(f"Operational error: {e}")
#             return None
#         except MySQLdb.ProgrammingError as e:
#             print(f"Programming error: {e}")
#             return None
#         except MySQLdb.IntegrityError as e:
#             print(f"Integrity error: {e}")
#             return None
#         except MySQLdb.InternalError as e:
#             print(f"Internal error: {e}")
#             return None
#         except MySQLdb.DatabaseError as e:
#             print(f"Database error: {e}")
#             return None
#         except MySQLdb.DataError as e:
#             print(f"Data error: {e}")
#             return None
#         except MySQLdb.InterfaceError as e:
#             print(f"Interface error: {e}")
#             return None
#         except MySQLdb.Error as e:
#             print(f"Error: {e}")
#             return None
        
        
#     def cursor(self):
#         try:
#             return self.connection.cursor()
#         except Mysqldb.Error as e:
#             print(f"not sucessful: {e}")
#             return False
       
#     def commit(self):
#         self.connection.commit()
#         return True
    
#      def execute_con(self, query):
#         try:
#             cursor = self.cursor()
#             if cursor:
#                 cursor.execute(query)
#                 self.commit()
#                 return True
#             else:
#                 return False
#         except MySQLdb.DataError as e:
#             print(f"not sucessful: {e}")
#             return False
#         except MySQLdb.Error as e:
#             print(f"not sucessful: {e}")
#             return False
#         finally:
#             cursor.close()
     
    
#     def close(self):
#         try:
#             if self.connection:
#                 self.connection.close()
#             else:
#                 print("connection not found")
#                 return False
#             return True
#         except Mysqldb.Error as e:
#             print(f"not successful: {e}")
#             return False
#         finally:
#             self.connection.close()
    
#     def get_connected(self):
#         self.connect()  
        
    
    
class ConnectionDB:
    def __init__(self):
        self.connection = None

    def connect(self, user, password, host, db):
        try:
            connection_url = f"mysql+pymysql://{user}:{password}@{host}/{db}"
            print(f"Connected to {db} on {host}.")
            return connection_url
        except MySQLdb.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    


                    
                    
                    
                    
                    
                    
                    