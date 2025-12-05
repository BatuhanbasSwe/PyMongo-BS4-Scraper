import datetime
from pymongo import MongoClient





class MongoDBManager:

    def __init__(self, uri, db_name, collection_name):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)

            # Test connection
            self.client.admin.command('ping')

            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]

            print(f"--> Connection Successful! Target: {self.db_name} -> {self.collection_name}")
            return True
        except Exception as e:
            print(f"--> Connection Failed: {e}")
            return False

    def insert_data(self, data_dict):
        """Inserts a single dictionary (document) into the collection."""
        if self.collection is not None:
            # Add timestamp automatically
            data_dict["created_at"] = datetime.datetime.now()
            result = self.collection.insert_one(data_dict)
            print(f"--> Data Inserted. ID: {result.inserted_id}")
        else:
            print("--> Connection not established yet!")

    def fetch_all_data(self):
        """Retrieves and prints all documents from the collection."""
        if self.collection is not None:
            data_cursor = self.collection.find()
            print("\n--- Current Data in Collection ---")
            for document in data_cursor:
                print(document)
            print("----------------------------------\n")
        else:
            print("--> Connection not established yet!")