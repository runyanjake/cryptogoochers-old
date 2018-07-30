NUM_LOOPS = 10

all:
	@echo Running headlessbrowserscraping.py on Python 3 using custom parameters...
	python3 headlessbrowserscraping.py --iterations 1000000 --wait_time 900
	@echo Done! Exiting...

allcurrencies:
	@echo Running headlessbrowserscraping.py on python3 for all currencies.
	./scrapeall.sh
	
multithreaded:
	@echo Runs 2 instances of headlessbrowserscraping.py as backgrounded tasks...
	python3 headlessbrowserscraping.py --browser chrome --iterations 10 --wait_time 30 &
	python3 headlessbrowserscraping.py --browser firefox --iterations 10 --wait_time 30 &
	@echo Done! Exiting...

trackall:
	@echo Tracks all currencies, with all running concurrently in the background.
	python3 headlessbrowserscraping.py --currency BTC --browser chrome --iterations 10000 --wait_time 1800 &
	python3 headlessbrowserscraping.py --currency ETH --browser firefox --iterations 10000 --wait_time 1800 &
	@echo Done! Exiting...
