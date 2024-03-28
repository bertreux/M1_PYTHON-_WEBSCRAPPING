import scrapy
from testScrapy.items import QuotescrapItem

def start_requests(self):
        user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
        ]

        fake_browser_header = {
            "upgrade-insecure-requests": "1",
            "user-agent": "",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-site": "none",
            "sec-fetch-mod": "",
            "sec-fetch-user": "?1",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "fr-CH,fr;q=0.9,en-US;q=0.8,en;q=0.7"
        }

        for url in self.start_urls:
            userr = user_agent_list[randint(0, len(user_agent_list)-1)]
            fake_browser_header["user-agent"] = userr
            print(f"\n************ New User Agent *************\n{userr}\n")
            yield scrapy.Request(url=url, callback=self.parse, headers=fake_browser_header)

class QuoteSpider(scrapy.Spider):
    name = 'quotespider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        quote = response.css('div.col-md-8 div.quote')
        quote_item = QuotescrapItem()

        for q in quote:
            quote_item['quote'] = q.css('span.text::text').get()
            quote_item['author'] = q.css('small::text').get()
            quote_item['about'] = 'http://quotes.toscrape.com'+q.css('span a').attrib['href']
            quote_item['tags'] = {tmp: None for tmp in q.css('div.tags a.tag::text').getall()}
            yield quote_item

        next_page = response.css('ul.pager li.next a').attrib['href']
        if next_page is not None:
            next_page_url = 'http://quotes.toscrape.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)