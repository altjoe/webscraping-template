import time
import traceback
import pretty_errors
import re
from bs4 import BeautifulSoup
import requests


# driver = webdriver.Chrome("chromedriver")

# we don't really care aboust historical data so just scrape the first page

# chromedriver path for selenium


class FlexibleWebscraper():
    def __init__(self, url):
        self.url = url
        self.beautiful_soup = BeautifulSoup(
            requests.get(url).text, "html.parser")
        # print(self.beautiful_soup)
        self.prev_soup = None
        self.found = 'None found'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_links(self, element, attr, name):
        return [element['href'] for element in self.beautiful_soup.find_all(element, {attr: name})]

    def get_single_misc_text(self, element, attr, name):
        element = self.beautiful_soup.find(element, {attr: name})
        if element:
            return element.text.strip()
        else:
            return -1


class SimplifiedWebscraper(FlexibleWebscraper):
    def __init__(self, params, baseurl=None):
        super().__init__(params['url'])
        self.baseurl = baseurl
        self.linkparams = params['link']
        self.titleparams = params['title']
        self.timeparams = params['time']
        self.authorparams = params['author']
        self.all_data = []

    def get_links(self):
        return super().get_links(*self.linkparams)

    def get_content(self, link):
        return super().get_content(link)

    def auto_scrape_simple_articles(self, overwrite={'title': False, 'time': False, 'author': False}):
        links = self.get_links()
        if self.baseurl:
            links = [self.baseurl + link for link in links]
        for link in zip(links):
            if type(link) == tuple:
                link = link[0]
            article_data = {}
            with FlexibleWebscraper(link) as scraper:

                if overwrite['title'] == False:
                    article_data['title'] = scraper.get_single_misc_text(
                        *self.titleparams)
                if overwrite['time'] == False:
                    article_data['time'] = scraper.get_single_misc_text(
                        *self.timeparams)
                if overwrite['author'] == False:
                    article_data['author'] = scraper.get_single_misc_text(
                        *self.authorparams)

                print(article_data['author'],
                      article_data['title'], article_data['time'], link)
                self.all_data.append(article_data)
                # print(article_data['author'])
            time.sleep(2)
        pd.DataFrame(self.all_data).to_csv('venturebeat.csv', index=False)


# if __name__ == "__main__":
    # with FlexibleWebscraper('https://venturebeat.com/category/ai/') as scraper:
    #     scraper.auto_scrape()

        # print(scraper)
        # time.sleep(2)
