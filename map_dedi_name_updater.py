# Import the necessary modules from Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Added import for Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

track_info_file = open("track_info_map.txt", "r", encoding="UTF-8")
track_info = []
for line in track_info_file:
    track_info.append(line.strip().split("@"))

track_info_file.close()

driver = webdriver.Firefox()
driver.get("http://dedimania.net/tmstats/?do=stat")
challenges_button = driver.find_element(By.XPATH, "//*[text()='Challenges']").click()

new_track_info = []

total = len(track_info)
count = 0
for map in track_info:
    updated_map_info = map.copy()
    success = True
    uid_field = driver.find_element(By.NAME, "Uid")
    uid_field.clear()
    uid_field.send_keys(map[0])
    
    submit = driver.find_elements(By.XPATH, "//*[@type='submit']")[0]

    submit.click()
    try:
        map_row = driver.find_element(By.XPATH, "//table[@class='tabl'][2]//tr[4]")
    except:
        success = False
    
    if success:
        if map_row.get_attribute("bgcolor") == "#FFFFFF":
            dedi_map_name = map_row.find_element(By.XPATH, "./td[3]/a").get_attribute("innerHTML")
            updated_map_info[3] = dedi_map_name
    new_track_info.append(updated_map_info)
    count += 1
    print(f"{round(count*100 / total, 1)}%")

driver.quit()

track_info_file = open("track_info_map.txt", "w", encoding="UTF-8")
for map in new_track_info:
    track_info_file.write(f"{map[0]}@{map[1]}@{map[2]}@{map[3]}@{map[4]}\n")

track_info_file.close()
    




