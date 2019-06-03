import logging
LOGLEVEL = logging.INFO
LOGFILE = 'test.log'
LOGFORMAT = '%(asctime)s  LOGLEVEL:%(levelname)s  User:%(name)s  Msg:%(message)s'
logging.basicConfig(filename=LOGFILE, level=LOGLEVEL, format=LOGFORMAT)


logging.info('test')
# 2019-06-03 10:24:18,639  LOGLEVEL:INFO  User:root  Msg:test
