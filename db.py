import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

conn.execute('''CREATE TABLE IF NOT EXISTS register (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ism TEXT NOT NULL,
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


conn.commit()
conn.close()
