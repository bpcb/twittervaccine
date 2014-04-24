import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

"""Sample of inserting a python dictionary into a table."""

from db import get_database_connection

record = {'col1': 7, 'col2': "pizza pizza", 'col3': True}

tups = [(key, val) for key, val in record.iteritems()]
keys = [key for key, val in tups]
vals = [val for key, val in tups]

conn = get_database_connection()
cursor = conn.cursor()

num_cols = len(keys)
key_str = ','.join(keys)
val_str = ','.join(['%s'] * num_cols)

qry = "INSERT INTO vaccine.dummy (%s) VALUES (%s)" % (key_str, val_str)
print qry

cursor.execute(qry, vals)

conn.commit()
cursor.close()
conn.close()
