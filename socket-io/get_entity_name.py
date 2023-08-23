import os
from dotenv import load_dotenv
import psycopg2
from pymongo import MongoClient
import re


load_dotenv()

host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")
user = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")

MONGO_URL = os.getenv("MONGODB_URI")

class Mongo:
    def __init__(self):
        self.database = self.get_database()
        
    def get_database(self, database_name="chainmart-mongodb", connection_string=MONGO_URL):

        client = MongoClient(connection_string)
        db = client[database_name]

        return db
    
    def get_collection(self, collection_name):
        return self.database[collection_name]
    
def replace_name(text, name_entity):
    text_replace = re.sub(r'\[(.*?)\]', "[{}]", text)
    return text_replace.format(name_entity)


if __name__ == "__main__":
    db = Mongo()
    collection = db.database["products"]
    name_entity = []
    for i in collection.find({}):
        name_entity.append(i["name"])
        
    f = open("./socket-io/data.txt", "r", encoding="utf-8")
    data = f.read()
    f.close()

    data = data.split("\n")
    
    list_data = []

    for entity in name_entity:
        for i in data:
            list_data.append(replace_name(i, entity))


    f = open("./socket-io/result.txt", "w", encoding="utf-8")
    
    for i in list_data:
        f.write(i + "\n")
    
    f.close()
