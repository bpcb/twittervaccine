# Calculate the majority vote for each tweet
# XXX Emits multiple tuples in the event of a tie

DROP TABLE IF EXISTS vaccine.majority_vote;
CREATE TABLE vaccine.majority_vote(tweet_id int, vote varchar(1), vote_count int);

INSERT INTO vaccine.majority_vote
SELECT X.* FROM vaccine.vote_count AS X
JOIN (
    SELECT tweet_id, MAX(count) AS max_count
    FROM vaccine.vote_count AS Y
    GROUP BY tweet_id
    ) AS Y
ON X.count = Y.max_count AND X.tweet_id = Y.tweet_id;
