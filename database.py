import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

host = os.getenv("host")
port = os.getenv("port")
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")


class Database:
    def __init__(self):
        self.conn = None
        self.initialConnection()

    def initialConnection(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password,
                )
            except (Exception, psycopg2.DatabaseError) as error:
                print("Initial connection error")
                print(error)
        else:
            print("Connection is already established")

    def connect(self):
        if self.conn is None:
            try:
                self.conn = psycopg2.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password,
                )
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
        else:
            print("Connection is already established")

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
        else:
            print("Connection is already closed")
