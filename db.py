import sqlite3

conn = sqlite3.connect("database.db")

conn.execute('''CREATE TABLE IF NOT EXISTS start_ (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ism_familiya TEXT NOT NULL,
    username Text NOT NULL,
    id_ Text NOT NULL
    
)''')


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, ism_familiya, username, id_):
        with self.connection:
            return self.cursor.execute("INSERT INTO start_ (ism_familiya,username,id_) VALUES(?,?,?)",
                                       (ism_familiya, username, id_))

    def get_all_users(self):
        with self.connection:
            return self.cursor.execute("SELECT ism_familiya,username,id FROM start_").fetchall()


conn.execute('''CREATE TABLE IF NOT EXISTS ariza (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    phone TEXT NOT NULL,
    children TEXT NOT NULL,
    adress TEXT NOT NULL,
    sinf TEXT NOT NULL,
    location1 NOT NULL,
    location2 NOT NULL,
    data_time NOT NULL
)''')


class Database1:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, fullname, phone, children, adress, sinf, location1, location2,data_time):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO ariza (fullname, phone, children,adress,sinf,location1,location2,data_time) VALUES(?,?,?,?,?,?,?,?)",
                (fullname, phone, children, adress, sinf, location1, location2,data_time))

    def get_all_users(self):
        with self.connection:
            return self.cursor.execute(
                "SELECT id, fullname, phone, children,adress,sinf,location1,location2 ,data_time FROM ariza").fetchall()





conn.commit()
conn.close()
