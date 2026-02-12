# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NewsCrawlerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        if adapter.get('title'):
            adapter['title'] = adapter['title'].strip()

        if adapter.get('link') and not adapter['link'].startswith('http'):
            adapter['link'] = spider.start_urls[0] + adapter['link']
        
        if adapter.get('summary'):
            adapter['summary'] = " ".join(adapter['summary'].split())

        return item
