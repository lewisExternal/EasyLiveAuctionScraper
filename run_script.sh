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

if [ $# -eq 3 ] && [[ $3 == "y" || $3 == "Y" ]];
then
    echo "Script will be run in the background. Please run: watch tail log.txt"
    nohup python3.8 process_auction_house.py $1 $2 $3 > log.txt 2>&1 &
else 
    python3.8 process_auction_house.py $1 $2
fi

deactivate