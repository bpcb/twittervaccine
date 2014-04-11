# Compute the fraction of votes for each tweet, category
DROP TABLE IF EXISTS vaccine.vote_fraction;
CREATE TABLE vaccine.vote_fraction(tweet_id int, vote varchar(1), fraction double,
       PRIMARY KEY (tweet_id, vote));

INSERT INTO vaccine.vote_fraction
SELECT V.tweet_id, V.vote, V.count / T.count
FROM vaccine.vote_count AS V, vaccine.total_vote AS T
WHERE V.tweet_id = T.tweet_id;
