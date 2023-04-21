import pretty_errors
import requests
from bs4 import BeautifulSoup
from print_prettier import printred, printgreen, printyellow, printblue, printfinish, printcyan
import re
import time
import random


class FlexibleWebscraper:
    """
    This is a webscraper that can be used with almost any article website.

    required params: url, article_link
    optional params: baseurl, bs4_multi, bs4_single, regex_config
    structure of params and examples of usage:
    'url': 'hhtp://url to scrape.com',
    'article_link': ('a', 'href', re.compile(r'http://ai.googleblog.com/20.*')),
    'bs4_multi': {
        'content': ('p', None, None),
        'time': ('time', None, None),
    },
    'bs4_single': {
        'title': ('title', None, None),
        'author': ('p', 'id', 'newBylineAuthor')

    },
    'regex_config': {
        'author': r'Posted by (.*?)</'
    }
    """

    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.isChild = self.set_param_if_valid('is_child', False)

        self.url = self.set_param_if_valid('url', None, required=True)

        self.baseurl = self.set_param_if_valid('baseurl', '')
        self.bs4_multi_config = self.set_param_if_valid('bs4_multi', {})
        self.bs4_single_config = self.set_param_if_valid('bs4_single', {})
        self.regex_config = self.set_param_if_valid('regex_config', {})
        self.bs4_element_attr_config = self.set_param_if_valid(
            'bs4_attr', {})
        self.link_filter = self.set_param_if_valid('link_filter', None)

        self.soup = self.make_the_soup(self.url, self.baseurl)
        self.soupy_text = str(self.soup)
        # try:
        #     self.soup = BeautifulSoup(
        #         requests.get(self.url).text, 'html.parser')

        #     self.soupy_text = str(self.soup)

        #     with open('soupy_text.log', 'w') as f:
        #         f.writelines(self.soupy_text)
        # except Exception as e:
        #     if e == requests.exceptions.MissingSchema:
        #         printred('Missing Schema. Moving on...')

    def make_the_soup(self, url, baseurl):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        try:
            stock = BeautifulSoup(requests.get(
                url, headers=headers).text, 'html.parser')
            return stock
        except Exception as e:
            if e == requests.exceptions.MissingSchema:
                try:
                    stock = BeautifulSoup(requests.get(
                        baseurl + url, headers=headers).text, 'html.parser')
                    return stock
                except:
                    return None

    def set_param_if_valid(self, param, default, required=False):
        if param in self.kwargs:
            return self.kwargs[param]
        else:
            if required:
                raise Exception('No {} provided'.format(param))
            return default

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_paragraphs(self, link):
        paragraphs = self.soup.find_all('p')
        return '\n'.join([paragraph.text for paragraph in paragraphs]).lstrip()[1:]

    def regex_pass(self, key, regexstr):
        printblue('regex_pass: regexstr: {}, key: {}'.format(
            regexstr, key.upper()))

        match = re.findall(regexstr, self.soupy_text)

        if len(match) == 0:
            printyellow(
                'No elements found for: {} Pass: {}\n'.format(key, 'regex_pass'))
            return -1
        elif len(match) > 1:
            printyellow(
                'Multiple elements found for: {} Pass: {}\n'.format(key, 'regex_pass'))
            return ' '.join(match).strip()

        printgreen('Found regex key: {}\n Result {}\n Pass: {}\n'.format(
            key.upper(), match[0].strip(), 'regex_pass'))
        return match[0].strip()

    def bs4_multi(self, key, element, attr=None, name=None):
        printblue('bs4_multi: element: {}, attr: {}, name: {}'.format(
            element, attr, name))

        if attr != None and name != None:
            element = self.soup.find_all(element, {attr: name})
        else:
            element = self.soup.find_all(element)

        if len(element) == 0:
            printyellow(
                'No elements found for: {} Pass: {}\n'.format(key, 'bs4_multi'))
            return -1

        result = ' '.join([element.text for element in element]).strip()
        printgreen('Found Multi key: {}\n Result {}\n Pass: {}\n'.format(
            key.upper(), result[:100], 'bs4_multi'))
        return result

    def bs4_single(self, key, element, attr=None, name=None):
        printblue('bs4_single: element: {}, attr: {}, name: {}'.format(
            element, attr, name))

        if attr != None and name != None:
            element = self.soup.find(element, {attr: name})
        else:
            element = self.soup.find(element)

        if not element:
            printyellow('No elements found for: {} Pass: {}\n'.format(
                key, 'bs4_single'))
            return -1
        printgreen('Found Single key: {}\n Result {}\n Pass: {}\n'.format(
            key.upper(), element.text, 'bs4_multi'))
        return element.text.strip()

    def bs4_element_attr(self, key, element, attr=None, name=None, toget=None):
        printblue('bs4_attr: element: {}, attr: {}, name: {}'.format(
            element, attr, name))

    # you can do multiple passes with the same key
    # in case one fails

    def find_article_data(self):

        current_article_data = {'url': self.baseurl + self.url}
        for key, params in self.bs4_multi_config.items():
            if key not in current_article_data:
                current_article_data[key] = self.bs4_multi(key, *params)
        for key, params in self.bs4_single_config.items():
            if key not in current_article_data:
                current_article_data[key] = self.bs4_single(key, *params)
        for key, regex in self.regex_config.items():
            if key not in current_article_data:
                current_article_data[key] = self.regex_pass(key, regex)
        for key, params in self.bs4_element_attr_config.items():
            if key not in current_article_data:
                current_article_data[key] = self.bs4_element_attr(key, *params)

        # if any of the values are -1, then the article is not valid
        if -1 in current_article_data.values():
            printred('Article is not valid for: {}\n'.format(self.url))
            return -1

        return current_article_data

    def get_article_links(self):

        links = []
        if 'article_link' in self.bs4_single_config:
            links += [self.baseurl + element['href'] for element in self.soup.find(
                *self.bs4_single_config['article_link'])]
        if 'article_link' in self.bs4_multi_config:
            links += [self.baseurl + element['href'] for element in self.soup.find_all(
                *self.bs4_multi_config['article_link'])]
        if 'article_link' in self.regex_config:
            links = [self.baseurl + href for href in re.findall(
                self.regex_config['article_link'], self.soupy_text)]

        if self.link_filter != None:
            links = self.link_filter(links)
        else:
            links = list(set(links))

        if len(links) == 0:
            raise Exception('No links found')

        printblue('Found {} links {}\n'.format(len(links), links[:5]))
        return links

    # def get_article_links(self, element, attr=None, name=None):
    #     if attr and name:

    #         links = [element['href'] for element in self.soup.find_all(
    #             element, {attr: name})]

    #         printred(links[0])
    #     else:
    #         links = [element['href']
    #                  for element in self.soup.find_all(element)]

    #     unique_links = list(set(links))
    #     links = unique_links

    #     if len(links) == 0:
    #         raise Exception('No links found')

    #     print()
    #     printblue('Found {} links {}\n'.format(len(links), links[:5]))
    #     return links

    def automate_scrape(self):
        self.links = self.get_article_links()

        for link in self.links:
            childparams = {
                'is_child': True,
                'url': link,
                'bs4_single': self.bs4_single_config,
                'bs4_multi': self.bs4_multi_config,
                'regex_config': self.regex_config,
                'bs4_element_attr_config': self.bs4_element_attr_config
            }
            with FlexibleWebscraper(childparams) as scraper:
                data = scraper.find_article_data()
                if data != -1:
                    self.pc_article_data_pretty(data)
            time.sleep(5 + random.randint(0, 3))

    def pc_article_data_pretty(self, data):
        print()
        printfinish()
        printfinish('Title: {}'.format(data['title']))
        printfinish('Author: {}'.format(data['author']))
        printfinish('Time: {}'.format(data['time']))
        printfinish('Content: {}'.format(data['content'][:100]))
        printfinish('URL: {}'.format(data['url']))
        printfinish()
        print()


params = {
    'url': 'https://ai.googleblog.com/',
    'article_link': ('a', 'href', re.compile(r'http://ai.googleblog.com/20.*')),
    'bs4_multi': {
        'content': ('p', None, None),
        'time': ('time', None, None),
    },
    'bs4_single': {
        'title': ('title', None, None),
        # 'author': ('p', 'id', 'newBylineAuthor')

    },
    'regex_config': {
        'author': r'Posted by (.*?)</'
    },
    'bs4_element_attr_config': {
        'time': ('time', 'datetime', re.compile(r'20.*')),
    }
}


def main():
    with FlexibleWebscraper(params) as scraper:
        scraper.automate_scrape()
        pass


if __name__ == '__main__':
    main()
