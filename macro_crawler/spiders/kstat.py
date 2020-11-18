import psycopg2
import requests
import json
import scrapy
from scrapy import Spider
from datetime import date
from helper import auth, dateutil
from database import manager, models, status
from macro_crawler.items import TimeseriesItem


class CementProduction(Spider):
    """시멘트협회의 웹페이지 테이블 데이터를 파싱"""

    name = "kr_cement_prod"
    params = {}

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(CementProduction, self).__init__(*args, **kwargs)
        if start_date is None:
            start_date = status.get_last_date(self.name)
        if end_date is None:
            end_date = date.today().strftime("%Y%m")
        self.start_date = start_date
        self.end_date = end_date
        self.params['start_date'] = start_date
        self.params['end_date'] = end_date

    def start_requests(self):
        if self.start_date < self.end_date:
            yield scrapy.Request(url='http://www.cement.or.kr/stati_2015/field_statistics.asp?sm=2_3_0', callback=self.select_year)
        else:
            return

    def select_year(self, response):
        start_year = int(self.start_date[:4])
        end_year = int(self.end_date[:4])
        for year in range(start_year, end_year+1):
            href = response.xpath('//*[@id="sub_contents"]/div[1]/ul/li/a[text()=$year]/@href', year=year).get()
            # Chaining requests. Since the url for current year is same as start url, add option dont_filter to avoid duplicates filter.
            yield scrapy.Request(response.urljoin(href), dont_filter=True, callback=self.parse_data, cb_kwargs={'year':year})

    def parse_data(self, response, year):
        monthly_values = zip(response.xpath('//*[@id="sub_contents"]/div[3]/table/tbody/tr//td[1]//text()').getall(), response.xpath('//*[@id="sub_contents"]/div[3]/table/tbody/tr//td[2]//text()').getall())
        for month, data in monthly_values:
            if '월' in month:
                yield TimeseriesItem(date=str(year)+str(month.replace('월','')).zfill(2), value=float(data.replace(',','')))
