# Macro Crawler
The set of crawling programs on each economic site.
Every single spider represents how it crawl the data from the variant sources.
This project's point of view.
- spiders for each site
- database model
- exception handler for request/response
- key management
- job history
- configurable&extensible
- cron scheduling

# Run and Tests Spiders
```
scrapy crawl <spider_name(eg. kr_cpi)> -a arg1=value1
eg. scrapy crawl kr_cpi -a start_date=202006
```

# Cron job scheduling
Scrapydweb conducts this using (clustered)scrapy and its cron scheduler.
To deploy
```
scrapyd-deploy macro_crawler -p macro_crawler
```

# To inspect response itself
insert codes below ahead of any response
```
from scrapy.shell import inspect_response
inspect_response(response, self)
```