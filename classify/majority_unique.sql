# Drop tweets that contain ties in their majority vote counts
DROP TABLE IF EXISTS vaccine.majority_vote_unique;

CREATE TABLE vaccine.majority_vote_unique(tweet_id int, vote varchar(1), vote_count int);

INSERT INTO vaccine.majority_vote_unique
SELECT X.* FROM vaccine.majority_vote AS X
WHERE NOT EXISTS (
    SELECT * FROM vaccine.majority_vote AS Y
    WHERE X.tweet_id=Y.tweet_id AND X.vote <> Y.vote
    );
