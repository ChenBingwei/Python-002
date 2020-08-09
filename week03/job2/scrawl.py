# -*- coding: utf-8 -*-

import multiprocessing
import os
import random
import re
import sys
import threading
import time
from concurrent.futures import ProcessPoolExecutor
from queue import Queue

import matplotlib.pyplot as plt
import pymysql
import requests
from lxml import etree

"""
说明：
1、在 MYSQL_SETTINGS 中修改对应数据库配置信息以及 HEADERS 中 cookies 和 user-agnent 信息；
2、在macos系统上执行，建议先执行 export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES；
   目的是为了设置环境变量以允许在新的Mac OS High Sierra安全规则下使用多线程应用程序或脚本
3、然后在命令行运行 python scrawl.py 即可
"""

MYSQL_SETTINGS = {
    'host': 'localhost',
    'port': 3306,
    'user': '*********',
    'password': '*********',
    'db': '*********',
    'charset': 'utf8'
}

SQL_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS `work_position`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `work_city` VARCHAR(255) NOT NULL,
   `work_position` VARCHAR(255) NOT NULL,
   `work_salary` VARCHAR(255) NOT NULL,
   PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

SQL_INIT_TABLE = "DELETE FROM work_position"
SQL_INSERT = """
INSERT INTO work_position
(`work_city`, `work_position`, `work_salary`)
VALUES 
('{}', '{}', '{}');
"""
SELECT_SQL = "select * from work_position where work_city='{}'"

HEADERS = {
    'authority': 'www.lagou.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'RECOMMEND_TIP=true; _ga=GA1.2.1593259044.1591960182; '
              'user_trace_token=20200612190942-b307dbf5-db59-457e-90a1-b9f7447d8747; '
              'LGUID=20200612190942-7f3fad81-a743-4638-9859-0e87a850605b; '
              'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22172a839469a87d-0ab2f5fa286a15-143f6257-1296000'
              '-172a839469bbe6%22%2C%22%24device_id%22%3A%22172a839469a87d-0ab2f5fa286a15-143f6257-1296000'
              '-172a839469bbe6%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6'
              '%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22'
              '%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5'
              '%BC%80%22%7D%7D; JSESSIONID=ABAAABAABAGABFA875DFE79A56A4EB3424876F05C122A25; '
              'WEBTJ-ID=20200809093501-173d0db541d5bf-077bc0e1bc86ec-31677305-1296000-173d0db541eb5d; '
              'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1596936902; _gid=GA1.2.160269641.1596936902; '
              'X_MIDDLE_TOKEN=d99a38f89653829e26dd86b9fde1b04a; TG-TRACK-CODE=index_navigation; '
              'LGSID=20200809175817-cc85ea5e-8d81-4bd4-9df5-697b92e47114; PRE_UTM=; PRE_HOST=; PRE_SITE=; '
              'PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fsignature'
              '%3DBA5E9A14EC8AABFB3771A38F14E8243F%26service%3Dhttp%25253A%25252F%25252Fwww.lagou.com%25252Fbeijing'
              '-zhaopin%25252FPython%25252F1%252527%26action%3Dlogin%26serviceId%3Dlagou%26ts%3D1596967096774; '
              'sm_auth_id=ue610o160rg355so; '
              'gate_login_token=9608b166485400f7deab4d616a8cfc11b4a1febfdc5befa35e7643047b41e3d9; '
              '_putrc=5EF00C60F980CA74123F89F2B170EADC; login=true; unick=%E9%99%88%E7%A7%89%E8%94%9A; '
              'showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=1; '
              'privacyPolicyPopup=false; X_HTTP_TOKEN=c8613e5cf378c55c6417696951a3c0817ee539c37f; '
              'index_location_city=%E5%85%A8%E5%9B%BD; _gat=1; SEARCH_ID=1c7d2d52662f44fc90ace77df26e58f7; '
              'LGRID=20200809180006-9b828a3f-b31f-439d-8bda-dd33356f111c; '
              'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1596967206',
}


def calculate_average_monthly_salary(salary):
    """
    Take the average of the minimum and maximum salary
    :param salary:
    :return:
    """
    salary = re.sub(r'[^\d+\·-]', '', salary)
    salary_list = list(map(int, re.split(r'[-\·]', salary)))
    monthly_salary = sum(salary_list[:2]) / 2
    return monthly_salary


def handle_result_from_db():
    result_dict = {
        'beijing': '',
        'guangzhou': '',
        'shanghai': '',
        'shenzhen': '',
    }
    db_conn = pymysql.connect(**MYSQL_SETTINGS)
    db_cur = db_conn.cursor()
    for key in result_dict.keys():
        print(SELECT_SQL.format(key))
        db_cur.execute(SELECT_SQL.format(key))
        list_info = [calculate_average_monthly_salary(i[3]) for i in db_cur.fetchall()]
        result_dict[key] = sum(list_info) / len(list_info)
    db_cur.close()
    db_conn.close()
    return result_dict


def plot():
    try:
        result_dict = handle_result_from_db()
        x_ticks = []
        y = []
        for (key, value) in result_dict.items():
            x_ticks.append(key)
            y.append(value)

        plt.bar(range(4), y, color='rgbc')
        for x, y in zip(range(4), y):
            plt.text(x + 0.02, y + 1, '{}k'.format(round(y, 2)), ha='center', va='bottom')

        plt.xticks(range(4), x_ticks)
        plt.xlabel('City')
        plt.ylabel('Salary/month(k)')

        plt.ylim((0, 30))
        plt.title("Python programmer average monthly salary statistics")
        plt.savefig('./result.jpg')
        plt.show()

    except Exception as e:
        print(f'Failed to plot:{e}')


class CrawlThread(threading.Thread):
    """
    爬虫类
    """

    def __init__(self, city, thread_id, queue):
        super().__init__()
        self.city = city
        self.thread_id = thread_id
        self.queue = queue

    def run(self):
        print(f'开始爬虫线程：{self.thread_id} pid:{os.getpid()}')
        self.scheduler()
        print(f'结束爬虫线程：{self.thread_id} pid:{os.getpid()}')

    # 模拟任务调度
    def scheduler(self):
        while True:
            if self.queue.empty():  # 队列为空不处理
                break
            else:
                page = self.queue.get()
                url = f'https://www.lagou.com/{self.city}-zhaopin/Python/{page}'
                try:
                    # downloader 下载器
                    # 随机等待1-10秒
                    time.sleep(random.randint(1, 10))
                    response = requests.get(url, headers=HEADERS)

                    dataQueue.put((self.city, response))
                except Exception as e:
                    print('下载出现异常', e)


class ParserThread(threading.Thread):
    '''
    页面内容分析
    '''

    def __init__(self, thread_id, queue, db_api):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = queue
        self.db_api = db_api

    def run(self):
        print(f'启动分析线程：{self.thread_id} pid:{os.getpid()}')
        while not flag:
            try:
                item = self.queue.get(False)
                if not item:
                    continue
                self.parse_data(item)
                self.queue.task_done()
            except Exception as e:
                pass
        print(f'结束分析线程：{self.thread_id} pid:{os.getpid()}')

    def parse_data(self, item):
        '''
        解析网页内容的函数
        :param item:
        :return:
        '''
        try:
            db_cursor = self.db_api.cursor()
            html = etree.HTML(item[1].text)
            print(html.text)
            works = html.xpath('//*[@id="s_position_list"]/ul/li')
            for work in works:
                result = (
                    item[0],
                    work.attrib.get('data-positionname').lower(),
                    work.attrib.get('data-salary').lower()
                )

                if not result in city_result:
                    # Since variables are shared between multiple processes,
                    # they are used for deduplication
                    city_result.add(result)
                    try:
                        db_cursor.execute(SQL_INSERT.format(*result))
                        self.db_api.commit()
                    except Exception as e:
                        print(e)
                        self.db_api.rollback()

        except Exception as e:
            print('page error', e)


dataQueue = Queue()
flag = False
city_result = set()


def start_scrawler(city):
    # Since variables are shared between multiple processes,
    # they are used for deduplication
    global city_result
    global flag
    db_connect_in_process = pymysql.connect(**MYSQL_SETTINGS)

    print('进程 %s 开始' % os.getpid())
    pageQueue = Queue(20)
    # 取10个页面
    for page in range(1, 11):
        pageQueue.put(page)

    # 爬虫线程
    crawl_threads = []
    crawl_name_list = ['crawl_1', 'crawl_2', 'crawl_3']
    for thread_id in crawl_name_list:
        thread = CrawlThread(city, thread_id, pageQueue)
        thread.start()
        crawl_threads.append(thread)

    # 解析线程

    parse_thread = []
    parser_name_list = ['parse_1', 'parse_2', 'parse_3']
    for thread_id in parser_name_list:
        thread = ParserThread(thread_id, dataQueue, db_connect_in_process)
        thread.start()
        parse_thread.append(thread)

    # 结束crawl线程
    for t in crawl_threads:
        t.join()

    # 结束parse线程
    flag = True
    for t in parse_thread:
        t.join()
    db_connect_in_process.close()

    print('进程 %s 结束' % os.getpid())


def main():
    try:
        city_list = ['beijing', 'shanghai', 'guangzhou', 'shenzhen']
        process_number = 4 if multiprocessing.cpu_count() >= 4 else multiprocessing.cpu_count()
        with ProcessPoolExecutor(process_number) as Executor:
            Executor.map(start_scrawler, city_list)

        # 画图
        plot()

    except KeyboardInterrupt as e:
        print(f'Caught: {e}, aborting')
        sys.exit(0)
    except IOError as e:
        print(f'IOError occured: {e}')
        sys.exit(0)
    except Exception as e:
        print(f'Error : {e}', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    db_conn = pymysql.connect(**MYSQL_SETTINGS)
    db_cur = db_conn.cursor()
    db_cur.execute(SQL_CREATE_TABLE)
    db_cur.execute(SQL_INIT_TABLE)
    db_cur.close()
    db_conn.commit()
    db_conn.close()
    main()
