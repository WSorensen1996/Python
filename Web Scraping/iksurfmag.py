link = "https://www.iksurfmag.com/awards/readers-awards-2021/best-kitesurfing-vlogger-of-2021/"

mikkel = '//*[@id="PDI_answer50580828"]'

from cmath import exp
from os import EX_OK
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import urllib 
import requests
import urllib.request
from time import sleep
import random

def open(): 
    driver = webdriver.Chrome()
    driver.get(link)
    return driver

def tearDown(driver):
    driver.close()

def back(driver): 
    try: 
        driver.execute_script("window.history.go(-1)")
        return True
    except: 
        print("Back error")
        tearDown()
        return False

def find(driver, method, link):
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((method, link)))
        return element
    except: 
        print("Not succesful:", link)
        tearDown()
        return None


def vote(driver): 
    print("voting")
    find(driver, By.XPATH, mikkel).click()
    find(driver, By.XPATH, '//*[@id="pd-vote-button11009014"]/span').click()
    sleep(2)
    tearDown(driver)

if __name__== "__main__": 
    for i in range (5): 
        print(f"Voted {i} times")
        vote(open())


