# encoding:utf-8
import logging

path = '..'
# create logger
# 这里可以修改开源模块的日志等级
formatter = logging.Formatter(fmt="%(asctime)s  %(levelname)s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
# 设置日志的路径，编码
c = logging.FileHandler(path + "/lib/log/all.log", mode='a', encoding='utf8')
c.setFormatter(formatter)

logger = logging.getLogger('frame log')
logger.setLevel(logging.DEBUG)
logger.addHandler(c)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)


# 打印debug级日志
def debug(ss):
    global logger
    try:
        logger.debug(str(ss))
    except exception():
        return


# 打印info级别的日志
def info(ss):
    global logger
    try:
        logger.info(str(ss))
    except exception():
        return


# 打印warn级别的日志
def warn(ss):
    global logger
    try:
        logger.warning(str(ss))
    except exception():
        return


# 打印error级别日志
def error(ss):
    global logger
    try:
        logger.error(str(ss))
    except exception():
        return


# 打印异常日志
def exception(e):
    global logger
    try:
        logger.exception(e)
    except exception():
        return


# 调试
if __name__ == "__main__":
    debug("debug test")
    info("info test")
    warn("warn test")
    error("error test")

    # 使用exception方法：
    try:
        a = 1
        print(a + "2")
    except Exception as e:
        exception(e)