# Import the necessary modules from Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Added import for Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

uid_file = open("id_map.txt", "r")

uids = []

for line in uid_file:
    uids.append([line.split(',')[0], line.split(',')[1].strip()])
uid_file.close()

data = []

driver = webdriver.Firefox()

count = 0

for id in uids:
    driver.get(f"https://www.xaseco.org/uidfinder.php?uid={id[0]}")
    dedi_exists = (len(driver.find_elements(By.CLASS_NAME, "error")) == 0)
    info_table = driver.find_element(By.ID, "uidfinder")
    tmx_name = info_table.find_element(By.XPATH, ".//tr[5]/td[2]").get_attribute('innerHTML')
    if dedi_exists:
        dedi_name = info_table.find_element(By.XPATH, ".//tr[13]/td[2]").get_attribute('innerHTML')
    else:
        dedi_name = "N/A"
    data.append([id[0], id[1], tmx_name, dedi_name, tmx_name.lower()])
    count += 1
    print(f"{round(100*count / 903, 2)}%")

driver.quit()

data.sort(key=lambda x: x[4])

track_info_file = open("track_info_map_obsolete.txt", "w", encoding="UTF-8")
for track in data:
    track_info_file.write(f"{track[0]}@{track[1]}@{track[2]}@{track[3]}@{track[4]}\n")
track_info_file.close()
