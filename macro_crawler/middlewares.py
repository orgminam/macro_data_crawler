# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from database import status
import json
import traceback

class MacroCrawlerSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        """스파이더 작업 성공 후 실행되는 훅"""

        # Called with the results returned from the Spider, after
        # it has processed the response.
        spider.logger.info(f"Add success log for {spider.name}")
        status.update_success_hist(spider.name, json.dumps(spider.params))
        # Must return an iterable of Request, or item objects.
        # yield to pipeline
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        """응답 프로세싱중 예외 발생시 실행되는 훅"""

        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.
        spider.logger.error(f"Add response-error log for {spider.name}")     
        status.update_error_hist(
            spider.name,
            str(exception),
            json.dumps(spider.params),
            "".join(traceback.format_tb(exception.__traceback__))
        )
        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        pass


class MacroCrawlerDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        """요청 프로세싱중 예외 발생시 실행되는 훅"""

        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.
        
        if not hasattr(spider, "err_logged"):
            spider.logger.error(f"Add request-error log for {spider.name}")     
            status.update_error_hist(
                spider.name,
                str(exception),
                json.dumps(spider.params),
                "".join(traceback.format_tb(exception.__traceback__))
            )
            spider.err_logged = True
        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        pass
