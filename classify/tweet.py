
class Tweet(object):
    def __init__(self, tweet_id):
        self.tweet_id = tweet_id
        self.majority_vote = None
        self.text = None

    def __repr__(self):
        return 'Tweet(%s, %r, %s)' % (self.tweet_id, self.majority_vote, self.text)
