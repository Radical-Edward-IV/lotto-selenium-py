#!/usr/bin/env python
# coding: utf-8

# In[40]:


import time
import logging
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

###############################
# Logging
###############################
now = time.localtime()
file_name = "/Users/edward/Projects/Python/selenium/log/lotto_%04d%02d%02d.log" %(now.tm_year, now.tm_mon, now.tm_min)
logging.basicConfig(filename=file_name, encoding='utf-8', level=logging.DEBUG)

###############################
# Classes
###############################
class Ball:
    def __init__(self, n, w):
        self.number = n
        self.weight = w

###############################
# Functions
###############################
# Common
def wait_and_click(driver, xpath):
    element = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, xpath))
    ).click()

def close_pop_ups(main_window):
    new_popup = WebDriverWait(driver, 3).until(ec.new_window_is_opened(main_window))
    windows = driver.window_handles
    for w in windows:
        if w != main_window[0]:
            driver.switch_to.window(w)
            driver.close()
            driver.switch_to.window(main_window[0])

# Lotto
def get_num_arr(balls, total_weight):
    result = []
    while result.__len__() != 6:
        r = random.random()
        for b in balls:
            r -= b.weight
            if r < 0 and b not in result:
                result.append(b)
                break
    return result

###############################
# Driver Options Settings
###############################
options = Options()
options.add_argument("headless")
options.add_argument("--disable-loging")
options.add_argument("--blink-settings=imagesEnabled=false") # Unloading Images

##############################
# Account Info
##############################
USER_ID = ""
USER_PW = ""

##############################
# Create Session
##############################
driver = webdriver.Chrome(options)
driver.get("https://dhlottery.co.kr/user.do?method=login&returnUrl=")
main_window = driver.window_handles
logging.debug("[Main window name is %s..;]" %main_window)
print("[Main window name is %s..;]" %main_window)
print("[Create Session Completed..;]")

##############################
# Login Process
##############################
user_id = "/html/body/div[3]/section/div/div[2]/div/form/div/div[1]/fieldset/div[1]/input[1]"
user_pw = "/html/body/div[3]/section/div/div[2]/div/form/div/div[1]/fieldset/div[1]/input[2]"
wait_and_click(driver, user_id)
driver.find_element(By.XPATH, user_id).send_keys(USER_ID)
driver.find_element(By.XPATH, user_pw).send_keys(USER_PW, Keys.ENTER)
print("[Login Completed..;]")
# Close Pop-ups
close_pop_ups(main_window)

##############################
# Select Numbers
##############################
driver.get("https://dhlottery.co.kr/gameResult.do?method=statByNumber")
weights = driver.find_elements(By.XPATH, "//*[@id='printTarget']/tbody/tr/td[3]")
balls = []
total_weight = 0
for i in range(0, 45):
    w = int(weights[i].text)
    balls.append(Ball(i + 1, w))
    total_weight += w

for b in balls:
    b.weight = b.weight / total_weight

##############################
# Buy 6/45 Lotto
##############################
wait_and_click(driver, "//*[@id=\"gnb\"]/ul/li[1]/a")
driver.find_element(By.XPATH, "//*[@id=\"gnb\"]/ul/li[1]/div/ul/li[1]/a").click()

# Switch Window
time.sleep(3)
windows = driver.window_handles

for w in windows:
    if w != main_window[0]: driver.switch_to.window(w)
try:
    driver.switch_to.frame("ifrm_tab")
    
    # Execute Script
    script = ""
    for i in range(0, 5):
        selected_balls = get_num_arr(balls, total_weight)
        for ball in selected_balls:
            script += " $('#check645num%s').click();\n " %ball.number
        script += " $('#btnSelectNum').click();\n "
    script += " $('#btnBuy').click();\n "
    driver.execute_script(script)
    wait_and_click(driver, "/html/body/div[4]/div/div[2]/input[1]")
    print("[Complete All tasks]")
    driver.quit()
except:
    print("[Failure due to exception]")
    driver.quit()

