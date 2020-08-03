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