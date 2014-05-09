import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

from db import get_database_connection
import pandas

conn = get_database_connection(port = 2001)
output = conn.execute('SELECT L.county, L.state, S.result FROM tweets_tweet AS T, sentiment_score AS S, \
	usa_user_locations AS L WHERE T.id=S.id AND T.tweeter_id=L.id AND algorithm=1')
	
