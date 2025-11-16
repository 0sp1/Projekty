from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

service = Service("C:/path/to/msedgedriver.exe")

driver = webdriver.Edge(service=service)

driver.get("https://www.microsoft.com")

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("Surface Laptop")
search_box.submit()

