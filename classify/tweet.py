import collections

class Tweet(object):
    def __init__(self, tweet_id):
        self.tweet_id = tweet_id
        self.votes = collections.Counter()
        self.text = None

    def __repr__(self):
        return 'Tweet(%s, %r, %s)' % (self.tweet_id, self.votes, self.text)

    def add_votes(self, label, count):
        self.votes[label] += count

    def get_majority_vote(self):
        max_key, max_val = max(self.votes.iteritems(), key=lambda x: x[1])
        return max_key # XXX ties broken arbitrarily
