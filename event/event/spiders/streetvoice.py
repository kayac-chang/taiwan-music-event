from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Response
from bs4 import BeautifulSoup
from datetime import datetime


def parse_activity(response: Response):
    soup = BeautifulSoup(response.text, 'lxml')

    def parse_date(text: str):
        [date, _, time] = text.split('|')
        return {
            'text': text,
            'datetime': datetime.strptime(
                f'{date.strip()} {time.strip()}',
                "%Y 年 %m 月 %d 日 %H:%M"
            )
        }

    def parse_location(selector: str):
        tag = soup.select_one(selector)
        return {
            'address': tag.contents[2],
            'map': tag.contents[3]['href'],
        }

    def parse_text(selector: str):
        return soup.select_one(selector).get_text(strip=True)

    yield {
        'title': parse_text('#pjax-container h1'),
        'date':
            parse_date(parse_text('#pjax-container h3:nth-of-type(1)')),
        'location': parse_location('#pjax-container h3:nth-of-type(2)'),
        'ticket': parse_text('#pjax-container h3:nth-of-type(3)'),
        'artists':
            parse_text('#pjax-container h3:nth-of-type(4)').split('・'),
        'description':
            soup.select_one('#pjax-container .text-read p').prettify()
    }


class StreetvoiceSpider(CrawlSpider):
    name = 'streetvoice'
    allowed_domains = ['streetvoice.com']
    start_urls = ['https://streetvoice.com/venue/activities/all/0/']

    rules = (
        Rule(
            link_extractor=LinkExtractor(
                allow=r'/venue/activities/all',
                unique=True,
            ),
            follow=True
        ),
        Rule(
            link_extractor=LinkExtractor(
                allow=r'/venue/activities/\d',
                unique=True
            ),
            callback=parse_activity
        )
    )
