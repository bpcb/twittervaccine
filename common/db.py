import pymysql
import os

def get_database_connection(port=None):
    if not port:
        try:
            with open(os.path.expanduser('~/.mysqlport')) as fh:
                port = int(fh.read())
        except Exception as e:
            port = 3306
    conn = pymysql.connect(host = 'localhost', port = port, user='root', db='vaccine', charset = 'utf8')
    return conn
