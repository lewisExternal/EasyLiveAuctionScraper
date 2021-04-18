from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import sys
#from webdriver_manager.chrome import ChromeDriverManager
import numpy as np 
import pandas as pd 
import time
import getAuctions
import scrapeAuction
import db_lib
import sqlite3
from pyvirtualdisplay import Display

###############################################################
# DATE: 2021/03
# AUTHOR: LEWIS JAMES 
###############################################################

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
    
    auction_links = []
    links = driver.find_element_by_class_name('blue-text').find_elements_by_tag_name('a')
    
    # extract href 
    for link in links:
        auction_links.append(link.get_attribute('href'))
    
    return auction_links

def main():

    # take parameters from the command line 
    arguments = len(sys.argv) - 1
    print ("The script is called with %i argument(s)" % (arguments))
    #print(sys.argv[1])

    # create virtual display for Raspberry Pi deployment
    display = Display(visible=0, size=(800, 600))
    display.start()
    
    # get driver 
    driver = get_driver()
    #driver = webdriver.Chrome(ChromeDriverManager().install())

    # set auction links, first command line argument 
    if arguments >= 1: 
        auction_house_url = sys.argv[1]
    else: 
        print("Default auction house selected: https://www.easyliveauction.com/auctioneers/2020auctions/")
        auction_house_url = "https://www.easyliveauction.com/auctioneers/2020auctions/"

    # set auction links, first command line argument 
    if arguments == 2: 
        resilience = True
    else: 
        print("Default resilience = False")
        resilience = False   

    # database name 
    database = r"pythonsqlite.db"

    # create the db if it doesn't already exist 
    db_lib.main(database) 
    print("DB called.")
    
    # get connection to db 
    conn = db_lib.create_connection(database)
    print("Connection to the DB established.")

    # get auctions to process 
    if resilience == False:
        
        # get auction links
        driver.get(auction_house_url)

        # get auction links 
        links_to_process = get_auction_links(driver)
        print("Links to process the auctions have been found.")
        driver.quit()

        # save links to auctions 
        links_to_auctions_df = pd.DataFrame(links_to_process,columns=['links'])
        #links_to_auctions_df.to_csv("auction_links.csv")

        # collect list of auctions 
        auctions_array = []
        print("Collecting auctions...")
        
        for link in links_to_process:

            try:
                # get an array of auctions 
                auction_result = getAuctions.main(link)
            
                # add each reuslt to resutl array 
                for auction in auction_result:
                    auctions_array.append(auction)

            except Exception as e:
                print("This link is an error:  " + link + "   " + str(e))
    
        print("The number of auctions found is " + str(len(auctions_array)))

        # create an auctions df 
        auctions_array_df = pd.DataFrame(auctions_array,columns=['link']) 

        # add columns to the df for AH and processed flag 
        auctions_array_df['auction_house_url'] =  auction_house_url
        auctions_array_df['processed'] = 0
    
        # save auction links to the database 
        auctions_array_df.to_sql('auctions', conn, if_exists='append', index=False)
        print("Auctions data has been inserted to the DB.")
    
    else:
        # get auctions in the DB 
        auctions_array = db_lib.get_auction_links_to_process(conn,auction_house_url)

    # get products from auctions
    print("Getting products from auctions...")
    counter = 1 
    for auction in auctions_array:
      
        try:

            print("Processing auction: " + str(counter) + " of "+ str(len(auctions_array)))
            
            # convert to a string if tuple
            if isinstance(auction,tuple):
                auction = ''.join(auction)

            # process products from auctions 
            product_df = scrapeAuction.main(auction)

            # save reuslts to the product data base 
            product_df.to_sql('products', conn, if_exists='append', index=False)
            
            # set the auction processed flag once complete 
            db_lib.update_processed_auction(conn,auction)

        except Exception as e:
            print("Processing " + auction + " we have observed the following error. " + str(e))
        
        # increment counter 
        counter = counter + 1 



if __name__ == "__main__":
    main()
