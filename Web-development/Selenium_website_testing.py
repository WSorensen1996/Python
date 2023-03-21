from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as expect
from time import sleep
from random import randrange


driver = webdriver.Chrome()
driver.get("http://127.0.0.1:5000")

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

def find_and_click(method, link):
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((method, link)))
        element.click()
        return True
    except: 
        print("Not succesful:", link)
        tearDown()
        return False




def fill_form_by_name(method, link, value): 
    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((method, link)))
        element.click()
        
        element.send_keys(value)
        return True
    except: 
        print("Not succesful:", link, value )
        tearDown()
        return False

#assert find_and_click("Home") # Some error!

def test_search_in_python_org():
    random = randrange(10000)

    try: 
        #Test all links
        texts = ["Get in touch", "All projects", "About me", "Contact me", "Logout"]
        assert all(find_and_click(By.LINK_TEXT, x) for x in texts), back()

        #Get form
        driver.get("http://127.0.0.1:5000/register")

        #fill reg. form
        assert fill_form_by_name(By.NAME, "username", f"{random}teser@tester.com")
        assert fill_form_by_name(By.NAME, "password", f"{random}tester123")
        find_and_click(By.NAME, "submit")
        assert (driver.current_url == "http://127.0.0.1:5000/login") 

        #fill form
        assert fill_form_by_name(By.NAME, "nm", f"{random}teser@tester.com")
        assert fill_form_by_name(By.NAME, "psw", f"{random}tester123")
        assert find_and_click(By.XPATH,"/html/body/div/form/button")

        #Check if user was in session and logout
        driver.get("http://127.0.0.1:5000/")
        assert find_and_click(By.LINK_TEXT,"Contact me")
        assert (driver.current_url == "http://127.0.0.1:5000/contact") , back()
        assert find_and_click(By.LINK_TEXT,"Logout"), back()

        return True
    except: 
        print("Something happend - an error has occurred ")
        tearDown()
        return False




if __name__ == "__main__":
    try:
        assert test_search_in_python_org()
        tearDown()
        print("Testing status: SUCCES! ")
    except: 
        print("Testing status: FAILED! ")


