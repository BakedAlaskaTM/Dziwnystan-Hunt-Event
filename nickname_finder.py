# Import the necessary modules from Selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Added import for Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()

driver.get("http://dedimania.net/tmstats/?do=stat")

driver.find_element(By.XPATH, "//option[text()='Players']").click()

login_file = open("players.txt", "r")

logins = []

for line in login_file:
    logins.append(line.strip())

for login in logins:
    login_field = driver.find_element(By.NAME, "Login")
    login_field.clear()
    login_field.send_keys(f"{login}")
    submit = driver.find_elements(By.XPATH, "//*[@type='submit']")[0].click()
    info_table = driver.find_elements(By.XPATH, "//table[@class='tabl'][2]//tr")
    print(info_table[3].find_element(By.XPATH, "./td[6]/a").get_attribute("innerHTML"))

driver.quit()