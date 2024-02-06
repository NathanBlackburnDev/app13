import sqlite3

# Create database class
class Database:
    # Initalise database name
    def __init__(self):
        self.DBname = 'database.db'

    # Create connection method
    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.DBname)
        except Exception as e:
            print(e)

        return conn
    
    # Create disconnect method
    def disconnect(self, conn):
        conn.close()

    # Create query method
    def queryDB(self, command, params=[]):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(command, params)
        result = cur.fetchall()
        self.disconnect(conn)
        return result
    
    # Create update method
    def updateDB(self, command, params=[]):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(command, params)
        conn.commit()
        result = cur.fetchall()
        self.disconnect(conn)
        return result

