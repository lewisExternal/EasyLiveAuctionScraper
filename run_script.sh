#!/bin/bash

function activate {
            source env/bin/activate
}

if [ ! -d "./env" ];
then

echo "Creating environment..."
python3.8 -m venv env
activate
python3.8 -m pip install -r requirements.txt

else

echo "Environment already exists"
activate

fi

#nohup python3.8 process_auction_house.py $1 $2 > log.txt 2>&1 & 
python3.8 process_auction_house.py $1 $2

deactivate