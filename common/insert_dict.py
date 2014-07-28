import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

"""Sample of inserting a python dictionary into a table."""

from db import get_database_connection

def insert_record(record, table):
	"""
	Given a dictionary, uses its keys to insert its values
	in mySQL table (assumes key names map to column names in table).
	"""

	tups = [(key, val) for key, val in record.iteritems()]
	keys = [key for key, val in tups]
	vals = [val for key, val in tups]

	conn = get_database_connection(port = 2001)
	cursor = conn.cursor()

	num_cols = len(keys)
	key_str = ','.join(keys)
	val_str = ','.join(['%s'] * num_cols)

	qry = "REPLACE INTO %s (%s) VALUES (%s)" % (table, key_str, val_str)
	cursor.execute(qry, vals)

	conn.commit()
	cursor.close()
	conn.close()
    
def in_database(entry, column, table):
    """
    Test whether entry is already observed in a given column of a given table.
    """
    
    conn = get_database_connection(port = 2001)
    cursor = conn.cursor()
    
    query = 'SELECT * FROM %s WHERE %s = %s' % (table, column, entry) 
    cursor.execute(query)
    
    results = cursor.fetchall()
    
    if len(results) == 0:
        return False
    else:
        return True
    
if __name__ == '__main__':
    assert in_database(entry = 591, column = 'user_id', table = 'users_2014') == True
    assert in_database(entry = 0000000000, column = 'user_id', table = 'users_2014') == False
