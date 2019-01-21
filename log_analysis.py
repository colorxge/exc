import re
import datetime


logexample = '''183.69.210.164 - - [07/Apr/2017:09:32:46 +0800] "GET /app/template/default//style/css.css HTTP/1.1" 200 8803 "http://job.magedu.com/index.php?m=login" "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"'''
pattern='''(?P<remote>[\d.]+) - - \[(?P<datetime>[^\[\]]+)\] "(?P<method>\w+) (?P<url>\S+) (?P<protocol>[\w/.]+)" (?P<status>\d+) (?P<length>\d+) "(?P<exp>[^"]+)" "(?P<useragent>[^"]+)"'''
regex = re.compile(pattern)


def covert_time(strdate:str):
    return datetime.datetime.strptime(strdate, '%d/%b/%Y:%H:%M:%S %z')

def covert_request(strrequest:str):
    return dict(zip(['method', 'url', 'protocol'], strrequest.split()))

ops = {
    'datetime': lambda strdate: datetime.datetime.strptime(strdate, '%d/%b/%Y:%H:%M:%S %z'),
    'status': int,
    'length': int
}

def extract(line):
    matcher = regex.match(line)
    info = None
    if matcher:
        info = {k: ops.get(k, lambda x: x)(v) for k, v in matcher.groupdict().items()}
    return info

print(extract(logexample))

# 数据载入

# with open("D:\BaiduNetdiskDownload\\09-Python week07\logs\\test.log") as f:
#     for line in f:
#         a = regex.match(line)
#         print(a.groups())
#         print(a.groupdict())

def load(path:str):
    with open(path) as f:
        for line in f:
            fields = extract(line)
            if fields:
                yield fields
            else:
                continue

