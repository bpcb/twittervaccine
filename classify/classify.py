#!/usr/bin/env python

"""Tweet sentiment analysis."""

import random
import sys
import time

import nltk.classify

import ttokenize
from extract import *
from tweet import *

def prepare_nltk_naive_bayes_data(tweets):
    """Return a list of (feature_dictionary, label) tuples."""

    instances = []
    for tweet in tweets:
        toks = ttokenize.tokenize(tweet.text)
        feature_dict = dict([(t, True) for t in toks])
        instances.append((feature_dict, tweet.get_majority_vote()))
    return instances

def train_nltk_naive_bayes(tweets):
    instances = prepare_nltk_naive_bayes_data(tweets)
    return nltk.classify.NaiveBayesClassifier.train(instances)

def test_nltk_naive_bayes(classifier, tweets):
    instances = prepare_nltk_naive_bayes_data(tweets)
    return nltk.classify.accuracy(classifier, instances)

TEST_SET_PROPORTION = .2

def main():
    random.seed(7)

    # AAA: Use a random shuffle to select test/training sets
    print('Extracting twitter data from the database...')
    tm1 = time.time()
    tweets = extract()
    tm2 = time.time()

    print('  time=%0.3fs' % (tm2 - tm1))

    test_set_size = int(TEST_SET_PROPORTION * len(tweets))

    print('Training on %d tweets' % (len(tweets) - test_set_size))

    tm1 = time.time()
    random.shuffle(tweets)

    test_set = tweets[:test_set_size]
    training_set = tweets[test_set_size:]

    classifier = train_nltk_naive_bayes(training_set)
    tm2 = time.time()

    print('  time=%0.3fs' % (tm2 - tm1))

    print('Testing accuracy on %d tweets' % test_set_size)
    tm1 = time.time()
    ac = test_nltk_naive_bayes(classifier, test_set)
    tm2 = time.time()

    print('Accuracy=%f' % ac)
    print('  time=%0.3fs' % (tm2 - tm1))

if __name__ == '__main__':
    main()
