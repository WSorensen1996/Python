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
import pandas 



url = "https://www.youtube.com/c/TechWithTim/videos?view=0&sort=p&flow=grid"

driver = webdriver.Chrome()
driver.get(url)


def tearDown():
    driver.close()

def back(): 
    try: 
        driver.execute_script("window.history.go(-1)")
        return True
    except: 
        print("Back error")
        tearDown()
        return False

def find(method, link, elm = driver):
    try:
        wait = WebDriverWait(elm, 10)
        element = wait.until(EC.presence_of_element_located((method, link)))
        return element
    except: 
        print("Not succesful:", link)
        tearDown()
        return None


def scrape(): 
    print("scraping")
    videos = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'style-scope ytd-grid-video-renderer')))

    for video in videos: 
        title = find( By.XPATH, './/*[@id="video-title"]',video)
        views = find( By.XPATH, './/*[@id="metadata-line"]/span[1]',video)
        age =  find( By.XPATH, './/*[@id="metadata-line"]/span[2]',video)

        

        print("\n"+title.text)
        print(views.text)
        print(age.text)

if __name__== "__main__": 
    find(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div/div/button/span').click()

    
    scrape()