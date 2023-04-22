import functools
import random
import re
import time
import selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from print_prettier import printblue, printcyan, printfinish, printgreen, printred, printyellow


def error_handling(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            printcyan('Class: {} | Function: {}'.format(
                func.__class__.__name__, func.__name__))
            func(*args, **kwargs)
        except selenium.common.exceptions.NoSuchElementException as e:
            errormessage = str(e).split('\n')[0]
            message = 'NoSuchElementException: \n\t{}'.format(errormessage)
            printyellow(message)
        except KeyboardInterrupt:
            printred('KeyboardInterrupt')
        except Exception as e:
            printyellow(
                'Errortype: \n\t{} \n Error: \n\t{}'.format(type(e), e))
    return wrapper


class WebScraper:
    @error_handling
    def __init__(self, url, **kwargs):
        self.__dict__.update(kwargs)
        self.url = url

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=ChromeService(
            ChromeDriverManager().install()), options=options)
        self.driver.get(self.url)

    @error_handling
    def __enter__(self):
        return self

    @error_handling
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()

    @error_handling
    def get_links(self):
        article_links = self.driver.find_elements(
            By.XPATH, '//a[@href]')
        links = [link.get_attribute('href') for link in article_links]

        self.links = links

    @error_handling
    def get_paragraphs(self):
        paragraphs = self.driver.find_elements(By.XPATH, self.paragraphsearch)
        self.paragraphs = '\n'.join(
            [paragraph.text for paragraph in paragraphs])

    @error_handling
    def get_titles(self):
        title = self.driver.find_elements(By.XPATH, self.titlesearch)
        titles = []
        for copy in title:
            if copy.text not in title:
                titles.append(copy.text)
        self.title = ' '.join(titles)

    @error_handling
    def get_author(self):
        author = self.driver.find_elements(By.XPATH, self.authorsearch)
        authors = []
        for copy in author:
            if copy.text not in authors:
                authors.append(copy.text)
        self.author = ' '.join(authors)

    @error_handling
    def get_time(self):
        self.time = self.driver.find_element(By.XPATH, self.timesearch)

    @error_handling
    def automate_scrape(self):
        for link in self.article_links:
            self.driver.get(link)
            self.get_paragraphs()
            self.get_titles()
            self.get_author()
            self.parse_time()

            self.print_data()
            time.sleep(2 + random.randint(0, 4))


class TheVergeScraper(WebScraper):
    @error_handling
    def __init__(self):
        # this could change
        kwargs = {
            'paragraphsearch': '//div[@class="duet--article--article-body-component"]//p',
            'titlesearch': '//h1',
            'authorsearch': '//a[contains(@href, "author")]',
            'timesearch': '//time'
        }

        # this could change
        super().__init__('https://www.theverge.com/ai-artificial-intelligence', **kwargs)

        self.get_links()
        self.filter_article_links()
        self.automate_scrape()

    @error_handling
    def parse_time(self):
        self.get_time()
        self.time = self.time.get_attribute('datetime')

    @error_handling
    def filter_article_links(self):
        regex = r'\d{4}\/?\d{1,2}\/?\d{1,2}'  # this could change
        self.article_links = []
        for link in self.links:
            if link not in self.article_links:
                matches = re.findall(regex, link)
                if len(matches) > 0:
                    self.article_links.append(link)

        printfinish('Found {} links: {}'.format(
            len(self.article_links), self.article_links[:5]))

    @error_handling
    def collect_data(self):
        self.data = {
            'title': self.title,
            'author': self.author,
            'time': self.time,
            'paragraphs': self.paragraphs,
            'link': self.driver.current_url,
        }

    @error_handling
    def print_data(self):
        printfinish()
        printblue('ANum rticle Links: {}'.format(len(self.article_links)))
        printblue('Title: {}'.format(self.title))
        printblue('Author: {}'.format(self.author))
        printblue('Time: {}'.format(self.time))
        printblue('Paragraphs: {}'.format(self.paragraphs[:200]))
        printfinish()


def main():
    with TheVergeScraper() as scraper:
        time.sleep(2)


if __name__ == '__main__':
    main()
