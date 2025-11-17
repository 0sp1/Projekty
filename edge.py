import time
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

service = Service("C:/path/to/msedgedriver.exe")
driver = webdriver.Edge(service=service)

words = ["Surface Laptop", "Xbox Series X", "Windows 11", "Microsoft Office", "Azure Cloud"]

while True:  
    random_word = random.choice(words)
    print("Searching for:", random_word)

    driver.get("https://www.microsoft.com")
    time.sleep(2) 

    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(random_word)

    search_box.submit()

    time.sleep(5)  
