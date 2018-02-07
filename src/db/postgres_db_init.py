import postgresql

class DBInitialisator:
    def __init__(self):
        self.url = 'pq://postgres:123@localhost:5432'
        self.conn = postgresql.open(self.url)
        self.create_database("test1")

    def __exit__(self):
        self.conn.close()

    def create_database(self, db_name):
        self.conn.execute('DROP DATABASE IF EXISTS ' + db_name)
        self.conn.execute('CREATE DATABASE ' + db_name)
        self.conn.close()
        self.conn = postgresql.open(self.url + '/' + db_name.lower())

