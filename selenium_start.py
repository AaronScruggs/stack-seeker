import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *

myProxy = '119.237.211.19'
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", myProxy)
profile.set_preference("network.proxy.http_port", 3128)
profile.update_preferences()
driver = webdriver.Firefox(firefox_profile=profile)


def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver

def lookup(driver, query):
    driver.get("http://www.mmaapi.com")
    try:
        box = driver.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "navbar")))
        link = driver.find_element_by_link_text('Data Explorer')


        button = driver.wait.until(EC.element_to_be_clickable(
            (By.NAME, "btnK")))
        box.send_keys(query)
        button.click()
    except TimeoutException:
        print("Box or Button not found in google.com")



















