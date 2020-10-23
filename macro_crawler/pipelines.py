# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from macro_crawler.items import TimeseriesItem
from scrapy.exceptions import DropItem
from helper.dateutil import LastDateCollector
from database import manager, models, status


class MacroCrawlerPipeline:

    sess = manager.Session()
    ldc = LastDateCollector()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if isinstance(item, TimeseriesItem) and adapter.get('date') and adapter.get('value'):
            date = adapter['date']
            value = adapter['value']
            obj = models.MacroData(
                id=spider.name, date=date, value=value)
            self.ldc.update(date)
            self.sess.merge(obj)
            self.sess.commit()
            status.update_last_date(spider.name, self.ldc.get())
        else:
            raise DropItem(f"Invalid data {item}")
        return item
