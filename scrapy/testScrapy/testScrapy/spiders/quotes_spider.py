import scrapy

class QuoteSpider(scrapy.Spider):
    name = 'quotespider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        quote = response.css('div.col-md-8 div.quote')
        for q in quote:
            yield{
             'quote' :q.css('span.text::text').get(),
             'author' : q.css('small::text').get(),
             'about' : 'http://quotes.toscrape.com'+q.css('span a').attrib['href'],
             'tags' : {tmp: None for tmp in q.css('div.tags a.tag::text').getall()}
            }

        next_page = response.css('ul.pager li.next a').attrib['href']
        if next_page is not None:
            next_page_url = 'http://quotes.toscrape.com' + next_page
            yield response.follow(next_page_url, callback=self.parse)