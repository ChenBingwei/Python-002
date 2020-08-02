# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

import pandas as pd
import pymysql


class Job1PipelineToMysql:
    SQL_CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS `maoyan_movies`(
       `id` INT UNSIGNED AUTO_INCREMENT,
       `movie_name` VARCHAR(255) NOT NULL,
       `movie_type` VARCHAR(255) NOT NULL,
       `movie_rank` VARCHAR(255) NOT NULL,
       `movie_time` VARCHAR(255) NOT NULL,
       PRIMARY KEY (`id`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    SQL_INIT_TABLE = "DELETE FROM maoyan_movies"
    SQL_INSERT = """
    INSERT INTO maoyan_movies
    (`movie_name`, `movie_type`, `movie_rank`, `movie_time`)
    VALUES 
    ('{}', '{}', '{}', '{}');
    """

    def process_item(self, item, spider):

        try:
            db_cur = self.db_conn.cursor()
            db_cur.execute(
                self.SQL_INSERT.format(
                    item['movie_name'],
                    item['movie_type'],
                    item['movie_rank'],
                    item['movie_time'],
                )
            )
            db_cur.close()
        except:
            self.db_conn.rollback()

        return item

    def open_spider(self, spider):
        mysql_settings = spider.settings.get('MYSQL_SETTINGS')

        self.db_conn = pymysql.connect(**mysql_settings)
        db_cur = self.db_conn.cursor()
        try:
            db_cur.execute(self.SQL_CREATE_TABLE)
            db_cur.execute(self.SQL_INIT_TABLE)
            db_cur.close()
        except:
            self.db_conn.rollback()

    def close_spider(self, spider):
        self.db_conn.commit()
        self.db_conn.close()


class Job1PipelineToCsv:
    OUTPUT_PATH = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'output/job2_output_maoyan_top10.csv'
    )

    def process_item(self, item, spider):
        movie_info = (
            item['movie_rank'],
            item['movie_name'],
            item['movie_type'],
            item['movie_time'],
        )
        pd_info = pd.DataFrame(data=[movie_info])
        if not os.path.exists(self.OUTPUT_PATH):
            # Add the first line of content when writing for the first time
            pd_info.to_csv(self.OUTPUT_PATH, encoding='utf8', index=False,
                           header=['排名', '电影名称', '电影类型', '上映时间'])
        else:
            pd_info.to_csv(self.OUTPUT_PATH, encoding='utf8', mode='a',
                           index=False, header=False)

        return item

    def open_spider(self, spider):
        # When the spider starts, delete the previous output file
        if os.path.exists(self.OUTPUT_PATH):
            os.remove(self.OUTPUT_PATH)

    def close_spider(self, spider):
        # Before the spider ends, sort the output files according to the ranking
        if os.path.exists(self.OUTPUT_PATH):
            sourted_csv = pd.read_csv(self.OUTPUT_PATH, index_col='排名', parse_dates=True).sort_index()
            sourted_csv.to_csv(self.OUTPUT_PATH)
