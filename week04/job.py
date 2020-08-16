import random

import pandas as pd
import pymysql

MYSQL_SETTINGS = {
    'host': 'localhost',
    'port': 3306,
    'user': '*******',
    'password': '*******',
    'db': '*******',
    'charset': 'utf8'
}

SQL_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS `{}`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `name` VARCHAR(255) NOT NULL,
   `age` INTEGER NOT NULL,
   PRIMARY KEY (`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
SQL_INSERT = """
INSERT INTO `{}`
(`name`, `age`)
VALUES 
('{}', '{}');
"""

SQL_INIT_TABLE = "DROP TABLE IF EXISTS {}"

db_conn = pymysql.connect(**MYSQL_SETTINGS)
db_cur = db_conn.cursor()
db_cur.execute(SQL_INIT_TABLE.format('data'))
db_cur.execute(SQL_INIT_TABLE.format('table1'))

db_cur.execute(SQL_CREATE_TABLE.format('data'))
db_cur.execute(SQL_CREATE_TABLE.format('table1'))

db_cur.close()
db_conn.commit()
db_conn.close()

db_conn = pymysql.connect(**MYSQL_SETTINGS)
db_cur = db_conn.cursor()
data_data = []
table1_data = []
for i in range(100):
    name = ''.join([chr(random.randint(97, 122)) for _ in range(3)])
    age = random.randint(20, 70)
    data_data.append([i + 1, name, age])
    db_cur.execute(SQL_INSERT.format('data', name, age))

for i in range(100):
    name = ''.join([chr(random.randint(97, 122)) for _ in range(3)])
    age = random.randint(20, 70)
    table1_data.append([i + 1, name, age])
    db_cur.execute(SQL_INSERT.format('table1', name, age))
db_cur.close()
db_conn.commit()
db_conn.close()

data = pd.DataFrame(data_data, columns=['id', 'name', 'age'])
table1 = pd.DataFrame(table1_data, columns=['id', 'name', 'age'])

# 1. SELECT * FROM data;
data

# 2. SELECT * FROM data LIMIT 10;
data.head(10)

# 3. SELECT id FROM data;  //id 是 data 表的特定一列
data.id

# 4. SELECT COUNT(id) FROM data;
data.id.count()

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
data[(data.id < 1000) & (data.age > 30)]

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
table1.groupby('id').age.nunique()

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(data, table1, on='id', how='inner')

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([data, table1]).drop_duplicates()

# 9. DELETE FROM table1 WHERE id=10;
table1[table1.id != 10]
table1.drop(table1[table1.id == 10].index)

# 10. ALTER TABLE table1 DROP COLUMN column_name;
table1.drop(['name'], axis=1)
table1.drop(columns=['name'])
