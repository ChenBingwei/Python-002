# 第二周学习笔记

## 异常处理

异常捕获过程：

1. 异常类把错误消息打包到一个对象（`traceback`）
2. 该对象会自动查找到调用栈
3. 直到运行系统找到明确的声明如何处理这些类异常的位置

堆栈信息可通过`pretty_errors`模块来美化。



## 数据库连接

1. 在直接连接数据库的方法中，PyMySQL模块连接更加稳定
2. PyMySQL连接数据库总体流程为：开始-->创建connection-->获取cursor-->sql语句-->关闭cursor-->关闭connection-->结束
3. ORM隐藏了数据访问细节，“封闭”的通用数据库交互，并通过对象模型构造关系数据库结构；但性能略有降低且对于复杂查询支持有限



## 反爬虫

1. 可通过requests的post请求获取登陆cookies，也可通过Selenium来模拟浏览器操作完成
2. 可通过tesseract+语言识别库来完成对验证码的认证
3. 结合scrapy框架中中间件模块可实现IP代理以及请求异常处理功能
4. 大文件下载方案：

```python
# 所以为了防止内存不够用的现象出现，我们要想办法把下载的文件分块写到磁盘中。
import requests
file_url = "http://python.xxx.yyy.pdf"
r = requests.get(file_url, stream=True)
with open("python.pdf", "wb") as pdf:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            pdf.write(chunk)
```



## 分布式爬虫

分布式爬虫可通过scrapy+redis来实现，利用redis实现队列和管道的共享，主要方式为：

1. 使用RedisSpider类替代Spider类
2. Scheduler的queue交由Redis实现
3. item pipeline交由Redis实现



