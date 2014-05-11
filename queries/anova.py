from pandas.io import sql
import pymysql
import scipy.stats
import numpy as np

# Use SQL to compute the average sentiment score per user. 
# Drop state-only entries (for which the county is not known).

query = """
-- emit average user score; note that user id defines location
select L.id AS user_id, L.county, L.state, avg(result) AS user_avg_score
from tweets_tweet AS T, sentiment_score AS S, usa_user_locations AS L
where T.id=S.id AND T.tweeter_id=L.id AND algorithm=1 AND L.county is not NULL
group by L.id, L.county, L.state;
"""

conn = pymysql.connect(host='localhost', port=2001, user='root', db='vaccine')
cursor = conn.cursor()
cursor.execute(query)

results = cursor.fetchall()
cursor.close()
conn.close()

# Create a data series for each county/state. 

import collections
d = collections.defaultdict(list)
for _id, county, state, avg in results:
    d[(county, state)].append(avg)
print len(d)

# Filter out counties with less than 20 users.

d2 = {key: val for key, val in d.iteritems() if len(val) >= 20}
print len(d2)

# Run ANOVA over resulting 417 counties.

f, p = scipy.stats.f_oneway(*d2.values())
print f, p

value_arrays = []
for values in d2.values():
	value_arrays.append(np.array(values))
print value_arrays
h, p2 = scipy.stats.kruskal(*value_arrays)
print h, p2