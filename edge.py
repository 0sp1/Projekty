import time
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

TARGET_POINTS = 170  
MIN_DELAY = 2        
MAX_DELAY = 6        

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
        points = int(points_element.text.replace(",", ""))
        return points
    except:
        return None

while True:
    current_points = get_current_points()
    if current_points is None:
        print("Unable to read points, continuing anyway.")
    else:
        print(f"Current Microsoft Rewards points: {current_points}")
        if current_points >= TARGET_POINTS:
            print("Target points reached. Stopping.")
            break

    word1 = random.choice(first_words)
    word2 = random.choice(second_words)
    combined_search = f"{word1} {word2}"

    print(f"Searching for: {combined_search}")

    driver.get("https://www.bing.com")
    time.sleep(2)

    search_box = find_search_box()

    if search_box is None:
        print("Search box not found — skipping this search.")
        continue

    search_box.clear()
    search_box.send_keys(combined_search)
    search_box.submit()

    delay = random.uniform(MIN_DELAY, MAX_DELAY)
    print(f"Waiting {delay:.2f} seconds...")
    time.sleep(delay)

print("Finished.")
driver.quit()
