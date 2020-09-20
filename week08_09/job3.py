# 作业三：
# 实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。

import random
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func_return = func(*args, **kwargs)
        end = time.time()
        print('{}() execute time: {}s'.format(func.__name__, end - start))
        return func_return

    return wrapper


@timer
def test_function(n):
    time.sleep(n)


if __name__ == '__main__':
    sleep_number = random.randint(0, 10)
    print('Sleep time is {}'.format(sleep_number))
    test_function(sleep_number)
