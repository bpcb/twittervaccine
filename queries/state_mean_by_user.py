# Compute state mean by user for a given algorithm
import sys

algo = int(sys.argv[1])

print("""select state, avg(user_avg_score) AS avg_score from (
    -- emit average score per user
    select L.id AS user_id, L.state AS state, avg(S.result) AS user_avg_score
    from tweets_tweet AS T, sentiment_score AS S, usa_user_locations AS L
    where T.id=S.id AND T.tweeter_id=L.id AND S.algorithm=%d
    group by L.id, L.state) X
group by state;
""" % algo)