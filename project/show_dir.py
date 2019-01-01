import argparse
from pathlib import Path
from datetime import datetime

# 1、实现传参问题
# ls -l -a -h
parser = argparse.ArgumentParser(prog='ls', add_help=True, description='list diectory contents')  # 获得一个参数解释器
parser.add_argument('path', nargs='?', default='.', help='path help')
parser.add_argument('-l', action='store_true', help='use a long listing format')
parser.add_argument('-a', action='store_true', help='show all files, include then starting with .')
parser.add_argument('-g', action='store_true', help='in the form human friendliness')
args = parser.parse_args()  # 分析参数
print('args = {}'.format(args))
parser.print_help()


# 实现主体功能
def show_dir(path, all=False):
    p = Path(path)
    for file in p.iterdir():
        if not all and file.name.startswith('.'):
            continue
        else:
            yield file.name

print(list(show_dir(args.path, True)))


# 获取文件类型
def get_filetype(file: Path):
    if file.is_dir():
        return 'd'
    elif file.is_block_device():
        return 'b'
    # ```
    else:
        return '-'


# 获取权限格式 -rwxrwxrwx 1 python python 5 Oct 25 00:07 test
def show_dir_detail(path, all=False):
    p = Path(path)
    for file in p.iterdir():
        if not all and file.name.startswith('.'):
            continue
        stat = file.stat()
        t = get_filetype(file)
        yield (t, stat.st_size, file.name)

print(list(show_dir_detail(args.path)))