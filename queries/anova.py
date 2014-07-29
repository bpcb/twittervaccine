from pandas.io import sql
import pymysql
import scipy.stats
import numpy as np
import collections

# Use SQL to compute the average sentiment score per user. 
# Drop state-only entries (for which the county is not known).

def average_user_scores(query):
    """
    Queries SQL database to return an object with average score
    by user with their associated county and state locations.
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

if __name__ == '__main__':
    # Query that emits average value by user for 2009 data.
    
    # query = """
    # -- emit average user score; note that user id defines location
    # select L.id AS user_id, L.county, L.state, avg(result) AS user_avg_score
    # from tweets_tweet AS T, sentiment_score AS S, usa_user_locations AS L
    # where T.id=S.id AND T.tweeter_id=L.id AND algorithm='3' AND L.county is not NULL
    # group by L.id, L.county, L.state;
    # """

    # Query that instead emits the average value for users in 2014 data.
    query = """
    (
    SELECT L.user_id, L.county, L.state, AVG(result) AS user_avg_score
    from tweets_2014 AS T, sentiment_score_2014 AS S, user_locations_2014 AS L
    WHERE T.tweet_id=S.tweet_id AND T.user_id=L.user_id AND algorithm='5' AND L.county IS NOT NULL
    GROUP BY L.user_id, L.county, L.state
    )
    """

    d = average_user_scores(query)
    d2 = county_results(d)
    print len(d2)
    
    # Run ANOVA over resulting 417 counties (for 2009 data; still running 2014 data).

    f, p = scipy.stats.f_oneway(*d2.values())
    print f, p

    # Run Kruskal test which makes less stringent assumptions than ANOVA.

    value_arrays = []
    for values in d2.values():
        value_arrays.append(np.array(values))
    h, p2 = scipy.stats.kruskal(*value_arrays)
    print h, p2