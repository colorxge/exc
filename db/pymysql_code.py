import pymysql
from pymysql.cursors import DictCursor

# version 1
try:
    conn = pymysql.connect('127.0.0.1', 'root', '123456', 'test', 3306)
    print(conn.ping(False))

    cusor = conn.cursor(DictCursor)
    for i in range(10):
        sql = 'select %(id)s'
        row = cusor.execute(sql, {'id': i})
        print(row)
        print(cusor.fetchone())
except Exception as e:
    print(e)
finally:
    if conn:
        conn.close()
    # print(conn.ping(False))


# version 2
conn = pymysql.connect('127.0.0.1', 'root', '123456', 'test', 3306)
try:
    with conn as cusor:
        sql = 'select %(id)s'
        cusor.execute(sql, {'id': 100})
        print(cusor.fetchone())
    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()
finally:
    print('=========')
    conn.close()
