# 命令调度器
from functools import partial


def command_dispatcher():
    # 构建全局字典
    cmd_tbl = {}

    #注册函数
    def reg(cmd, *args, **kwargs):
        def _reg(fn):
            func = partial(fn, *args, **kwargs)
            cmd_tbl[cmd] = func
            return func
        return _reg

    # 缺省函数
    def default_func():
        print('Unknown command')

    # 调度器
    def dispatcher():
        while True:
            cmd = input('Please input cmd>>')
            # 退出条件
            if cmd.strip() == '':
                return
            cmd_tbl.get(cmd, default_func)()

    return reg, dispatcher


reg, dispatcher = command_dispatcher()


@reg('mag', z=200, y=300, x=100)
def foo1(x, y, z):
    print('magedu', x, y, z)


@reg('py', 300, b=400)
def foo2(a, b=100):
    print('python', a, b)

dispatcher()
