select county, state, avg(result) AS avg_score, count(*) AS num_tweets FROM (
    select L.county, L.state, S.result from tweets_tweet AS T, sentiment_score AS S,
     usa_user_locations AS L WHERE T.id=S.id AND T.tweeter_id=L.id AND algorithm=1) as X
group by county, state
having count(*) > 50
order by avg_score;


