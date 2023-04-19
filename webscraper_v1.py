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
        self.beautiful_soup_string = str(self.beautiful_soup)
        with open('previous_soup.txt', 'w') as f:
            f.write(str(self.beautiful_soup))
        # print(self.beautiful_soup)
        self.prev_soup = None
        self.found = 'None found'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def get_content(self, link):
        paragraphs = self.beautiful_soup.find_all('p')
        return '\n'.join([paragraph.text for paragraph in paragraphs]).lstrip()

    def get_links(self, element, attr=None, name=None):
        if attr and name:
            links = [element['href'] for element in self.beautiful_soup.find_all(
                element, {attr: name})]
        else:
            links = [element['href']
                     for element in self.beautiful_soup.find_all(element)]
        return links

        # return [element['href'] for element in self.beautiful_soup.find_all(element, {attr: name})]
    def backup_pass(self, key, soup):
        try:
            regexstring = self.backup[key]
            regex = re.compile(regexstring)
            found = regex.findall(self.beautiful_soup_string)
            print('Backup parse: ', found)
            return found[0]
        except:
            traceback.print_exc()
            print('Second parse failed: ', key)
            return -1

    def pass_manager(self, key):
        pass_counter = 1
        while True:
            if pass_counter == 1:
                found = self.get_single_misc_text(*self.params[key])
                if found != -1:
                    return found
                else:
                    print('First Pass Failed: ', key)
                    pass_counter += 1

            elif pass_counter == 2:
                found = self.backup_pass(key)
                if found != -1:
                    return found
                else:
                    print('Second Pass Failed: ', key)
                    pass_counter += 1
            else:
                return -1

    def get_single_misc_text(self, element, attr=None, name=None):
        element = self.beautiful_soup.find(element)
        if attr != None and name != None:
            # print('attr: ', attr, 'name: ', name)
            element = self.beautiful_soup.find(element, {attr: name})

        # print(type(element), element.keys())
        if element:
            return element.text.strip()
        else:
            return -1


class SimplifiedWebscraper(FlexibleWebscraper):
    def __init__(self, params, baseurl='', backupparams=None):
        super().__init__(params['url'])
        if backupparams != None:
            self.backup = backupparams
        self.baseurl = baseurl
        self.linkparams = params['link']
        self.titleparams = params['title']
        self.timeparams = params['time']
        self.authorparams = params['author']
        self.params = params
        self.all_data = []

    def get_links(self):
        return super().get_links(*self.linkparams)

    def get_content(self, link):
        return super().get_content(link)

    def auto_scrape_simple_articles(self, **kwargs):
        links = self.get_links()
        if self.baseurl:
            links = [self.baseurl + link for link in links]

        if len(links) > 2:
            print('Recieved Links: ', str(links[:2])[
                  :-2] + ', ', f'...({len(links) - 2} more)]')
        elif len(links) == 0:
            print('No Links Found')
        else:
            print('Recieved Links: ', str(links))

        time.sleep(3)
        for link in links:
            if type(link) == tuple:
                link = link[0]
            article_data = {}
            onFailKey = 'None'
            try:
                with FlexibleWebscraper(link) as scraper:
                    for key in self.params:
                        onFailKey = key
                        if key == 'url' or key == 'link':
                            continue

                        found = scraper.pass_manager(key)
                        if found == -1:
                            raise Exception('Failed to find: ', key)
                        article_data[key] = found

                    article_data['link'] = link
                    article_data['content'] = scraper.get_content(link)

                    self.print_article(article_data)

            except Exception as e:
                print('################ Start Error ################')
                print('Error on: ', onFailKey)
                print(type(e), e)
                if type(e) == TypeError:
                    print('Type Error: ', *self.params[onFailKey])
                traceback.print_exc()
                # print(f'Auto Scrape Failed on: ${onFailKey}')
                print('################ End Error ################')
                with open('soup.out', 'w') as f:
                    f.write(self.beautiful_soup.prettify())
                break
            time.sleep(2)
        # pd.DataFrame(self.all_data).to_csv('venturebeat.csv', index=False)

    def print_article(self, article):
        print('------------------------- start')
        print('Title: ', article['title'])
        print('Author: ', article['author'])
        print('Time: ', article['time'])
        print('Link: ', article['link'])
        print('Content: ', article['content'][:50])
        print('------------------------- end')
        print('\n')

# if __name__ == "__main__":
    # with FlexibleWebscraper('https://venturebeat.com/category/ai/') as scraper:
    #     scraper.auto_scrape()

        # print(scraper)
        # time.sleep(2)
