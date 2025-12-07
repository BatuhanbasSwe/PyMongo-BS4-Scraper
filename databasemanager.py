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

    def insert_data(self, data_dict,order_no=None ):
        if self.collection is not None:
            data_dict["created_at"] = datetime.datetime.now()

            try:
                result = self.collection.update_one(
                    {"title":data_dict["title"]},
                    {"$set":data_dict},
                    upsert=True
                )

                title= data_dict.get('title', 'Unknown')
                rating = data_dict.get('rating', 0.0)
                if order_no:
                    print(f"{order_no} - {title} ({rating})")
                # -----------------------------
                else:
                    print(f"{title} | {rating}")
            except Exception as e:
                print(f"Error: {e}")

        else:
            print("--> Connection not established yet!")

