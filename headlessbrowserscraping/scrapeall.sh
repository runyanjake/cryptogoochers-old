#!/bin/bash

NUMLOOPS=10
WAITTIME=2 #seconds

COUNTER=1
while [  $COUNTER -le $NUMLOOPS ]; do
    echo Scraping iteration $COUNTER/$NUMLOOPS
	echo -e "\tBTC" 
	python3 headlessbrowserscraping.py --currency BTC --browser chrome --iterations 1 --wait_time 1 > /dev/null
	echo -e "\tETH" 
	python3 headlessbrowserscraping.py --currency ETH --browser chrome --iterations 1 --wait_time 1 > /dev/null
	echo -e "\tXRP" 
	python3 headlessbrowserscraping.py --currency XRP --browser chrome --iterations 1 --wait_time 1 > /dev/null
	echo -e "\tEOS" 
	python3 headlessbrowserscraping.py --currency EOS --browser chrome --iterations 1 --wait_time 1 > /dev/null
	echo -e "\tXLM" 
	python3 headlessbrowserscraping.py --currency XLM --browser chrome --iterations 1 --wait_time 1 > /dev/null
	echo -e "\tLTC" 
	python3 headlessbrowserscraping.py --currency LTC --browser chrome --iterations 1 --wait_time 1 > /dev/null
	echo -e "\tADA" 
	python3 headlessbrowserscraping.py --currency ADA --browser chrome --iterations 1 --wait_time 1 > /dev/null
	echo -e "\tMIOTA" 
	python3 headlessbrowserscraping.py --currency MIOTA --browser chrome --iterations 1 --wait_time 1 > /dev/null
	echo -e "\tTRX" 
	python3 headlessbrowserscraping.py --currency TRX --browser chrome --iterations 1 --wait_time 1 > /dev/null
	# IF ON WINDOWS USE "> nul" not "> /dev/null"

    sleep $WAITTIME
    let COUNTER=COUNTER+1 
done
