import MySQLdb

def get_database_connection():
    conn = MySQLdb.connect(host='localhost', user='root', db='vaccine')
    return conn
