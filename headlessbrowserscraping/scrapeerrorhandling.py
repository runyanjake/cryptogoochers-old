
import selenium
from selenium.webdriver.firefox.options import Options
from selenium import webdriver   

URL = "https://bitcoincharts.com/markets/coinbaseUSD.html"
XPATH = "//div[@id='market_summary']/child::div/child::p/child::span"
DRIVERPATH = "./browserdrivers/chromedriver"

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(DRIVERPATH, chrome_options=chrome_options)

try:
    driver.get(URL)
    text = driver.find_element_by_xpath(XPATH).text
    print("Read: " + str(text))
    driver.quit()
except(selenium.common.exceptions.NoSuchElementException):
    print("Page loading failed, most likely on their end.")
    driver.quit()