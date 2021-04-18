# Easy Live Auction
Get product information from the domain easyliveauction.com

## How to run
Script takes two command line arguments 

>1. (Optional) auction_link_url i.e 'https://www.easyliveauction.com/auctioneers/2020auctions/' [default]
>2. (Optional) resilience i.e 'y' 

Select the auction house from the following https://www.easyliveauction.com/auctioneers/, insert into the first parameter.  
Existence of the second argument will mean the auctions table will not be populated. 

i.e to run in resilience mode 

> ./run_script.sh https://www.easyliveauction.com/auctioneers/2020auctions/ y 

## Results 

Stored in a sqlite DB, hard coded as pythonsqlite.db. Schemas can be seen below. 

""" TABLE auctions (
                                        id integer PRIMARY KEY,
                                        link text NOT NULL,
                                        auction_house_url text NOT NULL, 
                                        processed INT NOT NULL
                                    ); """

""" TABLE products (
                                    id integer PRIMARY KEY,
                                    itemno text,
                                    price text,
                                    desc text,
                                    img text,
                                    date text,
                                    url text 
                                );""


## Requirements 
The script has been written to create a virtual environment to install requirements 
Please see the requirements.txt
Needs Python-3.8.5 or later 

## Testing
No unit tests as yet 

## TO DO 
N/A 