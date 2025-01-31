# Import the necessary modules from Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Added import for Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC



options = Options()
options.page_load_strategy = 'eager'

tmx_file = open("tmx_ids.txt", "r")
tmx_ids = []

for line in tmx_file:
    tmx_ids.append(line.removesuffix("\n"))

tmx_file.close()

good_maps = []

id_num = 0
while id_num < len(tmx_ids):
    driver = webdriver.Firefox()

    for i in range(25):
        print(tmx_ids[id_num])
        while True:
            try:
                driver.get(f"https://tmnf.exchange/trackshow/{tmx_ids[id_num]}")
                print("Loading...")
            except:
                driver.get("https://www.google.com/")
                print("Refreshing...")
            else:
                break
        
        while True:
            try:
                author_time = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//td[@template='trackmedals']")))
                print("Trying...")
            except:
                print("Waiting...")
            else:
                print("Worked")
                break
        

        at = int(author_time.get_attribute("template-data").split(",")[0].split(":")[1])
        print(at)
        if at > 9000:
            good_maps.append(f"{tmx_ids[id_num]}\n")
            print("Added")
        else:
            print("Not added")
        print()
        if id_num < len(tmx_ids)-1:
            id_num += 1
        else:
            break
    
    driver.quit()
    if id_num >= len(tmx_ids)-1:
        break

maps_added = open("maps_to_play.txt", "w")

for i in good_maps:
    maps_added.write(i)

maps_added.close()