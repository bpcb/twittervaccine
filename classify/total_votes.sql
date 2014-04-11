# Count all votes for a given tweet
DROP TABLE IF EXISTS vaccine.total_vote;
CREATE TABLE vaccine.total_vote(tweet_id int PRIMARY KEY, count int);

INSERT INTO vaccine.total_vote
SELECT tweet_id, COUNT(*) AS vote_count FROM vaccine.sentiment_sentiment
GROUP BY tweet_id;
