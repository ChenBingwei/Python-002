# 学习笔记

## 多进程

产生新的进程常用`os.fork()`或者`multiprocessing.Process()`

### 创建进程

#### os.fork()

可以使用`os.fork()`来创建，如下：

```python
import os
os.fork()
print('111')
## 输出结果
## 111
## 111
```

父进程和新建的子进程都会运行`print('111')`，可通过返回值来判断父子进程关系，`os.fork()`函数返回值为0表示子进程，否则为对应父进程，可通过`os.getpid()`和`os.getppid()`来获取当前进程和其父进程的进程id。

#### multiprocessing.Process()

```Python
from multiprocessing imort Process
def f(name):
  print(f'hello {name}') # python3.6以上支持该语法

if __name__ == '__main__':
  p = Process(target=f, args=('john',))
  p.start()
  p.join() # 默认阻塞
```

p.join([timeout])表示合并进程，会阻塞timeout秒，终止或超时最后均返回None；

⚠️注意：

1、可通过检查进程的exitcode确定该进程是否终止；

2、合并进程必须在启动进程之后；

3、一个进程可多次合并，但不可并入自身，会导致死锁；

```python
from multiprocessing import Process

p = Process()
p.start() # 启动子进程
p.join() # 阻塞，等待子进程结束
p.terminate() # 强制结束子进程
```



### multiprocessing模块

```python
multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={})
# - group：分组，实际上很少使用
# - target：表示调用对象，你可以传入方法的名字, 当不给Process指定target时，会默认调用Process类里的run()方法。
# - name：别名，相当于给这个进程取一个名字
# - args：表示被调用对象的位置参数元组，比如target是函数a，他有两个参数m，n，那么args就传入(m, n)即可
# - kwargs：表示调用对象的字典
```

`multiprocessing.children()`返回激活的子进程

`multiprocessing.cpu_count()`返回cpu核数，一般创建的进程数和cpu核数相同，理论上效率最大化

### 多进程之间的通信

#### 队列

```python
from multiprocessing import Queue

q = Queue()
# 先入先出
# put和get是队列最常用的两个功能
q.put([42, None, 'hello'])
print(q.get())    # prints "[42, None, 'hello']"
```

`q.get()`方法有两个重要参数block和timeout，block为True时，get对空队列会等待timeout时间后抛出`queue.Empty`异常；若为False，get对空队列会直接抛出`queue.Empty`异常。

`q.put()`方法也有同样的block和timeout参数，在队列满的场景下处理逻辑同get类似，抛出异常为`queue.Full`。

#### 管道和共享内存

队列的底层就是使用的管道

```python
from multiprocessing import Pipe

parent_conn, child_conn = Pipe()
# 返回的两个连接对象 Pipe() 表示管道的两端。
# 每个连接对象都有 send() 和 recv() 方法（相互之间的）。
# 请注意，如果两个进程（或线程）同时尝试读取或写入管道的 同一 端，
# 则管道中的数据可能会损坏。当然，同时使用管道的不同端的进程不存在损坏的风险。
```

变量是写在每个进程的内存中，多个进程共享一块内存，即可实现多进程之间的通信， 在进行并发编程时，通常最好尽量避免使用共享状态。

```python
from multiprocessing import Value, Array
# 共享内存 shared memory 可以使用 Value 或 Array 将数据存储在共享内存映射中
# 这里的Array和numpy中的不同，它只能是一维的，不能是多维的。
# 同样和Value 一样，需要定义数据形式，否则会报错
num = Value('d', 0.0)
arr = Array('i', range(10))
```

## 锁

安全的进程和线程，指的是线程和进程的表现和它最终期望的结果是一致的。队列就是进程安全的。

```python
from multiprocessing import Lock

l = Lock()
l.acquire() # 锁住
for _ in range(5):
  pass
l.release() # 释放
```

