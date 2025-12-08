"""
IMDb Scraper Pro - Main Application Module.
This module handles the CLI interface, user interactions,
and coordinates the scraping and database operations.
"""


import argparse
from dataclasses import dataclass, asdict
from databasemanager import MongoDBManager
from new_scraper import IMDbScraper


@dataclass
class IMDbContent:
    """Data model representing an IMDb Movie or TV Show."""
    title: str
    rating: float
    year: int
    category: str
    watched: bool = False


# MongoDB Connection String (Placeholder password for security)
MY_URI="mongodb+srv://oguzbatu2934_db_user:PASSWORD@cluster0.kejl8qw.mongodb.net/?appName=Cluster0"

MENU_OPTIONS = {
    "1": {
        "name": "Top 250 Movies",
        "url": "https://www.imdb.com/search/title/?groups=top_250&sort=user_rating,desc&count=250"
    },
    "2": {
        "name": "Top 250 TV Shows",
        "url": "https://www.imdb.com/search/title/?title_type=tv_series&groups"
               "=top_250&sort=user_rating,desc&count=250"
    },
    "3": {
        "name": "Most Popular Movies",
        "url": "https://www.imdb.com/chart/moviemeter/?ref_=chttvtp_nv_menu"
    }
}


def print_menu():
    """Displays the main menu options to the user."""
    print("\n" + "=" * 40)
    print("      IMDb SCRAPER PRO (FINAL)      ")
    print("=" * 40)
    print("1. Top 250 Movies")
    print("2. Top 250 TV Shows")
    print("3. Most Popular Movies")
    print("--- ALGORITHMS ---")
    print("4. Find Highest Rating")
    print("5. Mark a Movie as Watched")
    print("6. Show My Watched Movies")
    print("7. Remove from Watched List")
    print("Q. Exit")
    print("=" * 40)


def filter_by_rating(manager: MongoDBManager):
    """Filters movies in the database by a minimum rating."""
    try:
        min_rating = float(input("Minimum Rating: (e.g. 8.3): "))
        query = {"rating": {"$gte": min_rating}}
        results = list(manager.collection.find(query).sort("rating", -1))

        if results:
            print(f"\n Found {len(results)} items with minimum rating {min_rating}+:")
            for index, item in enumerate(results, 1):
                status = "Watched" if item.get("watched") else " "
                print(f"{index}. {item['title']} | {item['rating']} {status}")
        else:
            print("No items found above rating")
    except ValueError:
        print("Invalid Number entered.")


def select_movie_from_search(manager, action_text):
    """Searches for a movie and asks the user to select the correct one."""
    search_name = input(f"Enter name to search ({action_text}): ").strip()
    matches = list(manager.collection.find(
        {"title": {"$regex": search_name, "$options": "i"}}
    ).limit(10))

    if not matches:
        print("No matches found.")
        return None

    if len(matches) == 1:
        movie = matches[0]
        confirm = input(f"Did you mean '{movie['title']}' ({movie['year']})? (Y/N): ").upper()
        if confirm == "Y":
            return movie
        return None

    print(f"Found {len(matches)} matches. Please select one:")
    for index, match in enumerate(matches, 1):
        status = "Watched" if match.get("watched") else " "
        print(f"{index}. {match['title']} ({match['year']}) {status}")

    try:
        selection = int(input("👉 Select number (0 to cancel): "))
        if 1 <= selection <= len(matches):
            return matches[selection - 1]
    except ValueError:
        pass

    print("Selection cancelled.")
    return None


def mark_as_watched(manager):
    """Marks a selected movie as 'watched' in the database."""
    movie = select_movie_from_search(manager, "mark as watched")
    if movie:
        manager.collection.update_one(
            {"_id": movie["_id"]},
            {"$set": {"watched": True}}
        )
        print(f"Success! '{movie['title']}' has been marked as watched!")


def show_watched_list(manager: MongoDBManager):
    """Displays all movies marked as watched."""
    query = {"watched": True}
    results = list(manager.collection.find(query))
    if results:
        print(f"\nYour Watched List ({len(results)} items):")
        print("-" * 40)
        for index, item in enumerate(results, 1):
            print(f"{index}. {item['title']} | {item['rating']}")
        print("-" * 40)
    else:
        print("You haven't marked any movies as watched yet.")


def remove_from_watched_list(manager):
    """Removes the 'watched' status from a selected movie."""
    movie = select_movie_from_search(manager, "remove from watched")
    if movie:
        if movie.get("watched"):
            manager.collection.update_one(
                {"_id": movie["_id"]},
                {"$set": {"watched": False}}
            )
            print(f"Success! '{movie['title']}' removed from your watched list.")
        else:
            print(f"'{movie['title']}' was not in your watched list anyway.")


if __name__ == "__main__":
    # Parsing command line arguments
    parser = argparse.ArgumentParser(description="IMDb Scraper with Selenium")
    parser.add_argument("--headless", action="store_true", help="Run browser in background")
    args = parser.parse_args()

    db_manager = MongoDBManager(MY_URI, "IMDb_Archive", "Allcontent")

    try:
        if db_manager.connect():
            while True:
                print_menu()
                choice = input("Choice: ").strip().upper()

                if choice == 'Q':
                    print("Exiting...")
                    break

                if choice in MENU_OPTIONS:
                    target = MENU_OPTIONS[choice]
                    try:
                        count_input = input(f"Count for '{target['name']}' (Max 250+): ")
                        LIMIT = int(count_input)
                    except ValueError:
                        LIMIT = 25

                    print(f"\n🚀 Starting Selenium Scraper for {target['name']} ...")

                    # Initialize scraper inside the loop for a fresh session
                    scraper = IMDbScraper(headless=args.headless)

                    try:
                        scraped_data = scraper.scrape_data(target['url'], LIMIT)

                        if scraped_data:
                            print(f"{len(scraped_data)} items found, saving...")
                            for i, data_item in enumerate(scraped_data, 1):
                                content = IMDbContent(
                                    title=data_item["title"],
                                    rating=data_item["rating"],
                                    year=data_item["year"],
                                    category=target["name"]
                                )
                                db_manager.insert_data(asdict(content), i)
                            print("Completed.")
                        else:
                            print("No data inserted.")

                    except Exception as e:  # pylint: disable=broad-except
                        print(f"Error during scraping process: {e}")

                    finally:
                        scraper.close()
                        print("Browser closed.")

                    input("\nPress Enter to continue...")

                elif choice == '4':
                    filter_by_rating(db_manager)
                    input("\nPress Enter to continue...")
                elif choice == '5':
                    mark_as_watched(db_manager)
                    input("\nPress Enter to continue...")
                elif choice == '6':
                    show_watched_list(db_manager)
                    input("\nPress Enter to continue...")
                elif choice == '7':
                    remove_from_watched_list(db_manager)
                    input("\nPress Enter to continue...")
                else:
                    print("Invalid choice.")

    except KeyboardInterrupt:
        print("\nExiting program...")
