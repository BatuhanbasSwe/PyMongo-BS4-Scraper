# 🎬 IMDb Scraper with Selenium

A robust Python automation script designed to scrape movie, TV show, and rating data from [IMDb](https://www.imdb.com/) using **Selenium WebDriver**. This project simulates real user behavior to navigate pages and extract structured data for analysis.

## 🌟 Key Features

* **Browser Automation:** Uses Selenium to control a real Chrome browser instance.
* **Dynamic Content Handling:** Capable of scraping data that renders via JavaScript (unlike BeautifulSoup).
* **Data Extraction:** Targets specific elements like Movie Titles, Release Dates, Ratings, and Descriptions.
* **Scalable:** Can be modified to loop through multiple pages or lists (e.g., Top 250).

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on your machine:

1.  **Python 3.7+**: [Download Python](https://www.python.org/downloads/)
2.  **Google Chrome Browser**: The script requires a standard Chrome installation.
3.  **ChromeDriver**: A separate executable that allows Selenium to control Chrome.
    * *Note:* The version of ChromeDriver **must match** your installed Chrome version.
    * [Download ChromeDriver Here](https://chromedriver.chromium.org/downloads)

---

## 📥 Installation & Setup

Follow these steps to set up the project locally in an isolated environment.

### 1. Clone the Repository
Download the project to your local machine:
```bash
git clone https://github.com/BatuhanbasSwe/IMDBScraperwSelenium.git
cd IMDBScraperwSelenium
```

### 2. Create a Virtual Environment (Recommended)
It is best practice to use a virtual environment to manage dependencies and avoid conflicts.

On Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

On macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

(You will see `(venv)` appear at the start of your terminal line indicating it is active.)

### 3. Install Dependencies
Install the required Python libraries inside your virtual environment:
```bash
pip install selenium
```

### 4. Driver Setup
Ensure the chromedriver.exe (Windows) or chromedriver (Mac/Linux) file is either:

* Placed directly inside this project folder.
* OR added to your system's PATH variables.

---

## 🚀 Usage

Once the setup is complete, you can run the scraper.

1. **Open the Script:** Open the main Python file (e.g., `main.py` or `scraper.py`) in your code editor.
2. **Configuration (Optional):** If the script targets a specific URL, you can modify the `url` variable inside the code to change the target page.
3. **Run the Script:** Execute the following command in your terminal:
```bash
python main.py
```

---

## 🧠 How It Works (Logic)

1. **Initialization:** The script initializes the Selenium WebDriver and launches a Chrome window.
2. **Navigation:** It directs the browser to the specified IMDb URL.
3. **Element Location:** Using XPath or CSS Selectors, the script locates specific HTML elements (e.g., `<td class="titleColumn">` for movie titles).
4. **Extraction:** It iterates through the found elements, cleans the text data (removing newlines or extra spaces), and stores it in a list or dictionary.
5. **Output:** Finally, the data is printed to the console or saved to a file (CSV/TXT), and the browser closes automatically.

---

## ⚠️ Troubleshooting

* **SessionNotCreatedException:** ChromeDriver version not compatible with your Chrome Browser version. Update ChromeDriver.
* **NoSuchElementException:** IMDb may have updated their website structure (HTML/CSS classes). Inspect the page and update the XPath/CSS selectors in the code.
* **Browser closes immediately:** Usually happens if the script finishes execution or crashes. Run via terminal to see the error log.

---

## ⚖️ Disclaimer

This tool is created for educational purposes only.

Please respect IMDb's robots.txt and Conditions of Use.

Avoid sending too many requests in a short period to prevent your IP from being blocked.

---
