import time
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

service = Service("C:/path/to/msedgedriver.exe")
driver = webdriver.Edge(service=service)

first_words = [
    "Surface", "Xbox", "Windows", "Microsoft", "Azure",
    "Power", "Visual", "Cloud", "AI", "Security",
    "Enterprise", "Developer", "Business", "Edge", "Teams",
    "Dynamics", "Office", "Server", "Data", "Quantum"
]

second_words = [
    "Laptop", "Series X", "11", "Office Suite", "Cloud Services",
    "Tools", "Games", "Solutions", "Devices", "Support",
    "Analytics", "Platform", "Management", "Center", "Software",
    "Console", "Apps", "Integrations", "Compute", "Hardware"
]

for i in range(30):
    word1 = random.choice(first_words)
    word2 = random.choice(second_words)

    combined_search = f"{word1} {word2}"
    print(f"({i+1}/30) Searching for:", combined_search)

    driver.get("https://www.microsoft.com")
    time.sleep(2)

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(combined_search)

    search_box.submit()

    time.sleep(5) 

print("Finished 30 searches.")
driver.quit()

