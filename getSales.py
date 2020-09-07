from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import datetime
import logging
import random
import time
import os


DIR_NAME = datetime.datetime.now().strftime("%B")
FILE_NAME = f"{datetime.datetime.now().day}.csv"
PASSWORD = "password"
EMAIL = "email"
   
def sleep_random():
    sl_time = random.uniform(1, 2.9)
    logging.info(f'Please wait: {sl_time} s')
    time.sleep(sl_time)

def save_csv(df):
    try:
        os.mkdir(f"tables/{DIR_NAME}")
    except OSError:
        logging.warning("The directory %s excist" % f"tables/{DIR_NAME}")
    else:
        logging.debug("Successfully created the directory %s " % f"tables/{DIR_NAME}")
    file_name = f"tables/{DIR_NAME}/{FILE_NAME}"
    df.to_csv(file_name, index=False)
    logging.debug('Saving.....')

def worker():
    # download browser
    browser = webdriver.Firefox()

    # open url
    browser.get("https://erank.com/")

    # get login
    browser.find_element_by_css_selector(".f-12").send_keys(Keys.ENTER)
    sleep_random()
    browser.find_element_by_css_selector("#signin-email").send_keys(EMAIL)
    sleep_random()
    browser.find_element_by_css_selector("#signin-password").send_keys(PASSWORD)
    sleep_random()
    browser.find_element_by_css_selector(".btn-md").send_keys(Keys.ENTER)
    try:
        sleep_random()
        browser.find_element_by_css_selector(".f-12").send_keys(Keys.ENTER)
        sleep_random()
        browser.find_element_by_css_selector("#signin-email").send_keys(EMAIL)
        sleep_random()
        browser.find_element_by_css_selector("#signin-password").send_keys(PASSWORD)
        sleep_random()
        browser.find_element_by_css_selector(".btn-md").send_keys(Keys.ENTER)
        # get table with sales yesterday
        
    except:
        print("Try again")
        pass
    sleep_random()
    sleep_random()
    
    browser.get("https://erank.com/top-sellers")
    try:
        logging.debug('Waiting for loading page')
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".container-p-l-0 h3"))
        )
        sleep_random()
    except Exception as e:
        logging.error(e)

    html = browser.page_source
    df = pd.read_html(html)[1]
    logging.info('Got table!!!!')
    # save csv
    save_csv(df)

    # close browser
    browser.quit()

if __name__ == "__main__":
    logging.basicConfig(filename='example.log',level=logging.DEBUG)
    worker()
    print("============= Done ==================")