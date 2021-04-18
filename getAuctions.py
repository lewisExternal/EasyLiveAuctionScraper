from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import sys
#from webdriver_manager.chrome import ChromeDriverManager
import numpy as np 
import pandas as pd 
import time

def get_driver():
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #driver = webdriver.Chrome('./chromedriver')
    # Google VM 
    #chrome_options.binary_location = "/opt/google/chrome/google-chrome"
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options,executable_path=r'/usr/bin/chromedriver')

def get_auction_links(driver):
    
    result_array = []

    # get auctions 
    item_no = driver.find_elements_by_class_name('auction-title')

    # get auction links 
    for item in item_no:
        result_array.append(item.find_elements_by_tag_name('a')[0].get_attribute('href'))

    return result_array

def next_page(driver,url):
    
    return_code = -1
    
    try:
        element = driver.find_element_by_xpath('//*[@id="right-content"]/div/div/div[4]/div/div[3]')
        element.click() 

        # if the url doesn't increment exit the loop 
        if driver.current_url == url:
            return_code = 0

    except:
        # error case 
        return_code = 0
    
    return return_code
    
def main(url):

    auctions_list_array = [] 

    # get driver 
    driver = get_driver()
    #driver = webdriver.Chrome(ChromeDriverManager().install())

    # current strategy revolves around cycling within the past auction
    driver.get(url)

    # get auctions from first page
    auctions_list_array = get_auction_links(driver)

    # set default loop value 
    x = -1 

    # loop through all auctions 
    while x != 0:
        
        # get auction links 
        auctions_list = get_auction_links(driver)

        # append each of the links 
        for auction in auctions_list:
            auctions_list_array.append(auction)
    
        url = driver.current_url

        # move the page if possible 
        x = next_page(driver,url)
    
    # save data 
    #df = pd.DataFrame(data=auctions_list_array, columns=["auction_links"])
    #df.to_csv('_auction_links.csv')
    
    # quit the driver 
    driver.quit()

    return auctions_list_array

if __name__ == "__main__":
    main()
