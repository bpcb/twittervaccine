# Drop tweets that contain ties in their majority vote counts
DROP TABLE IF EXISTS vaccine.majority_vote_unique;

CREATE TABLE vaccine.majority_vote_unique(tweet_id int, vote varchar(1), vote_count int);

INSERT INTO vaccine.majority_vote_unique
SELECT X.* FROM vaccine.majority_vote AS X
JOIN (
    SELECT tweet_id, count(*) AS count FROM vaccine.majority_vote AS Y
    GROUP BY tweet_id
) AS Y
ON X.tweet_id = Y.tweet_id AND Y.count=1;

