# Import the necessary modules from Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Added import for Keys



def prep():
    # Create a webdriver object. Here we use Firefox, but you can choose other browsers like Chrome, Edge, etc.
    

    # Maximize the browser window
    driver.maximize_window()

    challenges_button = driver.find_element(By.XPATH, "//*[text()='Challenges']")

    challenges_button.click()

    change_map_order = driver.find_element(By.NAME, "MapOrder")
    change_map_order.click()

    asc_alp = driver.find_element(By.XPATH, "//*[text()='Challenge (Asc)']")
    asc_alp.click()

    # Locate the search icon element using XPath
    author_input = driver.find_element(By.NAME, "Author")

    # Click on the Search Icon to activate the search field
    author_input.send_keys("dziwnystan")

    # Locate the input field for search text using XPath
    submit = driver.find_elements(By.XPATH, "//*[@type='submit']")[0]

    # Enter the search query "Data Structure" into the input field
    submit.click()

    limit_input = driver.find_element(By.NAME, "Limit")

    limit_input.clear()
    limit_input.send_keys("100")

    submit = driver.find_elements(By.XPATH, "//*[@type='submit']")[1]
    submit.click()

def per_page(maps):
    temp_maps = maps.copy()
    info_table = driver.find_elements(By.XPATH, "//table[@class='tabl'][2]//tr")
    for i in info_table:
        if i.get_attribute("bgcolor") == "#FFFFFF" or i.get_attribute("bgcolor") == "#F0F0F0":
            map_name = i.find_element(By.XPATH, "./td[3]/a")
            map_id = i.find_element(By.XPATH, "./td[10]")
            temp_maps.append([map_name.get_attribute("innerHTML"), map_id.get_attribute("innerHTML")])
    return temp_maps

def next_page(cur_start):
    start_input = driver.find_element(By.NAME, "Start")
    start_input.clear()
    start_input.send_keys(f"{cur_start + 100}")
    submit = driver.find_elements(By.XPATH, "//*[@type='submit']")[1]
    submit.click()
    return cur_start + 100


maps = []
driver = webdriver.Firefox()

# Navigate to the GeeksforGeeks website
driver.get("http://dedimania.net/tmstats/?do=stat")

prep()
start_num = 1

for i in range(7):
    maps = per_page(maps)
    start_num = next_page(start_num)
maps = per_page(maps)

map_details = open("map_details.txt", "w", encoding="utf-8")

for map in maps:
    map_details.write(f"{map[0]}@{map[1]}\n")

map_details.close()

