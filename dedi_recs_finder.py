# Import the necessary modules from Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Added import for Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import datetime
import math

options = Options()
options.page_load_strategy = "normal"

def time_to_string(time_secs):
    h = str(math.floor(time_secs / 3600))
    m = str(math.floor((time_secs - int(h)*3600) / 60))
    s = str(round(time_secs - int(h)*3600 - int(m)*60, 2)).split(".")
    if h != "0":
        return f"{h}:{m.zfill(2)}:{s[0].zfill(2)}.{s[1].ljust(2, '0')}"
    elif m != "0":
        return f"{m}:{s[0].zfill(2)}.{s[1].ljust(2, '0')}"
    else:
        return f"{s[0]}.{s[1].ljust(2, '0')}"

def time_converter(time_str):
    split_time = time_str.split(":")
    length = len(split_time)
    time_seconds = 0
    for i in range(length):
        time_seconds += float(split_time[(length-1)-i]) * (60**i)
    return time_seconds

def prep():
    # Create a webdriver object. Here we use Firefox, but you can choose other browsers like Chrome, Edge, etc.
    
    challenges_button = dedi_driver.find_element(By.XPATH, "//*[text()='Challenges']")

    challenges_button.click()

    show_recs = dedi_driver.find_element(By.NAME, "Show")
    show_recs.click()

    recs = dedi_driver.find_element(By.XPATH, "//option[text()='Records']")
    recs.click()
    submit = dedi_driver.find_elements(By.XPATH, "//*[@type='submit']")[1]
    submit.click()

def next_challenge(map_id):
    uid_field = dedi_driver.find_element(By.NAME, "Uid")
    uid_field.clear()
    uid_field.send_keys(f"{map_id}")
    
    submit = dedi_driver.find_elements(By.XPATH, "//*[@type='submit']")[0]

    submit.click()
    dedi_driver.find_elements(By.XPATH, "//option[text()='Rank (Asc)']")[1].click()

def read_recs(overall_stats, map, players):
    ml_wr = False
    stats = overall_stats.copy()
    data = []
    tmx_wr = tmx_wrs[map[1]]
    if tmx_wr[0] != "N/A":
        tmx_wr_name = tmx_wr[0]
        tmx_wr_time = tmx_wr[1]
    else:
        tmx_wr_name = ""
        tmx_wr_time = ""
    if maps[3] != "N/A":
        info_table = dedi_driver.find_elements(By.XPATH, "//table[@class='tabl'][2]//tr")
        for i in info_table:
            if i.get_attribute("bgcolor") == "#FFFFFF" or i.get_attribute("bgcolor") == "#F0F0F0":
                login = i.find_element(By.XPATH, "./td[4]/a")
                nickname = i.find_element(By.XPATH, "./td[5]/a")
                rank = i.find_element(By.XPATH, "./td[6]")
                time = i.find_element(By.XPATH, "./td[8]/a")
                data.append([login.get_attribute("innerHTML"), nickname.get_attribute("innerHTML"), rank.get_attribute("innerHTML"), time.get_attribute("innerHTML")])
                if str(rank.get_attribute("innerHTML")).strip() == '10':
                    break
        if len(data) > 0:
            if data[0][0] in players:
                if tmx_wr_time != "" and float(tmx_wr_time) > time_converter(data[0][3]):
                    ml_wr = True
    stats.append([map[2], data, ml_wr, map[3], tmx_wr_name, tmx_wr_time])
    return stats.copy()
    

overall_stats = []
players = []
player_file = open("players.txt", "r")
for line in player_file:
    players.append(line.strip())
player_file.close()

tmx_wrs = {}
tmx_wr_file = open("tmx_wrs.txt", "r")
for line in tmx_wr_file:
    tmx_wr_info = line.split("|#~%|")
    tmx_wrs[tmx_wr_info[0]] = [tmx_wr_info[1], tmx_wr_info[2].split("\n")[0]]
tmx_wr_file.close()

maps = []
map_details = open("track_info_map.txt", "r", encoding="UTF-8")
for line in map_details:
    info = line.split("@")
    maps.append([info[0], info[1], info[2], info[3], info[4].split("\n")[0]])
map_details.close()

dedi_driver = webdriver.Firefox()
dedi_driver.get("http://dedimania.net/tmstats/?do=stat")
prep()


num_processed = 0
total_num = len(maps)
for map in maps:
    next_challenge(map[0])
    time.sleep(0.3)
    overall_stats = read_recs(overall_stats, map, players)
    num_processed += 1
    print(f"{round(num_processed*100 / total_num, 1)}%")

dedi_driver.quit()


rows = []
for map_stats in overall_stats:
    row_1 = [map_stats[0]]
    row_2 = [""]
    count = 0
    for player in map_stats[1]:
        row_1.append(player[0])
        row_2.append(player[3])
        count += 1
    while count < 10:
        row_1.append("")
        row_2.append("")
        count += 1

    row_1.append(map_stats[4])
    row_2.append(time_to_string(float(map_stats[5])))
    row_1.append(map_stats[2])
    row_1.append(map_stats[3])
    rows.append(row_1)
    rows.append(row_2)
    rows.append([""])

with open(f'Logs/dedi_recs_{datetime.date.today()}.csv', 'w', newline='', encoding="UTF-8") as csvfile:
    writer = csv.writer(csvfile, delimiter="@")
    writer.writerows(rows)
    