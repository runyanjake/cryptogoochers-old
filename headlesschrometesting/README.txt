When running this stuff it's useful to have (and was designed with) a virtual python environment with Selenium installed so it doesn't need to clutter up your normal installation.

(and get google chrome canary)

virtualenv -p python3 env     	//create an environment called env
source env/bin/activate	       	//start the environment
source deactivate		//close the environment

pip install selenium		//the selenium package for running headless browsers
