# Import the necessary modules from Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Added import for Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import json

tmx_ids = []
id_map_file = open("track_info_map.txt", "r", encoding="UTF-8")
for line in id_map_file:
    tmx_ids.append(line.split("@")[1])
id_map_file.close()

driver = webdriver.Edge()

tmx_wrs = []

for id in tmx_ids:
    driver.get(f"https://tmnf.exchange/api/replays?trackId={id}&count=1&fields=ReplayTime%2CUser.Name")
    tmx_wr = driver.find_element(By.TAG_NAME, "pre").get_attribute("innerHTML")
    wr_dict = json.loads(tmx_wr)
    try:
        wr_time = str(round(int(wr_dict["Results"][0]['ReplayTime']) / 1000, 2))
        wr_name = wr_dict["Results"][0]['User']['Name']
    except:
        wr_time = "N/A"
        wr_name = "N/A"
    tmx_wrs.append([id, wr_name, wr_time])

driver.quit()

tmx_wr_file = open("tmx_wrs.txt", "w", encoding="UTF-8")

for wr in tmx_wrs:
    tmx_wr_file.write(f"{wr[0]}|#~%|{wr[1]}|#~%|{wr[2]}\n")

tmx_wr_file.close()