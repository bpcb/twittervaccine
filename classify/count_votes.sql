# Tabulate all votes; group by tweet_id and vote category
DROP TABLE IF EXISTS vaccine.vote_count;
CREATE TABLE vaccine.vote_count(tweet_id int, vote varchar(1), count int);

INSERT INTO vaccine.vote_count
SELECT tweet_id, vote, COUNT(*) AS vote_count FROM vaccine.sentiment_sentiment
GROUP BY tweet_id, vote;