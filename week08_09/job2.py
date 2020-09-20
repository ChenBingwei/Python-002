# 作业二：
# 自定义一个 python 函数，实现 map() 函数的功能。

from collections.abc import Iterable


class MyMap:

    def __init__(self, func, *args):
        self.iterators = args
        self.func = func
        if not callable(self.func):
            raise TypeError("'{}' object is not callable.".format(type(self.func)))
        for iterator in self.iterators:
            if not isinstance(iterator, Iterable):
                raise TypeError("'{}' object is not Iterable.".format(type(iterator)))

    def __iter__(self):
        return self.generator()

    def generator(self):
        iterators, func = self.iterators, self.func

        try:
            i = 0
            while 1:
                yield func(*[j[i] for j in iterators])
                i += 1
        except IndexError:
            pass


if __name__ == '__main__':
    test_list = list(range(0, 10))
    map_list = MyMap(str, test_list)
    print(list(map_list))
