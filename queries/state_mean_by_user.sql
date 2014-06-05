-- Emit the mean of all users within a state
select state, avg(user_avg_score) AS avg_score from (
    -- emit average score per user
    select L.id AS user_id, L.state AS state, avg(S.result) AS user_avg_score
    from tweets_tweet AS T, sentiment_score AS S, usa_user_locations AS L
    where T.id=S.id AND T.tweeter_id=L.id AND S.algorithm=3
    group by L.id, L.state) X
group by state;
