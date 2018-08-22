TF intro: https://www.tensorflow.org/guide/low_level_intro

virtualenv -p python3 env     	//create an environment called env
source env/bin/activate	       	//start the environment
source deactivate		//close the environment

pip install matplotlib
pip install numpy
pip install --upgrade tensorflow //for non-mac
pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.10.0-py3-none-any.whl //for mac
