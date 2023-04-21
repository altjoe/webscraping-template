import re
from print_prettier import printgreen, printyellow
from webscraper import FlexibleWebscraper


ventrueBeatParams = {
    'url': 'https://venturebeat.com/category/ai/',
    'article_link': ('a', 'class', 'ArticleListing__title-link'),
    'bs4_multi': {
        'content': ('p', None, None),

    },
    'bs4_single': {
        'title': ('h1', 'class', 'article-title'),
        'time': ('time', 'class', 'the-time'),
        'author': ('a', 'rel', 'author'),

    }
}


techcrunchParams = {
    'url': 'https://techcrunch.com/tag/ai/',
    'article_link': ('a', 'class', 'post-block__title__link'),
    'bs4_multi': {
        'content': ('p', None, None),
        'author': ('a', 'href', re.compile(r'/author/.*')),
    },
    'bs4_single': {
        'title': ('h1', 'class', 'article__title'),
        # 'time': ('time', 'class', 'full-date-time'),
    },
    'regex_config': {
        'time': r'<meta content=\"(20.*)\" name=\"cXenseParse:recs:publishtime\"/>',

    },
}


def vergeLinkFilter(links):
    filteredLinks = []
    for link in links:
        if link not in filteredLinks:
            filteredLinks.append(link)
            printgreen('link: {}'.format(link))

    return list(set(filteredLinks))


thevergeParams = {
    'url': 'https://www.theverge.com/ai-artificial-intelligence',

    'baseurl': 'https://www.theverge.com',
    'bs4_multi': {
        'content': ('p', None, None),
        'article_link': ('a', 'href', '.*'),
    },
    'bs4_single': {
        'title': ('h1', 'class', 'c-page-title'),
        'time': ('time', 'class', 'c-byline__item'),
        'author': ('a', 'class', 'c-byline__item'),
    },
    'bs4_attr:': {

    },
    'regex_config': {
        'article_link': 'href=\"(.+?)\"'
    },
    'link_filter': vergeLinkFilter
}


def main():
    with FlexibleWebscraper(thevergeParams) as scraper:
        if scraper.soup is not None:
            scraper.automate_scrape()


main()
