# Import the necessary modules from Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Added import for Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.page_load_strategy = 'none'

tmx_id_file = open("maps_to_play.txt", "r")
tmx_ids = []
for line in tmx_id_file:
    tmx_ids.append(line.strip())
tmx_id_file.close()

id_pair = []

driver = webdriver.Firefox()

for id in tmx_ids:
    driver.get(f"https://tmnf.exchange/trackshow/{id}")
    dedi_id = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//a[text()='View on Dedimania']"))).get_attribute("href").split("=")[3].split("&")[0]
    id_pair.append([dedi_id, id])

driver.quit()

id_map_file = open("id_map.txt", "w")

for i in id_pair:
    id_map_file.write(f"{i[0]},{i[1]}\n")

id_map_file.close()