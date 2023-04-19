import re
import time
from main import FlexibleWebscraper, SimplifiedWebscraper
import pandas as pd


venturebeatParams = {
    'url': 'https://venturebeat.com/category/ai/',
    'link': ('a', 'class', 'ArticleListing__title-link'),
    'title': ('h1', 'class', 'article-title'),
    'time': ('time', 'class', 'the-time'),
    'author': ('a', 'rel', 'author')
}

techCrunchParams = {
    'url': 'https://techcrunch.com/tag/ai/',
    'link': ('a', 'class', 'post-block__title__link'),
    'title': ('h1', 'class', 'article__title'),
    'time': ('time', 'class', 'full-date-time'),
    'author': ('a', 'href', re.compile(r'/author/.*'))
}

openaiParams = {
    'url': 'https://openai.com/blog',
    'link': ('a', 'type', 'blog-details'),
    'title': ('h1', 'class', 'f-display-2'),
    'time': ('span', 'class', 'f-meta-2'),
    'author': ('a', 'href', 'router-link-active router-link-exact-active ui-link group inline-block ui-link--underline relative text-primary')
}




if __name__ == "__main__":
    # with SimplifiedWebscraper(techCrunchParams) as techCrunchScraper:
    # techCrunchScraper.auto_scrape_simple_articles()

    # with SimplifiedWebscraper(venturebeatParams) as ventureScraper:
    #     ventureScraper.auto_scrape_simple_articles()

    with SimplifiedWebscraper(openaiParams, baseurl='https://openai.com') as openaiScraper:
        openaiScraper.auto_scrape_simple_articles(overwrite={'title': False, 'time': False, 'author': True})
       
