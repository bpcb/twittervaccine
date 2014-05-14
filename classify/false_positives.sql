-- Print tweets where VSPS marks it as negative, but it is labeled as something else.

select V.tweet_id, S.result, V.vote, T.text
from sentiment_score AS S, majority_vote_unique AS V, tweets_tweet AS T
where V.tweet_id=S.id and S.algorithm=1 and S.result < 0 and V.vote <> '-'
      and T.id=V.tweet_id
limit 200;
