import argparse
from pathlib import Path
from datetime import datetime

# 1、实现传参问题
# ls -l -a -h
parser = argparse.ArgumentParser(prog='ls', add_help=False, description='list diectory contents')  # 获得一个参数解释器
parser.add_argument('path', nargs='?', default='.', help='path help')
parser.add_argument('-l', action='store_true', help='use a long listing format')
parser.add_argument('-a', action='store_true', help='show all files, include then starting with .')
parser.add_argument('-h', action='store_true', help='in the form human friendliness')
args = parser.parse_args(('-ahl',))  # 分析参数
print('args = {}'.format(args))
# parser.print_help()


# 实现主体功能 ls -l
def show_dir(path, all=True):
    p = Path(path)
    for file in p.iterdir():
        if not all and file.name.startswith('.'):
            continue
        else:
            yield file.name

# 获取权限格式 -rwxrwxrwx 1 python python 5 Oct 25 00:07 test
def show_dir_detail(path, all=False):
    p = Path(path)
    for file in p.iterdir():
        if not all and file.name.startswith('.'):
            continue
        stat = file.stat()
        t = get_filetype(file)
        mstr = rwx(file.stat().st_mode)
        file_atime = datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')
        yield (t+mstr, stat.st_nlink, stat.st_size,file_atime, file.name)

# 获取文件类型
def get_filetype(file: Path):
    if file.is_dir():
        return 'd'
    elif file.is_block_device():
        return 'b'
    # ```
    else:
        return '-'

rwx_mode = 'rwxrwxrwx'
def rwx(modint):
    # stat = file.stat().st_mode
    rwx_num = modint & 0o777
    endless_num = bin(rwx_num)
    stat_str = ''
    for i, v in enumerate(endless_num[2:]):
        if v == '1':
            stat_str += rwx_mode[i]
        else:
            stat_str += '-'
    return stat_str

size_mode = ' KMGT'
def human_mode(size):
    flag = 0
    while True:
        if size < 1024:
            return '{} {}'.format(size, size_mode[flag])
        size = round(size/1024, 1)
        flag += 1


def ls_dir(path, all=False, detail=False, human=False):
    p = Path(path)
    for file in p.iterdir():
        if not all and file.name.startswith('.'):
            continue
        if not detail:
            yield file.name
        else:
            stat = file.stat()
            t = get_filetype(file)
            mstr = rwx(file.stat().st_mode)
            file_atime = datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')
            if not human:
                yield (t + mstr, stat.st_nlink, stat.st_size, file_atime, file.name)
            else:
                yield (t + mstr, stat.st_nlink, human_mode(stat.st_size), file_atime, file.name)


print(list(ls_dir(args.path, args.a, args.l, args.h)))