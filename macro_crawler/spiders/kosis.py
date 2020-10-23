import psycopg2
import requests
import json
import scrapy
from scrapy import Spider
from datetime import date
from helper import auth, dateutil
from database import manager, models, status
from macro_crawler.items import TimeseriesItem

url = "http://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList"
sess = manager.Session()


def get_params(id, start_date, end_date):
    master_data = sess.query(models.Master).filter_by(id=id).first()
    param_copy = master_data.params.copy()
    param_copy["startPrdDe"] = start_date
    param_copy["endPrdDe"] = end_date
    param_copy["jsonVD"] = "Y"
    param_copy["format"] = "json"
    param_copy["apiKey"] = auth.get_key("kosis")
    return param_copy


class CommonKosisSpider(Spider):
    """일반적인 형태의 통계청 API 호출 슈퍼클래스"""

    def __init__(self, start_date=None, end_date=None, *args, **kwargs):
        super(CommonKosisSpider, self).__init__(*args, **kwargs)
        if start_date is None:
            start_date = status.get_last_date(self.name)
        if end_date is None:
            end_date = date.today().strftime("%Y%m")
        self.start_date = start_date
        self.end_date = end_date
        self.params = get_params(self.name, start_date, end_date)

    def start_requests(self):
        if self.start_date < self.end_date:
            yield scrapy.http.FormRequest(url=url, method="GET", formdata=self.params, callback=self.parse)
        else:
            return


class CpiSpider(CommonKosisSpider):
    """소비자 물가지수 수집
    SAMPLE: http://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=AAA&format=json&jsonVD=Y&userStatsId=kallsu/101/DT_1J17009/2/1/20200909140243_1&prdSe=M&newEstPrdCnt=3
    """

    name = "kr_cpi"
    
    def parse(self, response):
        data = json.loads(response.body)
        date_parser = dateutil.DateParser("%Y%m", "M")
        for row in data:
            date_parser.update(row["PRD_DE"])
            value = float(row["DT"])
            yield TimeseriesItem(
                date=date_parser.get(), value=value)
            

class CoreCpiSpider(CommonKosisSpider):
    """근원 소비자 물가지수
    SAMPLE: http://kosis.kr/openapi/statisticsData.do?method=getList&apiKey=AAA&format=json&jsonVD=Y&userStatsId=kallsu/101/DT_1J17009/2/1/20200909140243_2&prdSe=M&startPrdDe=199001&endPrdDe=202008
    """

    name = "kr_core_cpi"

    def parse(self, response):
        data = json.loads(response.body)
        date_parser = dateutil.DateParser("%Y%m", "M")
        for row in data:
            date_parser.update(row["PRD_DE"])
            value = float(row["DT"])
            yield TimeseriesItem(
                date=date_parser.get(), value=value)
