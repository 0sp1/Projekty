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
FAIL_LIMIT = 5
COOLDOWN_TIME = 60
MAX_SEARCHES_PER_SESSION = 40
NO_GAIN_LIMIT = 5
LOG_FILE = "search_log.csv"

service = Service("C:/path/to/msedgedriver.exe")
driver = webdriver.Edge(service=service)

first_words = [
    "Surface","Xbox","Windows","Microsoft","Azure","Power","Visual","Cloud","AI",
    "Security","Enterprise","Developer","Business","Edge","Teams","Dynamics",
    "Office","Server","Data","Quantum","HoloLens","Copilot","Fabric","Graph",
    "OneDrive","Intune","Defender","Synapse"
]

second_words = [
    "Laptop","SeriesX","Win11","Office","Cloud","Tools","Games","Solutions",
    "Devices","Support","Analytics","Platform","Management","Center","Software",
    "Console","Apps","Integrations","Compute","Hardware","Security","Services",
    "Networking","Storage","Automation","Insights","Monitoring","Workspace"
]

def init_csv():
    try:
        with open(LOG_FILE, "x", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp","search_term","points_before","points_after"])
    except FileExistsError:
        pass

def load_used_terms():
    terms = set()
    try:
        with open(LOG_FILE, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) > 1:
                    terms.add(row[1])
    except FileNotFoundError:
        pass
    return terms

def log_search(term, before, after):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), term, before, after])

def find_search_box(max_wait=10):
    for _ in range(max_wait):
        try:
            return driver.find_element(By.NAME, "q")
        except NoSuchElementException:
            time.sleep(1)
    return None

def get_current_points():
    driver.get("https://rewards.bing.com/")
    time.sleep(4)
    try:
        el = driver.find_element(By.ID, "userPoints")
        return int(el.text.replace(",", ""))
    except:
        return None

init_csv()
used_terms = load_used_terms()

fail_count = 0
search_count = 0
no_gain_count = 0

while True:
    points_before = get_current_points()
    if points_before is not None and points_before >= TARGET_POINTS:
        break
    if search_count >= MAX_SEARCHES_PER_SESSION:
        break
    if no_gain_count >= NO_GAIN_LIMIT:
        break

    combined_search = None
    for _ in range(20):
        candidate = f"{random.choice(first_words)} {random.choice(second_words)}"
        if candidate not in used_terms:
            combined_search = candidate
            used_terms.add(candidate)
            break

    if combined_search is None:
        break

    driver.get("https://www.bing.com")
    time.sleep(2)
    search_box = find_search_box()

    if search_box is None:
        fail_count += 1
    else:
        try:
            search_box.clear()
            search_box.send_keys(combined_search)
            search_box.submit()
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            search_count += 1
            fail_count = 0
            points_after = get_current_points()
            if points_after == points_before:
                no_gain_count += 1
            else:
                no_gain_count = 0
            log_search(combined_search, points_before, points_after)
        except:
            fail_count += 1

    if fail_count >= FAIL_LIMIT:
        time.sleep(COOLDOWN_TIME)
        fail_count = 0

driver.quit()
