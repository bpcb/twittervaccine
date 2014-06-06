import pymysql

def get_database_connection(port=None):
    if not port:
        port = 3306
    conn = pymysql.connect(host='localhost', port = port, user='root', db='vaccine')
    return conn
