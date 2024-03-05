import sqlite3

conn = sqlite3.connect("database.db")

conn.execute('''CREATE TABLE IF NOT EXISTS register (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    username Text NOT NULL,
    password Text NOT NULL
    
)''')


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, ism, username, password):
        with self.connection:
            return self.cursor.execute("INSERT INTO register (ism,username,password) VALUES(?,?,?)",
                                       (ism, username, password))

    def get_all_users(self):
        with self.connection:
            return self.cursor.execute("SELECT ism,username,password FROM register").fetchall()


conn.execute('''CREATE TABLE IF NOT EXISTS ariza (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    phone TEXT NOT NULL,
    children TEXT NOT NULL,
    adress TEXT NOT NULL,
    sinf TEXT NOT NULL,
    location1 NULL,
    location2 NULL
)''')


class Database1:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, fullname, phone, children, adress, sinf, location1, location2):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO ariza (fullname, phone, children,adress,sinf,location1,location2) VALUES(?,?,?,?,?,?,?)",
                (fullname, phone, children, adress, sinf, location1, location2))

    def get_all_users(self):
        with self.connection:
            return self.cursor.execute(
                "SELECT fullname, phone, children,adress,sinf,location1,location2 FROM register").fetchall()


conn.commit()
conn.close()
