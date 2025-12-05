from databasemanager import MongoDBManager


MY_URI = "mongodb+srv://oguzbatu2934_db_user:w9vjsbD855H1meI1@cluster0.kejl8qw.mongodb.net/?appName=Cluster0"


if __name__ == "__main__":
    print("Program starting...")


    my_db_manager = MongoDBManager(MY_URI, "ProjectDB", "Products")


    is_connected = my_db_manager.connect()

    if is_connected:
        test_product = {
            "name": "Laptop Case",
            "price": 450,
            "status": "In Stock"
        }

        my_db_manager.insert_data(test_product)
        my_db_manager.fetch_all_data()

    print("Program finished.")