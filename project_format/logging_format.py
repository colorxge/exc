import logging


LOGLEVEL = logging.INFO
LOGFILE = 'd:/tmp/test.log'
LOGFORMAT = "%(asctime)s [%(name)s] msg:%(message)s"
logging.basicConfig(format=LOGFORMAT, level=LOGLEVEL, filename=LOGFILE)
# FORMAT = logging.Formatter(LOGFORMAT)
logger = logging.getLogger('a')
logger.info('aad')


def getlogger(mod_name:str, filepath:str):
    logger = logging.getLogger(mod_name)
    logger.setLevel(logging.INFO)  # 单独设置
    logger.propagate = False  # 阻止传送给父logger
    handler = logging.FileHandler(filepath)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s [%(name)s %(funcName)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


### other .py
import test


logger = test.getlogger(__name__, 'd:/tmp/test.log')
logger.info()
