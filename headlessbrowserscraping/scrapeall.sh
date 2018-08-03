#!/bin/bash

NUMLOOPS=1000
WAITTIME=900 #seconds

COUNTER=1
while [  $COUNTER -le $NUMLOOPS ]; do
    echo Scraping ALL CRYPTOCURRENCY TYPES iteration $COUNTER/$NUMLOOPS
	echo -e "\tBTC" 
	python3 headlessbrowserscraping.py --currency BTC --browser chrome --iterations 1 --wait_time 1
	echo -e "\tETH" 
	python3 headlessbrowserscraping.py --currency ETH --browser chrome --iterations 1 --wait_time 1
	echo -e "\tXRP" 
	python3 headlessbrowserscraping.py --currency XRP --browser chrome --iterations 1 --wait_time 1
	echo -e "\tEOS" 
	python3 headlessbrowserscraping.py --currency EOS --browser chrome --iterations 1 --wait_time 1
	echo -e "\tXLM" 
	python3 headlessbrowserscraping.py --currency XLM --browser chrome --iterations 1 --wait_time 1
	echo -e "\tLTC" 
	python3 headlessbrowserscraping.py --currency LTC --browser chrome --iterations 1 --wait_time 1
	echo -e "\tADA" 
	python3 headlessbrowserscraping.py --currency ADA --browser chrome --iterations 1 --wait_time 1 
	echo -e "\tMIOTA" 
	python3 headlessbrowserscraping.py --currency MIOTA --browser chrome --iterations 1 --wait_time 1 
	echo -e "\tTRX" 
	python3 headlessbrowserscraping.py --currency TRX --browser chrome --iterations 1 --wait_time 1
        echo -e "\tUSDT"
        python3 headlessbrowserscraping.py --currency USDT --browser chrome --iterations 1 --wait_time 1
        echo -e "\tXMR"
        python3 headlessbrowserscraping.py --currency XMR --browser chrome --iterations 1 --wait_time 1

    sleep $WAITTIME
    let COUNTER=COUNTER+1 
done
