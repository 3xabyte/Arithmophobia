from mysql.connector import connect

class Database:

    def __init__(self):

        # Connect to database
        self._db = connect(host="localhost",user="Exabyte",password="Asdfghjkl.1")

        # Get cursor
        self._cursor = self._db.cursor()

        # Create the phasmodb schema if it does not exist
        self._cursor.execute("CREATE SCHEMA IF NOT EXISTS phasmodb")
        self._db.close()

        # Reconnect
        self._db = connect(host="localhost",user="Exabyte",password="Asdfghjkl.1",database="phasmodb")
        self._cursor = self._db.cursor()

        # Create the games table with the columns if it does not exist
        self._cursor.execute(
            """CREATE TABLE IF NOT EXISTS Games (
            casenumber INT AUTO_INCREMENT,
            map varchar(3) NOT NULL,
            ghost varchar(20) NOT NULL,
            correct BOOL NOT NULL,
            died BOOL NOT NULL,
            PRIMARY KEY (casenumber)
        );""")
                
        return
    


    def insert(self, map, ghost, correct, death):

        sql = "INSERT INTO Games (map, ghost, correct, died) VALUES ('{:}', '{:}', {:}, {:});".format(map, ghost, correct, death)

        self._cursor.execute(sql)
        self._db.commit()
        print("Data has been inserted")

        return
    
    def get_count(self):

        sql = "SELECT COUNT(casenumber) FROM phasmodb.Games"

        self._cursor.execute(sql)

        count = self._cursor.fetchone()[0]

        return count
    
    def get_all_data(self):

        sql = "SELECT * FROM phasmodb.Games"
        self._cursor.execute(sql)
        
        results = self._cursor.fetchall()

        return results
    
    def query(self, sql):
        
        try:
            self._cursor.execute(sql)
        except:
            print("Error in SQL, please fix it!")
            return None
        
        results = self._cursor.fetchall()

        return results





db = Database()


# f = open("games.txt", "r")

# lines = f.readlines()

# for x in lines:
#     l = x.rstrip("\n")
#     splitter = l.split(',')

#     correct = False
#     death = False

#     if(splitter[3] == "True"):
#         correct = True
#     if(splitter[4] == "True"):
#         death = True

#     db.insert(splitter[1],splitter[2],correct,death)


# print(db.get_all_data())