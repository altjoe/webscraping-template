import pretty_errors
import requests
from bs4 import BeautifulSoup
from print_prettier import printred, printgreen, printyellow, printblue, printfinish, printcyan
import re


class FlexibleWebscraper_V2:
    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.isChild = self.set_param_if_valid('is_child', False)

        self.url = self.set_param_if_valid('url', None, required=True)
        self.article_link = self.set_param_if_valid(
            'article_link', None, required=not self.isChild)

        self.baseurl = self.set_param_if_valid('baseurl', '')
        self.bs4_multi_config = self.set_param_if_valid('bs4_multi', {})
        self.bs4_single_config = self.set_param_if_valid('bs4_single', {})
        self.regex_config = self.set_param_if_valid('regex', {})

        self.soup = BeautifulSoup(requests.get(self.url).text, 'html.parser')
        self.soupy_text = self.soup.text

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

    def regex_pass(self, key, regex):
        printred('regex_pass: regex: {}'.format(regex))
        pass

    def bs4_multi(self, key, element, attr=None, name=None):
        printblue('bs4_multi: element: {}, attr: {}, name: {}'.format(
            element, attr, name))
        element = self.soup.find_all(element)
        if attr != None and name != None:
            element = self.soup.find_all(element, {attr: name})

        if len(element) == 0:
            printyellow(
                'No elements found for: {} Pass: {}'.format(key, 'bs4_multi'))
            return -1

        result = ' '.join([element.text for element in element]).strip()
        printgreen('Found Multi key: {}\n Result {}\n Pass: {}\n'.format(
            key.upper(), result[:100], 'bs4_multi'))
        return result

    def bs4_single(self, key, element, attr=None, name=None):
        printblue('bs4_single: element: {}, attr: {}, name: {}'.format(
            element, attr, name))
        element = self.soup.find(element)
        if attr != None and name != None:
            element = self.soup.find(element, {attr: name})

        if len(element) == 0:
            printyellow('No elements found for: {} Pass: {}'.format(
                element, 'bs4_single'))
            return -1
        printgreen('Found Single key: {}\n Result {}\n Pass: {}'.format(
            key.upper(), element.text, 'bs4_multi'))
        return element.text

    # you can do multiple passes with the same key
    # in case one fails

    def find_article_data(self):
        current_article_data = {'url': self.url}
        for key, params in self.bs4_multi_config.items():
            if key not in current_article_data:
                current_article_data[key] = self.bs4_multi(key, *params)
        for key, params in self.bs4_single_config.items():
            if key not in current_article_data:
                current_article_data[key] = self.bs4_single(key, *params)
        for key, regex in self.regex_config.items():
            if key not in current_article_data:
                current_article_data[key] = self.regex_pass(key, regex)
        return current_article_data

    def get_article_links(self, element, attr=None, name=None):
        if attr and name:
            links = [element['href'] for element in self.soup.find_all(
                element, {attr: name})]
        else:
            links = [element['href']
                     for element in self.soup.find_all(element)]

        if len(links) == 0:
            raise Exception('No links found')
        print()
        printyellow('Found {} links\n'.format(len(links)))
        return links

    def automate_scrape(self):
        self.links = self.get_article_links(*self.article_link)

        for link in self.links:
            childparams = {
                'is_child': True,
                'url': link,
                'bs4_single': self.bs4_single_config,
                'bs4_multi': self.bs4_multi_config,
                'regex_config': self.regex_config
            }
            with FlexibleWebscraper_V2(childparams) as scraper:
                data = scraper.find_article_data()
                self.pc_article_data_pretty(data)
            break

    def pc_article_data_pretty(self, data):
        print()
        printfinish()
        printfinish('Title: {}'.format(data['title']))
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

    },
    'regex': {
        'author': 'by (.*)'
    }
}


def main():
    with FlexibleWebscraper_V2(params) as scraper:
        scraper.automate_scrape()
        pass


if __name__ == '__main__':
    main()
