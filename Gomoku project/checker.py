import sqlite3
from hash import hashf


class connect:
    def __init__(self, database):
        try:
            self.conn = sqlite3.connect(database)
            self.c = self.conn.cursor()
        except Exception as error:
            print(error)

    def select_from_username(self):
        self.c.execute('SELECT username FROM userlogs ORDER BY rowid')
        print(self.c.fetchall())
        self.conn.commit()
        self.conn.close()

    def select(self):
        self.c.execute("""SELECT * FROM userlogs""")
        print(self.c.fetchall())
        self.conn.commit()
        self.conn.close()

    def login_checks(self):
        for username, password in self.c.execute("SELECT username, password FROM userlogs ORDER BY rowid"):
            print(username, password)

    def insert(self):
        table_info = ['testing', 'hello123']
        self.c.execute('INSERT INTO userlogs(username, password) VALUES(?,?)', table_info)
        self.conn.commit()
        self.conn.close()

    def delete_rows(self):
        self.c.execute('DELETE FROM userlogs')
        self.conn.commit()
        self.conn.close()

    def drop_table(self):
        self.c.execute('DROP TABLE userlogs')
        self.conn.commit()
        self.conn.close()

    def create_table(self):
        self.c.execute('CREATE TABLE userlogs('
                       'username VARCHAR UNIQUE,'
                       'password VARCHAR)')
        self.conn.commit()
        self.conn.close()


connect('userlog.db').select()
