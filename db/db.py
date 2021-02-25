#! python3
# db.py

import sqlite3


class DBConnection:

    def __init__(self, dbpath):
        self.connection = sqlite3.connect(dbpath)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def write_query(self, query, *args):
        self.cursor.execute(query, tuple(args))
        self.connection.commit()

    def read_query(self, query, *args):
        self.cursor.execute(query, tuple(args))
        values = self.cursor.fetchall()
        return values

    def read_headers(self):
        values = [
            d[0] for d in self.cursor.description
        ]
        return values
