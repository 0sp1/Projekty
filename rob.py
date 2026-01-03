from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time

edge_options = Options()
edge_options.add_argument("--start-maximized")

service = Service("path/to/msedgedriver.exe")

driver = webdriver.Edge(service=service, options=edge_options)

driver.get("https://www.bing.com")

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("latest news about AI")
search_box.send_keys(Keys.RETURN)

time.sleep(5)

first_result = driver.find_element(By.CSS_SELECTOR, "li.b_algo h2")
print("Top result:", first_result.text)

driver.quit()
