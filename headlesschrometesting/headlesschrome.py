import os 
import time
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys

PATH_TO_CHROMEDRIVER = './chromedriver/chromedriver'
driver = webdriver.Chrome(PATH_TO_CHROMEDRIVER)  # Chrome driver, using the chromedriver file in PATH_TO_CHROMEDRIVER, if not specified will search path.

CRYPTO_WEB_SOURCES = ['https://www.coindesk.com',
                      'https://cointelegraph.com/bitcoin-price-index']

# driver.get('http://www.google.com/xhtml')
# time.sleep(5) # Let the user actually see something!
# search_box = driver.find_element_by_name('q')
# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5) # Let the user actually see something!

driver.get(CRYPTO_WEB_SOURCES[1])
btc_value_element = driver.find_element_by_xpath("//div[@class='value text-nowrap']")
btc_value = btc_value_element.text
print("BTC VALUE: " + str(btc_value))

# for url in CRYPTO_WEB_SOURCES:
#     print("REPORT FROM " + url + ": ")
#     driver.get(url)
#     try:
#         coin_name = driver.find_element_by_xpath('//div[@class=value text-nowrap]').text
#         coin_val = driver.find_element_by_xpath('//div[@class=price-link]').text
#         print('\t' + str(coin_name) + '\'s price is ' + str(coin_val))
#     except AttributeError:
#         print("\tWas not found on this page.")
#     time.sleep(2)

driver.quit()