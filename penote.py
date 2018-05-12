import os
import sys
import time

# 获取进程号的命令
__PID_COMMAND = "ps -ef | grep penote.app | grep -v grep | awk '{print $2}'"
# 启动的命令
__START_COMMAND = 'nohup /usr/bin/python3.6 -m penote.app > /dev/null 2>&1 &'
# 结束的命令
__STOP_COMMAND = 'kill %s'
# 帮助
__HELP = '参数：\n    start - 运行\n    restart - 重启\n    stop - 停止\n'


def get_pid():
    """获取进程号"""
    return os.popen(__PID_COMMAND).read()


def start():
    """启动程序"""
    pid = get_pid()
    if pid != '':
        # 若程序在运行
        print('错误，程序正在运行，进程号%s' % pid, file=sys.stderr)
        exit(1)
    else:
        # 若程序未运行
        os.popen(__START_COMMAND)
        pid = get_pid()
        if pid != '':
            # 若程序在运行
            print('运行，进程号%s' % pid)
            exit(0)
        else:
            # 若程序未运行
            print('错误，启动失败', file=sys.stderr)
            exit(1)


def stop():
    """停止程序"""
    pid = get_pid()
    if pid != '':
        # 若程序在运行
        os.popen(__STOP_COMMAND % pid)
        print('停止，进程号%s' % pid)
        exit(0)
    else:
        # 若程序未运行
        print('错误，程序未运行', file=sys.stderr)
        exit(1)


def restart():
    """重启程序"""
    pid = get_pid()
    if pid != '':
        # 若程序在运行
        os.popen(__STOP_COMMAND % pid)
        time.sleep(5)
        start()
    else:
        # 若程序未运行
        start()


if __name__ == '__main__':
    # 若参数不正确
    if len(sys.argv) != 2:
        print(__HELP)
    else:
        arg = sys.argv[1]
        if arg == 'start':
            start()
        elif arg == 'stop':
            stop()
        elif arg == 'restart':
            restart()
        else:
            print('错误的参数"%s"\n%s' % (arg, __HELP), file=sys.stderr)
