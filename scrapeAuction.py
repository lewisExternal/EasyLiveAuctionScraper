from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import sys
#from webdriver_manager.chrome import ChromeDriverManager
import numpy as np 
import pandas as pd 
from halo import Halo


def get_driver():
    
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    #chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    # Google VM 
    #chrome_options.binary_location = "/opt/google/chrome/google-chrome"
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options,executable_path=r'/usr/bin/chromedriver')

def get_price(driver):
    try:
        price_element = driver.find_elements_by_xpath('/html/body/div[6]/div/div[2]/div[1]/div[1]/div/div[5]/div[1]/p')[0]
        price = price_element.text
        return price.replace("Â", "")
    except:
        return 'Error'
        
def get_desc(driver):
    try:
        desc_element = driver.find_elements_by_xpath('/html/body/div[6]/div/div[2]/div[1]/div[1]/div/div[5]/div[3]/p')[0]
        desc = desc_element.text
        return desc
    except: 
        return 'Error'
    
def get_image(driver):
    try:
        image_element = driver.find_elements_by_xpath('//*[@id="main-image1"]')[0]
        image = image_element.get_attribute("src")
        return image
    except:
        return 'Error'
    
def get_date(driver):
    try:
        date_element = driver.find_elements_by_xpath('/html/body/div[6]/div/div[2]/div[2]/div[4]/div/div/div[1]/div[1]/div/div/div[2]/div/div[2]')[0]
        date = date_element.text
        return date
    except:
        return 'Error'

def get_url(driver):
    try: 
        return driver.current_url
    except:
        return 'Error' 
    
def get_itemno(driver):
    item_no = (driver.find_elements_by_tag_name('strong'))[1].text
    item_no = item_no.translate({ord(i): None for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'})
    return int(item_no)

def next_page(driver):
    element = driver.find_element_by_link_text('Next') #.find_element_by_class_name('row').find_element_by_class_name('col-xs-12 col-sm-7')
    element.click()  

def first_item(driver):
    try:
        lot_0 = driver.find_element_by_xpath('//*[@id="right-content"]/div/div/div[7]/div/div/div/div[1]/div/div[2]/h4')
        lot_0.click()  
    except Exception as e:
        print("Lot 0 does not exist, exit."+str(e))
        sys.exit 


def main(url,background):

    # get driver 
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = get_driver()

    # current strategy revolves around cycling within the past auction
    driver.get(url)

    # click the first item in auction 
    first_item(driver)

    # set default x value 
    x = -1

    # empty array for result
    item_array = []
    result_array = []

    # spinner to show the script is running only if not in the background 
    if background == False:
        spinner = Halo(text='Processing Products', spinner='dots')
        spinner.start()
    
    # revolve round the loop unil the lot number reachers zero, then stop
    while x != 0:

        # scrape product values 
        item_array=[x,get_price(driver),get_desc(driver),get_image(driver),get_date(driver),get_url(driver)]
        result_array.append(item_array)
        #print(result_array)
        # Move next
        #print(str(x))
        next_page(driver)
        x = get_itemno(driver)
    
    if background == False:
        spinner.stop()
    
    driver.quit()

    df = pd.DataFrame(data=result_array, columns=["itemno", "price","desc","img","date","url"])
    #df.to_csv('result.csv')

    return df

if __name__ == "__main__":
    main()

