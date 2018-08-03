Install tweepy: pip install tweepy

Get the twitter ckey at https://apps.twitter.com

The pickling is set up already, and all that needs to be done is the actual pickling (run classifier.py)
Then, sentimentanalysis.py can be run straightaway. A lot of things need to be installed.

When running with the twitter grabber and updating graph (make graphupdate) option, don't close the graph first, CMD+C the terminal to stop the twitter grabber first or it will continually run and will have to be task manager'd. 

virtualenv -p python3 env     	//create an environment called env
source env/bin/activate	       	//start the environment
source deactivate		//close the environment

pip install matplotlib
pip install selenium		//the selenium package for running headless browsers
pip install plotly
pip install plotly --upgrade
