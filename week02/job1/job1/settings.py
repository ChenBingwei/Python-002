# Scrapy settings for job1 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'job1'

SPIDER_MODULES = ['job1.spiders']
NEWSPIDER_MODULE = 'job1.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 ' \
             '(KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 1

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://passport.meituan.com/account/secondverify?response_code=eefe3221070446419d4ee2a8d2c273e5'
               '&request_code=177189ef4ab84626a820318623825a28',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

COOKIES = {
    '__mta': '247430459.1595344111315.1595730288881.1595731455201.31',
    'uuid_n_v': 'v1',
    'uuid': '094DC040CB6411EA8A8375094482DFA4D0297F2A867F4419A03E2C61639BE876',
    'mojo-uuid': 'bfd678e2d91dd41560a8f1276904bfc8',
    '_lxsdk_cuid': '17371eb4681c8-0c283695860a77-31617402-13c680-17371eb4681c8',
    '_lxsdk': '094DC040CB6411EA8A8375094482DFA4D0297F2A867F4419A03E2C61639BE876',
    '_csrf': '23fc3bdfb0ef760942d493b14362cbb48e95303219d30ccf1dee412d00f51a0c',
    '_lx_utm': 'utm_source%3Dgoogle%26utm_medium%3Dorganic',
    'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2': '1595730279,1595738375,1596337856,1596350074',
    'mojo-session-id': '{"id":"847bd0a672be5499e331b9791f1c6ca9","time":1596376220673}',
    'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2': '1596376354',
    'mojo-trace-id': '15',
    '_lxsdk_s': '173af70045c-fef-c0-ff5%7C%7C24',
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'job1.middlewares.Job1DownloaderMiddleware': 200,
    'job1.middlewares.RandomHttpProxyMiddleware': 400
}
#
HTTP_PROXY_LIST = [
    'http://52.179.231.206:80',
    'http://95.0.194.241:9090',
    'http://180.109.127.80:4216',
    'http://123.125.114.21:80',
    'http://163.177.151.224:80',
    'http://101.37.118.54:8888',
    'http://117.185.16.253:80',
    'http://183.60.191.100:80'
]

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'job1.pipelines.Job1PipelineToCsv': 300,
    'job1.pipelines.Job1PipelineToMysql': 400,
}

# Replace the following account password database
MYSQL_SETTINGS = {
    'host': 'localhost',
    'port': 3306,
    'user': '********',
    'password': '********',
    'db': '********',
    'charset': 'utf8'
}
