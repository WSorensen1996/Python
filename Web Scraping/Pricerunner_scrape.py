from audioop import add
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

#Search for a subject 
subject = "Iphone".lower() 
currency = 'kr.'


option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(options=option)
driver.get(f"https://www.pricerunner.dk/results?q={subject}&suggestionsActive=true&suggestionClicked=false&suggestionReverted=false")

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


def find(method, link, driver = driver, all=0):
    try:
        if all==0: 
            return WebDriverWait(driver, 10).until(EC.presence_of_element_located((method, link)))
        if all==1: 
            return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((method, link)))
    except: 
        print("Not succesful:", link)
        tearDown(driver)
        return None

def scrape(): 
    #Close cookie accept! 
    find(By.XPATH, "//*[@id='consent']/div/div[2]/div[1]/div[2]/div/div/button[1]").click()

    product_txt = find(By.CLASS_NAME, 'VEHfYxE7Mb', all=1)[0].text
    product_list = []

    def word_search(start): 
        sub_found = product_txt.lower().find(subject,start) #iterstart
        if  sub_found!=-1: 
            curr_found = product_txt.lower().find(currency,sub_found) + len(currency) #iterstart
            if curr_found !=-1: 
                product = product_txt[sub_found:curr_found]
                product_list.append(product)
                word_search(curr_found)
    word_search(0)
    
    for product in product_list: 
        print("\n\n"+product)


if __name__== "__main__": 
    scrape()
    tearDown()

