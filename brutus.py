import os
import urllib
import csv
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

load_dotenv(find_dotenv())
driver = webdriver.Firefox(executable_path=os.environ['WEBDRIVER_PATH'])

wait = WebDriverWait(driver, 10, 1.0)
timeout = 10000

'''
WAITING SELECTORS
'''
def cond1(driver):
    return driver.execute_script("""
    var option = document.querySelector("#identifierId");
    if (option==null) return false;
    return option.value !== "0";
    """)

def cond2(driver):
    return driver.execute_script("""
    var option = document.querySelector("#passwordNext");
    if (option==null) return false;
    return option.value !== "0";
    """)

def cond3(driver):
    return driver.execute_script("""
    var option = document.querySelector("div[data-test=header-account-name]");
    if (option==null) return false;
    return option.value !== "0";
    """)

'''
THE ACTUAL STUFF
'''
def googleLogin(driver):
    #login button + modal
    driver.find_element_by_xpath("//button[@value='login']").click()
    driver.find_element_by_class_name('th-modal-btn__google').click()
    #login oauth page
    wait.until(cond1)
    driver.find_element(By.ID, 'identifierId').send_keys('brutusckz54@gmail.com')
    driver.find_element(By.ID, 'identifierNext').click()
    wait.until(cond2)
    driver.find_element_by_xpath("//div[@id='password']//input").send_keys('Chicago110')
    driver.find_element(By.ID, 'passwordNext').click()



def crawlTrails(driver):
    trails=driver.find_elements_by_tag_name("article")
        
    with open('trails.csv', 'w', newline='') as csvfile:
        csvprint = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
        for trail in trails:

            trail_title=trail.find_element_by_xpath(".//a").get_attribute("title")
            trail_description=trail.find_element_by_class_name("tile-description").text
            trail_url=trail.find_element_by_xpath(".//a").get_attribute("href")
            trail_duration=trail.find_element_by_class_name("progress-text").text
            trail_units=trail.find_element_by_class_name("th-button--popover-trigger").text
            units_extra=len(trail_units)-11
            csvprint.writerow([trail_title,trail_url,trail_description,trail_units[:units_extra],trail_duration])


def goToTrails(driver):
    url = os.environ['TRAILHEAD_MODULES']
    driver.get(url)
    #googleLogin(driver)
    #wait.until(cond3)
    crawlTrails(driver)

goToTrails(driver)