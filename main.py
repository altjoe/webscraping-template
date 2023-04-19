import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# we don't really care aboust historical data so just scrape the first page


class FlexibleWebscraper():
    __chrome_options__ = Options()
    __chrome_options__.add_argument("--headless")

    def __enter__(self):
        self.driver = webdriver.Chrome(options=self.__chrome_options__)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()





if __name__ == "__main__":
    with FlexibleWebscraper() as scraper:
        print(scraper.driver.title)
