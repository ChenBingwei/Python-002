# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from itemadapter import ItemAdapter


class SmzdmTop10Pipeline:
    SQL_CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS `smzdm_shampoo`(
       `id` INT UNSIGNED AUTO_INCREMENT,
       `shampoo_rank` VARCHAR(255) NOT NULL,
       `shampoo_name` VARCHAR(255) NOT NULL,
       `shampoo_evaluate` VARCHAR(255) NOT NULL,
       `shampoo_comments` VARCHAR(255) NOT NULL,
       `created_time` timestamp NULL DEFAULT current_timestamp(),
       PRIMARY KEY (`id`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    SQL_INIT_TABLE = "DELETE FROM smzdm_shampoo"
    SQL_INSERT = """
    INSERT INTO smzdm_shampoo
    (`shampoo_rank`, `shampoo_name`, `shampoo_evaluate`, `shampoo_comments`)
    VALUES 
    ('{}', '{}', '{}', '{}');
    """

    def process_item(self, item, spider):

        try:
            db_cur = self.db_conn.cursor()
            cmd = self.SQL_INSERT.format(
                item['shampoo_rank'],
                item['shampoo_name'],
                item['shampoo_evaluate'],
                '||'.join(item['shampoo_comments'])
            )
            db_cur.execute(cmd)
            db_cur.close()
        except Exception as e:
            print(e)
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
