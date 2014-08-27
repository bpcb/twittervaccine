import pandas as pd
import pymysql
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
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

# Query that emits average value by user for 2009 data.  
query_2009_indiv = """
SELECT U.twitter_user_id AS user_id, L.county, L.state, avg(result) AS user_avg_score
FROM tweets_tweet AS T, sentiment_score AS S, usa_user_locations AS L, tweeter_tweeter AS U
WHERE U.id=T.id AND T.id=S.id AND T.tweeter_id=L.id AND algorithm='5' AND L.county IS NOT NULL AND L.country='United States'
GROUP BY U.twitter_user_id;
"""

# Query that instead emits the average value for users in 2014 data.
query_2014_indiv = """
SELECT L.user_id, L.county, L.state, AVG(result) AS user_avg_score
FROM tweets_2014 AS T, sentiment_score_2014 AS S, user_locations_2014 AS L
WHERE T.tweet_id=S.tweet_id AND T.user_id=L.user_id AND algorithm='5' AND L.county IS NOT NULL AND L.country='United States'
GROUP BY L.user_id;
"""

new_query = """
SELECT U.user_id, L.county, L.state, L2.county, L2.state
FROM tweeter_tweeter as T, users_2014 as U, user_locations_2014 as L, usa_user_locations as L2
WHERE T.twitter_user_id=U.user_id
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
       
def compare_by_county():       
    df_2014 = pd.read_sql(query_2014, get_database_connection(port = 2001))
    stats_2014 = df_2014[['county', 'state', 'user_avg_score']].groupby(['county', 'state']).agg(['mean', 'count'])
    stats_2014_20_users = stats_2014[stats_2014['user_avg_score']['count'] >= 20]
    
    df_2009 = pd.read_sql(query_2009, get_database_connection(port = 2001))
    stats_2009 = df_2009[['county', 'state', 'user_avg_score']].groupby(['county', 'state']).agg(['mean', 'count'])
    stats_2009_20_users = stats_2009[stats_2009['user_avg_score']['count'] >= 20]
    print stats_2009_20_users
    
    combined = pd.merge(stats_2014_20_users, stats_2009_20_users, left_index = True, right_index = True, how = 'inner')
    print combined.corr()
    
    x = np.arange(0.70, 0.85, 0.01)
    m, b = np.polyfit(combined['user_avg_score_x']['mean'], combined['user_avg_score_y']['mean'], 1)
    plt.plot(x, m*x + b, '-', color = 'red', linewidth = 2)
    
    plt.scatter(combined['user_avg_score_x']['mean'], combined['user_avg_score_y']['mean'])
    plt.grid()
    plt.xlabel('Average user sentiment score by county, 2014')
    plt.ylabel('Average user sentiment score by county, 2009')
    plt.rcParams['xtick.major.pad'] = 8
    plt.rcParams['ytick.major.pad'] = 8
    plt.savefig('./compare_2009_2014_county.png')
    
def state_averages_2014():
    df_2014 = pd.read_sql(query_2014, get_database_connection(port = 2001))
    stats_2014 = df_2014[['state', 'user_avg_score']].groupby(['state']).agg(['mean', 'count'])
    print stats_2014 
    
    stats_2014.to_csv('./average_sentiment_by_state_2014.csv')
    
    
    
def compare_by_indiv():
    df_2014_indiv = pd.read_sql(query_2014_indiv, get_database_connection(port = 2001))
    df_2009_indiv = pd.read_sql(query_2009_indiv, get_database_connection(port = 2001))
    
    combined = pd.merge(df_2014_indiv, df_2009_indiv, on = 'user_id', how = 'inner')
    
    plt.scatter(combined['user_avg_score_x'], combined['user_avg_score_y'])
    plt.grid()
    plt.legend()
    plt.xlabel('Average user sentiment score, 2014')
    plt.ylabel('Average user sentiment score, 2009')
    plt.rcParams['xtick.major.pad'] = 8
    plt.rcParams['ytick.major.pad'] = 8
    plt.savefig('./compare_2009_2014_indiv.png')

if __name__ == '__main__':
    state_averages_2014()
    # anova()
    # compare_by_county()
    # compare_by_indiv()