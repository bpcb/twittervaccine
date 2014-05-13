from pandas.io import sql
import pymysql
import scipy.stats
import numpy as np
import collections

# Use SQL to compute the average sentiment score per user. 
# Drop state-only entries (for which the county is not known).

def average_user_scores():
	"""
	Queries SQL database to return an object with average score
	by user with their associated county and state locations.
	"""
	
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
	
	return results

def county_results(query_results):
	"""
	Returns a dictionary with 2-tuple keys (county, state) 
	associated with a list of average scores for users
	in counties where there are at least 20 users.
	"""
	
	d = collections.defaultdict(list)
	for _id, county, state, avg in query_results:
		d[(county, state)].append(avg)

	# Filter out counties with less than 20 users.
	d2 = {key: val for key, val in d.iteritems() if len(val) >= 20}
	
	return d2

d = average_user_scores()
d2 = county_results(d)

# Run ANOVA over resulting 417 counties.

f, p = scipy.stats.f_oneway(*d2.values())
print f, p

# Run Kruskal test which is less stringent with assumptions than ANOVA.

value_arrays = []
for values in d2.values():
	value_arrays.append(np.array(values))
h, p2 = scipy.stats.kruskal(*value_arrays)
print h, p2