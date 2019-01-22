import re
import datetime
import random
import time
from queue import Queue
import threading
from pathlib import Path
import sys


# 数据源
ops = {
    'datetime': lambda strdate: datetime.datetime.strptime(strdate, '%d/%b/%Y:%H:%M:%S %z'),
    'status': int,
    'length': int
}

logexample = '''183.69.210.164 - - [07/Apr/2017:09:32:46 +0800] "GET /app/template/default//style/css.css HTTP/1.1" 200 8803 "http://job.magedu.com/index.php?m=login" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"'''
pattern='''(?P<remote>[\d.]+) - - \[(?P<datetime>[^\[\]]+)\] "(?P<method>\w+) (?P<url>\S+) (?P<protocol>[\w/.]+)" (?P<status>\d+) (?P<length>\d+) "(?P<exp>[^"]+)" "(?P<useragent>[^"]+)"'''
regex = re.compile(pattern)

def extract(line):
    """
    返回字段的字典，如果返回None说明匹配失败
    """
    matcher = regex.match(line)
    info = None
    if matcher:
        info = {k: ops.get(k, lambda x: x)(v) for k, v in matcher.groupdict().items()}
    return info

# print(extract(logexample))


def openfile(path:str):
    with open(path) as f:
        for line in f:
            fields = extract(line)
            if fields:
                yield fields
            else:
                continue


def load(*paths):
    """ 装载日志文件 """
    for item in paths:
        p = Path(item)
        if not p.exists():
            continue
        if p.is_dir():
            for file in p.iterdir():
                if file.is_file():
                    yield from openfile(str(file))
        elif p.is_file():
            yield from openfile(str(p))



# for i in load('D:\\test.log'):
#     print(i)
# print(next(load('D:\\test.log')))


def source():
    yield {'datetime':datetime.datetime.now(), 'value':random.randint(1, 100)}
    time.sleep(1)

# s = source()
# items = [next(source()) for _ in range(3)]
# print(items)


# 处理函数
def handler(data):
    vals = [x['value'] for x in data]
    return sum(vals) / len(vals)


def status_handler(iterable):
    # 一批时间窗口内的数据
    status = {}
    for item in iterable:
        key = item['status']
        if key not in status.keys():
            status[key] = 0
        status[key] += 1
    total = sum(status.values())
    return {k:v/total*100 for k, v in status.items()}

# print("{:.2f}".format(handle(items)))

# 测试
def donothing_handler(iterable):
    return iterable


# 时间窗口
def window(src:Queue, handler, width:int, interval:int):
    """
    窗口函数
    :param src: 数据源，生成器，用来拿数据
    :param handler: 数据处理函数
    :param width: 时间窗口宽度，秒
    :param interval: 处理时间间隔，秒
    :return:
    """
    start = datetime.datetime.strptime('20190101 00:00:00 +0800', '%Y%m%d %H:%M:%S %z')
    current = datetime.datetime.strptime('20190101 00:01:00 +0800', '%Y%m%d %H:%M:%S %z')
    buffer = []     # 窗口中带计算的数据
    delta = datetime.timedelta(seconds=width - interval)
    while True:
        # 从数据源获取数据
        data = src.get()

        if data:    # 存入临时缓冲等待计算
            buffer.append(data)
            current = data['datetime']

        if (current - start).total_seconds() >= interval:
            ret = handler(buffer)
            print("{}".format(ret))
            start = current

            # 重叠方案
            buffer = [x for x in buffer if x['datetime'] > current - delta]


def dispatcher(src):
    handlers = []
    queues = []

    def reg(handler, width, interval):
        """
        注册窗口处理函数
        :param handler: 注册的数据处理函数
        :param width: 时间窗口宽度
        :param interval: 时间间隔
        :return:
        """
        q = Queue()
        queues.append(q)

        h = threading.Thread(target=window, args=(q, handler, width, interval))
        handlers.append(h)

    def run():
        for t in handlers:
            t.start()       # 启动线程

        for item in src:
            for q in queues:
                q.put(item)

    return reg, run


# path = 'D:\\test.log'
# reg, run = dispatcher(load(path))
# reg(status_handler, 10, 5)
# run()
# if __name__ == '__main__':
#     import sys
#     path = 'D:\\test.log'
#     reg, run = dispatcher(load(path))
#
#     reg(handler, 10, 5)
#     run()

