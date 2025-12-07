from databasemanager import MongoDBManager
from new_scraper import IMDbScraper
from dataclasses import dataclass, asdict



@dataclass
class IMDbContent:
    title: str
    rating: float
    year: int
    category: str
    watched: bool = False

MY_URI = "mongodb+srv://oguzbatu2934_db_user:MYPASSWORD@cluster0.kejl8qw.mongodb.net/?appName=Cluster0"

MENU_OPTIONS = {
    "1": {"name": "Top 250 Movies", "url": "https://www.imdb.com/chart/top/?ref_=hm_nv_menu"},
    "2": {"name": "Top 250 TV Shows", "url": "https://www.imdb.com/chart/toptv/?ref_=chttp_nv_menu"},
    "3": {"name": "Most Popular Movies", "url": "https://www.imdb.com/chart/moviemeter/?ref_=chttvtp_nv_menu"}
}



def print_menu():
    print("\n" + "=" * 40)
    print("      IMDb SCRAPER FINAL (STABLE)      ")
    print("=" * 40)
    print("1. Top 250 Movies")
    print("2. Top 250 TV Shows")
    print("3. Most Popular Movies")
    print("---ALGORITHM---")
    print("4. Find highest Rating ")
    print("5. Mark a Movie as Watched")
    print("6. Show My Watched Movies")
    print("Q. Exit")
    print("="* 40)


##---RATING ALGORITHM---------
def filter_by_rating(db_manager: MongoDBManager):
    try:
        min_rating =float(input("Minimum Rating: (e.g. 8.3):"))
        query = {"rating": {"$gte": min_rating}}
        results = list(db_manager.collection.find(query).sort("rating", -1))

        if results:
            print(f"\n Found {len(results)} movies with minimum rating {min_rating} +:")
            for i, item in enumerate(results,1):
                status="Watched" if item.get("watched") else " "
                print(f"{i}.{item['title']}  | {item['rating']} {status}")
        else:
            print("No Movies found above rating")
    except ValueError:
        print(" Invalid Number or range entered.")

### -----MARK AS WATCHED -----
def mark_as_watched(db_manager):
    search_name = input(" Enter movie,serie or show name to mark as watched:").strip()
    movie= db_manager.collection.find_one({"title":{"$regex":search_name, "$options":"i"}})

    if movie:
        db_manager.collection.update_one(
            {"_id":movie["_id"]},
            {"$set":{"watched":True}}
        )
        print(f"Movies {search_name} has been marked as watched! .")
    else:
        print(f"Movie {search_name} does not exist. ")
### ----- WATCHED LIST ------
def show_watched_list(db_manager: MongoDBManager):
    query = {"watched":True}
    results=list(db_manager.collection.find(query))
    if results:
        print(f"\n Your watched list length is : --> {len(results)} :")
        for i ,item in enumerate(results,1):
            print(f"{i}. {item['title']} | {item['rating']} ")
    else:
        print("You haven't marked any movies or series as watched yet.")



if __name__ == "__main__":
    db_manager = MongoDBManager(MY_URI, "IMDb_Archive", "Allcontent")
    scraper = IMDbScraper()

    if db_manager.connect():
        while True:
            print_menu()
            choice = input("Choice: ").strip().upper()

            if choice == 'Q':
                break

            if choice in MENU_OPTIONS:
                target = MENU_OPTIONS[choice]

                try:
                    limit = int(input(f"Count for {target['name']}'  (Max 25): "))

                except:
                    limit = 25

                print(f"\n Fetching {target['name']} ...")
                data = scraper.scrape_data(target['url'], limit)

                if data:
                    print(f"{len(data)} items found , saving to MongoDB...")
                    for i, item in enumerate (data,1):
                        content = IMDbContent(
                            title=item["title"],
                            rating=item["rating"],
                            year=item["year"],
                            category=target["name"]
                        )
                        db_manager.insert_data(asdict(content),order_no=i)
                    print("Completed.")
                else:
                    print("No data inserted.")
                input("\n Press Enter to continue...")

            elif choice == '4':
                filter_by_rating(db_manager)
                input("\n Press Enter to continue...")
            elif choice == '5':
                mark_as_watched(db_manager)
                input("\n Press Enter to continue...")
            elif choice == '6':
                show_watched_list(db_manager)
                input("\n Press Enter to continue...")
            else:
                print("Invalid choice.")
    else:
        print("Database connection failed.")
db_manager.collection.delete_many({})
print("⚠️ DATABASE CLEARED!")
