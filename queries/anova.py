import pandas as pd
import pymysql
import scipy.stats
import numpy as np
import collections
import sys

# Hack: append common/ to sys.path
sys.path.append("../common")

from db import get_database_connection

# Use SQL to compute the average sentiment score per user. 
# Drop state-only entries (for which the county is not known).

# Query that emits average value by user for 2009 data.  
query_2009 = """
SELECT L.id AS user_id, L.county, L.state, avg(result) AS user_avg_score
FROM tweets_tweet AS T, sentiment_score AS S, usa_user_locations AS L
WHERE T.id=S.id AND T.tweeter_id=L.id AND algorithm='5' AND L.county IS NOT NULL AND L.country='United States'
group by L.id, L.county, L.state;
"""

# Query that instead emits the average value for users in 2014 data.
query_2014 = """
(
SELECT L.user_id, L.county, L.state, AVG(result) AS user_avg_score
FROM tweets_2014 AS T, sentiment_score_2014 AS S, user_locations_2014 AS L
WHERE T.tweet_id=S.tweet_id AND T.user_id=L.user_id AND algorithm='5' AND L.county IS NOT NULL AND L.country='United States'
GROUP BY L.user_id, L.county, L.state
)
"""

def average_user_scores(query):
    """
    Queries SQL database to return an object with average score
    by user with their associated county and state locations.
    """

    conn = get_database_connection(port = 2001)
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
    
def anova():
    """
    Runs ANOVA and Kruskal tests over 2009 and 2014 datasets. 
    """
    
    for query in [query_2014, query_2009]:
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

if __name__ == '__main__':
    # anova()
    
    df_2014 = pd.read_sql(query_2014, get_database_connection(port = 2001))
    df_2009 = pd.read_sql(query_2009, get_database_connection(port = 2001))
    
    df_2014_means = df_2014.groupby(['county', 'state']).mean()
    df_2014_counts = df_2014.groupby(['county', 'state']).size()
    df_2014_concat = pd.concat([df_2014_means, df_2014_counts], axis = 1, keys = ['county', 'state'])
    print df_2014_concat.head()
    print df_2014_concat.columns.values
    df_2014_filtered = df_2014_concat[df_2014_concat['0'] >= 20]