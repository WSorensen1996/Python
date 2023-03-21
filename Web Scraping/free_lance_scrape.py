from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time
import re 
from add_to_file import add_email_to_file

##########################################################################################
emails = []
##########################################################################################


def open(link, headless = 0): 
    if headless == 0: 
        driver = webdriver.Chrome()
        driver.get(link)
        return driver

    if headless == 1: 
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(options=option)
        driver.get(link)
        return driver

def tearDown(driver):
    driver.close()

def find(method, link, driver, all=0):
    try:
        if all==0: 
            return WebDriverWait(driver, 10).until(EC.presence_of_element_located((method, link)))
        if all==1: 
            return WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((method, link)))
    except: 
        print("Not succesful:", link)
        tearDown(driver)
        return None

def validate_email(email): 
    pattern = '^[a-z 0-9]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(pattern, email): 
        return True
    return False

def look_up_emails(src): 
    for line in src.splitlines(): 
        words = line.split()
        for word in words: 
            if word != []: 
                if word.find("@") != -1: 
                    if validate_email(word): 
                        emails.append(word)
                        print("E-mail appended: ", word)

def scrape_site(driver, email_field_class): 
    try: 
        email_fields = find(By.CLASS_NAME, email_field_class, driver, all = 0).text
        look_up_emails(email_fields)
        tearDown(driver)
    except: 
        print("Failed to process")
        tearDown(driver)

def bs4_scrape(link) -> None :
    src = requests.get(link).text
    soup = BeautifulSoup(src, 'lxml' )
    txt = soup.get_text()
    if txt is not None: 
        look_up_emails(txt)
    return

def scrape_hrefs(driver,link) -> None : 
    elems = find(By.TAG_NAME, 'a' ,driver, all=1)
    for elem in elems:
        href = elem.get_attribute('href')
        if href is not None and href.find(link[:10]) != -1: 
            bs4_scrape(href)
    tearDown(driver)
    return


if __name__ == "__main__": 
    now = time.time()

    email_field_classes = ["view-content"]
    scrape_sites = ["https://conssci.umn.edu/faculty"] 

    scrape_href_sites = ["https://ansci.umn.edu/graduate/graduate-faculty-directory" ]

    for index,link in enumerate(scrape_sites): 
        scrape_site(open(link,headless=1),email_field_classes[index])
    for link in scrape_href_sites: 
        scrape_hrefs(open(link,headless=1),link)

    add_email_to_file(emails)
    print(f"Took {time.time()-now}s and scraped {len(emails)} emails")
      





