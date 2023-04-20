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


def main():
    with FlexibleWebscraper(ventrueBeatParams) as scraper:
        scraper.automate_scrape()
        pass

main()