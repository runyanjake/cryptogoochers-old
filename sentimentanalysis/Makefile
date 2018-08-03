all:
	@echo Creating an offline and non-updating graph of sentiment data...
	make graphoffline
	@echo Done.

retrain:
	@echo Retraining and re-pickling ML models...
	python classifier.py
	@echo Done.

getdata:
	@echo Gathering Twitter data...
	python sentimentanalysis.py
	@echo Done.

graphoffline:
	@echo "Creating graph of Twitter data (non-updating)..."
	python grapher.py
	@echo Done.

graphrefresh:
	@echo Creating graph of Twitter data that updates to include new data...
	make getdata &
	make graphoffline 
	@echo Done.

