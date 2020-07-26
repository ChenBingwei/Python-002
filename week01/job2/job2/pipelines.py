# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

import pandas as pd

from job2 import constants


class Job2Pipeline:

    def process_item(self, item, spider):
        movie_info = (
            item['movie_rank'],
            item['movie_name'],
            item['movie_type'],
            item['movie_time'],
        )
        pd_info = pd.DataFrame(data=[movie_info])
        if not os.path.exists(constants.OUTPUT_PATH):
            # Add the first line of content when writing for the first time
            pd_info.to_csv(constants.OUTPUT_PATH, encoding='utf8', index=False,
                           header=['排名', '电影名称', '电影类型', '上映时间'])
        else:
            pd_info.to_csv(constants.OUTPUT_PATH, encoding='utf8', mode='a',
                           index=False, header=False)

        return item

    def open_spider(self, spider):
        # When the spider starts, delete the previous output file
        if os.path.exists(constants.OUTPUT_PATH):
            os.remove(constants.OUTPUT_PATH)

    def close_spider(self, spider):
        # Before the spider ends, sort the output files according to the ranking
        sourted_csv = pd.read_csv(constants.OUTPUT_PATH, index_col='排名', parse_dates=True).sort_index()
        sourted_csv.to_csv(constants.OUTPUT_PATH)
