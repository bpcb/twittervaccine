import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

"""Sample of inserting a python dictionary into a table."""

from db import get_database_connection

record = {'col1': 7, 'col2': "pizza pizza", 'col3': True}

conn = get_database_connection()
cursor = conn.cursor()

num_cols = len(record)
key_str = ','.join(record.keys())
val_str = ','.join(['%s'] * num_cols)

qry = "INSERT INTO vaccine.dummy (%s) VALUES (%s)" % (key_str, val_str)
print qry

cursor.execute(qry, record.values())

conn.commit()
cursor.close()
conn.close()
