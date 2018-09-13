===== Environment Notes ===== 
General
    virtualenv -p python3 env     	//create an environment called env
    source env/bin/activate	       	//start the environment
    source deactivate		//close the environment
For use with JScraper
    <ADD THESE>
HypotheticalTrader.py
    pip install ccxt 


===== Vectorspace has some Cryptocurrency APIs that you can query to receive JSON =====

===== Thoughts =====
The token addresses seem to be important but not unique. 
Changing it seems to not really do anything. 
Is it a demo token and do i need to get an access token of my own?

===== Notes =====
"Baskets" are bundles of cryptocurrencies, much like groupings of stocks. part of the VS api generates these, idk how good it is tho.

Correlated cryptocurrencies via context-controlled NLP
curl -d "query=machine+learning&vxv_token_addr=0xC2A568489BF6AAC5907fa69f8FD4A9c04323081D" -X POST https://vectorspace.ai/recommend/app/correlated_cryptos