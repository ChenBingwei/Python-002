说明：数据库语句中的表名就是对应pandas.DataFrame的名字

```python
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
table1.groupby('id').order_id.nunique()

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
pd.merge(table1, table2, on='id', how='inner')

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([table1, table2]).drop_duplicates()

# 9. DELETE FROM table1 WHERE id=10;
table1[table1.id != 10]
# or
table1.drop(table1[table1.id == 10].index)

# 10. ALTER TABLE table1 DROP COLUMN column_name;
table1.drop(['column_name'], axis=1)
# or
table1.drop(columns=['column_name'])
```

