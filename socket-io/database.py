import os
from dotenv import load_dotenv
import psycopg2
from pymongo import MongoClient


load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")
user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

MONGO_URL = os.getenv("MONGODB_URI")


class Postgres:
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
        print("Connection closed")



class Mongo:
    def __init__(self):
        self.database = self.get_database()
        
    def get_database(self, database_name="chainmartDevDB", connection_string=MONGO_URL):

        client = MongoClient(connection_string)
        db = client[database_name]

        return db
    
    def get_collection(self, collection_name):
        return self.database[collection_name]