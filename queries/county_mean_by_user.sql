-- Emit the mean of all users within a county
select CONCAT(county, " ", state), avg(user_avg_score) AS avg_score FROM (
    -- emit average score per user
    select L.id AS user_id, L.county, L.state, avg(result) AS user_avg_score
    from tweets_tweet AS T, sentiment_score AS S, usa_user_locations AS L
    WHERE T.id=S.id AND T.tweeter_id=L.id AND algorithm=1 AND L.county IS NOT NULL
    group by L.id, L.county, L.state) X
group by county, state;
