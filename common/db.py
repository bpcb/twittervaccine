import pymysql

def get_database_connection(port = 2001):
	conn = pymysql.connect(host='localhost', port = port, user='root', db='vaccine')
 	
	return conn
