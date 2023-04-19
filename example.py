import re
import time
from webscraper_v1 import FlexibleWebscraper, SimplifiedWebscraper
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
    'author': ('span', 'class', 'f-ui-1 underline-thickness-1 underline-offset-4 underline')
}


towardsDataScience = {
}

googleAiBlog = {
    'url': 'https://ai.googleblog.com/',
    'link': ('a', 'class', 'post-outer-container'),
    'title': ('title', None, None),
    'time': ('time', None, None),
    'author': ('span', 'class', 'byline-author')
}
googleAiBackupParams = {
    'author': r'<span class="byline-author">(.*)</'
}


if __name__ == "__main__":
    # with SimplifiedWebscraper(techCrunchParams) as techCrunchScraper:
    # techCrunchScraper.auto_scrape_simple_articles()

    # with SimplifiedWebscraper(venturebeatParams) as ventureScraper:
    #     ventureScraper.auto_scrape_simple_articles()

    # with SimplifiedWebscraper(openaiParams, baseurl='https://openai.com') as openaiScraper:
    #     openaiScraper.auto_scrape_simple_articles()

    with SimplifiedWebscraper(googleAiBlog, backupparams=googleAiBackupParams) as googleAiScraper:
        googleAiScraper.auto_scrape_simple_articles()
