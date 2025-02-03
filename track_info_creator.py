# Import the necessary modules from Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Added import for Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

uid_file = open("id_map.txt", "r")

uids = []

special_maps = {
    "yHd__BBIVFpUEd8GjgZXGruWbf7": "De large & MG",
    "c7SLRA8a1NwwtbtWx9YOauQOnB6": "Evitaerc<--",
    "7nRzTzo7TdH0UNGYuWONe0u8yug": "ï»¿Î Ä¬Å„ã‚§ÏÑ³Ä½Î”Ð¸D",
    "1_iw6NIPnijIyvmin3N57y7Qffa": "¿Klub PrzyjaciÃ³Å, Myszki Miki",
    "css_Vu0kevU25LnCGqgi9_dZvxe": "ï»¿paÅ‚ka teleskopowa",
    "W50syMUoXiZtKZ2fQLa5HVVl6W": "ï»¿to byÅ‚ niebezpieczny czubek",
    "qVWCOja5AhHozZgUOnMo5Vexgl3": "ï»¿zupa z maÅ‚py",
    "wafA7PE6KIUa4NXJW27vip9tWoe": "ï»¿Å‚x"
}

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
    if id[0] in special_maps.keys():
        tmx_name = special_maps[id[0]]
    else:
        tmx_name = info_table.find_element(By.XPATH, ".//tr[5]/td[2]").get_attribute('innerHTML').lstrip()
    if dedi_exists:
        if id[0] == "yHd__BBIVFpUEd8GjgZXGruWbf7" or id[0] == "c7SLRA8a1NwwtbtWx9YOauQOnB6":
            dedi_name = special_maps[id[0]]
        else:
            dedi_name = info_table.find_element(By.XPATH, ".//tr[13]/td[2]").get_attribute('innerHTML')
    else:
        dedi_name = "N/A"
    data.append([id[0], id[1], tmx_name, dedi_name, tmx_name.lower()])
    count += 1
    print(f"{round(100*count / 903, 2)}%")

driver.quit()

data.sort(key=lambda x: x[4])

track_info_file = open("track_info_map.txt", "w", encoding="UTF-8")
for track in data:
    track_info_file.write(f"{track[0]}@{track[1]}@{track[2]}@{track[3]}@{track[4]}\n")
track_info_file.close()
