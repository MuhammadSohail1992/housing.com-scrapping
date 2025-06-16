from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://housing.com/in/buy/hyderabad/hyderabad")
# driver.get("https://housing.com/in/buy/hyderabad/hyderabad?page=7")
time.sleep(8)

# Scroll to bottom to load more listings
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

# Get all listing containers
cards = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='card-container']")

properties = []

for card in cards:
    try:
        title = card.find_element(By.CSS_SELECTOR, ".title-style").text
    except:
        title = ""

    try:
        subtitle = card.find_element(By.CSS_SELECTOR, ".subtitle-style").text
        location = subtitle.split("in")[-1].strip()
        city = location.split(",")[-1].strip()
    except:
        location = city = ""

    try:
        price_range = card.find_element(By.CSS_SELECTOR, ".T_blackText").text
        if " - " in price_range:
            price_min, price_max = [x.strip() for x in price_range.split(" - ")]
        else:
            price_min = price_max = price_range
    except:
        price_min = price_max = ""

    try:
        config = card.find_element(By.CSS_SELECTOR, ".T_configurationStyle").text
    except:
        config = ""

    try:
        avg_price = card.find_element(By.CSS_SELECTOR, "[data-q='property-detail']").text
        avg_price = avg_price.split("•")[0].replace("Avg. Price:", "").strip()
    except:
        avg_price = ""

    properties.append({
        "title": title,
        "city": city,
        "location": location,
        "price_min": price_min,
        "price_max": price_max,
        "configuration": config,
        "average_price": avg_price
    })

driver.quit()

# Save to CSV
if properties:
    with open("housing_final.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=properties[0].keys())
        writer.writeheader()
        writer.writerows(properties)
    print(f"✅ Done: {len(properties)} listings saved to housing_final.csv")
else:
    print("❌ No data found.")
