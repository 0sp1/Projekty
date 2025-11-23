import time
import csv
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

TARGET_POINTS = 170  
MIN_DELAY = 2        
MAX_DELAY = 6        

FAIL_LIMIT = 5       # ← Feature #5
COOLDOWN_TIME = 60   # seconds

LOG_FILE = "search_log.csv"   # ← Feature #7

service = Service("C:/path/to/msedgedriver.exe")
driver = webdriver.Edge(service=service)

first_words = [
    "Surface", "Xbox", "Windows", "Microsoft", "Azure",
    "Power", "Visual", "Cloud", "AI", "Security",
    "Enterprise", "Developer", "Business", "Edge", "Teams",
    "Dynamics", "Office", "Server", "Data", "Quantum",
    "HoloLens", "Copilot", "Fabric", "Graph", "OneDrive",
    "Intune", "Defender", "Synapse"
]

second_words = [
    "Laptop", "SeriesX", "Win11", "Office", "Cloud",
    "Tools", "Games", "Solutions", "Devices", "Support",
    "Analytics", "Platform", "Management", "Center", "Software",
    "Console", "Apps", "Integrations", "Compute", "Hardware",
    "Security", "Services", "Networking", "Storage", "Automation",
    "Insights", "Monitoring", "Workspace"
]

def init_csv():
    try:
        with open(LOG_FILE, "x", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "search_term", "points_before", "points_after"])
    except FileExistsError:
        pass  # Already exists

init_csv()

def log_search(term, before, after):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            term,
            before,
            after
        ])

def find_search_box(max_wait=10):
    for attempt in range(max_wait):
        try:
            return driver.find_element(By.NAME, "q")
        except NoSuchElementException:
            time.sleep(1)
    return None

def get_current_points():
    driver.get("https://rewards.bing.com/")
    time.sleep(4)
    try:
        points_element = driver.find_element(By.ID, "userPoints")
        return int(points_element.text.replace(",", ""))
    except:
        return None

fail_count = 0

while True:
    points_before = get_current_points()

    if points_before is None:
        print("Unable to read points, continuing anyway.")
    else:
        print(f"Current Microsoft Rewards points: {points_before}")
        if points_before >= TARGET_POINTS:
            print("Target points reached. Stopping.")
            break

    # Generate search term
    word1 = random.choice(first_words)
    word2 = random.choice(second_words)
    combined_search = f"{word1} {word2}"

    print(f"Searching for: {combined_search}")

    driver.get("https://www.bing.com")
    time.sleep(2)

    search_box = find_search_box()

    if search_box is None:
        print("Search box not found — failure.")
        fail_count += 1
    else:
        try:
            search_box.clear()
            search_box.send_keys(combined_search)
            search_box.submit()

            delay = random.uniform(MIN_DELAY, MAX_DELAY)
            print(f"Waiting {delay:.2f} seconds...")
            time.sleep(delay)

            fail_count = 0  # Reset failures on success

            # Log after search
            points_after = get_current_points()
            log_search(combined_search, points_before, points_after)

        except Exception as e:
            print("Error during search:", e)
            fail_count += 1

    # Failure protection
    if fail_count >= FAIL_LIMIT:
        print(f" Too many failures ({fail_count}). Cooling down for {COOLDOWN_TIME} seconds...")
        time.sleep(COOLDOWN_TIME)
        fail_count = 0

print("Finished.")
driver.quit()
