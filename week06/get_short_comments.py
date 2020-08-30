import requests
from lxml import etree
import re
import pymysql

MYSQL_SETTINGS = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '*********',
    'db': 'chenbw',
    'charset': 'utf8mb4'
}

SQL_INSERT = """
INSERT INTO `the_eight_hundred`
(`comment`, `star`, `time`)
VALUES 
('{}', '{}','{}');
"""

payload = {}
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/85.0.4183.83 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://movie.douban.com/subject/26754233/?from=showing',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}
db_conn = pymysql.connect(**MYSQL_SETTINGS)
db_cur = db_conn.cursor()

for i in range(0, 5):
    url = "https://movie.douban.com/subject/26754233/comments?start={}&limit=20&sort=new_score&status=P".format(i * 20)

    response = requests.request("GET", url, headers=headers, data=payload)
    html = etree.HTML(response.text)

    comments = html.xpath('//*[@class="comment-item"]')
    for comment in comments:
        try:
            time = comment.xpath('./div[2]/h3/span[2]/span[3]/text()')[0]
            time = re.sub(r'[^\w-]', '', time)
            star = comment.xpath('./div[2]/h3/span[2]/span[2]/@class')[0]
            star = int(re.sub(r'[^\d]', '', star)) / 10
            short = comment.xpath('./div[2]/p/span/text()')[0]
        except Exception as e:
            continue
        db_cur.execute(SQL_INSERT.format(short, star, time))

db_cur.close()
db_conn.commit()
db_conn.close()
