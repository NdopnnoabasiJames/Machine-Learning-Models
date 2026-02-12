import scrapy
from news_crawler.items import NewsCrawlerItem
from urllib.parse import urljoin 


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["nbcnews.com"]
    start_urls = [
        "https://www.nbcnews.com",
    ]

    def parse(self, response):
        headlines = response.css("article a, .headline a, h2 a, h3 a")
        seen_links = set()

        for headline in headlines:
            item = NewsCrawlerItem()

            link = headline.css("::attr(href)").get()
            if link:
                link = urljoin(response.url, link)

                if link in seen_links:
                    continue
                seen_links.add(link)

            title = headline.css('span::text, ::text').get()
            if not title:
                title = headline.css('::text').get()
            if not title:
                title = headline.xpath("./ancestor::article//h2/text() | ./ancestor::article//h3/text()").get()
            
            if title and link and 'nbcnews.com' in link:
                item['title'] = title.strip()
                item['link'] = link.strip()
                item['source'] = 'NBC News'

                yield scrapy.Request(
                    link,
                    callback=self.parse_article,
                    meta={'item': item}
                )
    def parse_article(self, response):
        item = response.meta['item']

        date = response.css("meta[name='pubdate']::attr(content), meta[property='article:published_time']::attr(content)").get()
        if date:
            item['date'] = date.strip()

        summary = response.css("meta[name='description']::attr(content)").get()
        if summary:
            item['summary'] = summary.strip()
        else:
            paragraphs = response.css("article p::text").getall()
            if paragraphs:
                item['summary'] = " ".join(paragraphs).strip()

        yield item
        
            
         