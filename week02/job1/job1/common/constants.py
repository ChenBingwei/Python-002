# -*- coding: utf-8 -*-

"""
Constants used in job1
"""
import os
import re

OUTPUT_PATH = os.path.join(
    re.sub(r'common/constants.py', '', os.path.abspath(__file__)),
    'output/job2_output_maoyan_top10.csv')

MAOYAN_BASE_URL = 'https://maoyan.com'

# Replace the following cookies
COOKIES = {
    '__mta': '247430459.1595344111315.1595730288881.1595731455201.31',
    'uuid_n_v': 'v1',
    'uuid': '094DC040CB6411EA8A8375094482DFA4D0297F2A867F4419A03E2C61639BE876',
    'mojo-uuid': 'bfd678e2d91dd41560a8f1276904bfc8',
    '_lxsdk_cuid': '17371eb4681c8-0c283695860a77-31617402-13c680-17371eb4681c8',
    '_lxsdk': '094DC040CB6411EA8A8375094482DFA4D0297F2A867F4419A03E2C61639BE876',
    '_csrf': '23fc3bdfb0ef760942d493b14362cbb48e95303219d30ccf1dee412d00f51a0c',
    'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2': '1595679031,1595730279,1595738375,1596337856',
    '_lx_utm': 'utm_source%3Dgoogle%26utm_medium%3Dorganic',
    'mojo-session-id': '{"id":"56b3f364abb87314947a502f726fe4a9","time":1596349807614}',
    'mojo-trace-id': '2',
    'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2': '1596349869',
    '_lxsdk_s': '173addce8be-996-a16-d4e%7C%7C5',
}

PARAMS = (
    ('showType', '3'),
)

# MYSQL
# The database structure is as follows
# mysql> describe maoyan_movies;
# +------------+--------------+------+-----+---------+----------------+
# | Field      | Type         | Null | Key | Default | Extra          |
# +------------+--------------+------+-----+---------+----------------+
# | id         | int unsigned | NO   | PRI | NULL    | auto_increment |
# | movie_name | varchar(255) | NO   |     | NULL    |                |
# | movie_type | varchar(255) | NO   |     | NULL    |                |
# | movie_rank | varchar(255) | NO   |     | NULL    |                |
# | movie_time | varchar(255) | NO   |     | NULL    |                |
# +------------+--------------+------+-----+---------+----------------+
# 5 rows in set (0.00 sec)
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
# mysql> select * from maoyan_movies;
# +----+-----------------------------+-----------------------------------+------------+------------+
# | id | movie_name                  | movie_type                        | movie_rank | movie_time |
# +----+-----------------------------+-----------------------------------+------------+------------+
# |  1 | 釜山行2：半岛               | 动作／惊悚                        | 1          | 2020-08-12 |
# |  2 | 活着                        | 动作／惊悚／灾难                  | 2          | 2020-06-24 |
# |  3 | 星际穿越                    | 剧情／科幻／冒险                  | 3          | 2020-08-02 |
# |  4 | 抵达之谜                    | 剧情／爱情／青春                  | 4          | 2020-07-31 |
# |  5 | 误杀                        | 剧情／犯罪                        | 5          | 2020-07-20 |
# |  6 | 妙先生                      | 动画／奇幻／冒险                  | 6          | 2020-07-31 |
# |  7 | 唐人街探案2                 | 喜剧／动作／悬疑                  | 7          | 2018-02-16 |
# |  8 | 天气之子                    | 爱情／动画／奇幻                  | 8          | 2019-11-01 |
# |  9 | 最美逆行                    | 剧情                              | 9          | 2020-06-28 |
# | 10 | 大话西游之大圣娶亲          | 喜剧／爱情／奇幻／古装            | 10         | 2020-07-24 |
# +----+-----------------------------+-----------------------------------+------------+------------+
# 10 rows in set (0.00 sec)
