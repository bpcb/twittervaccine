

-- average user tweet score
select T.tweeter_id, avg(result) AS user_avg_score, count(*) AS num_tweets
FROM tweets_tweet AS T, sentiment_score AS S
WHERE T.id=S.id AND algorithm=1
group by T.tweeter_id
having count(*) > 5
order by user_avg_score ASC
limit 50;

