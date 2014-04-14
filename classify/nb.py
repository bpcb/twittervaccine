#!/usr/bin/env python

"""Andrew's implementation of NaiveBayes."""

from collections import Counter, defaultdict

import math
import random
import time

import nltk

import ttokenize
from extract import *
from tweet import *

class NaiveBayes(object):

    def __init__(self):
        # Map from label to total count; used to compute prior
        self.label_counts = Counter()

        # Data counts: map from label to Counter of words;
        # used to compute data likelihood
        self.word_counts = defaultdict(Counter)

    def classify(self, words, alpha=1.0):
        num_words = len(set(words))

        training_set_size = sum(self.label_counts.values())
        max_p = -100000000
        max_label = None

        for label in self.label_counts.keys():
            # initialize likelihood with the MLE of the prior
            p = math.log(float(self.label_counts[label]) / training_set_size)

            cond_word_counts = self.word_counts[label]
            cond_num_words = sum(cond_word_counts.values())

            for word in words:
                # compute log data likelhood using a dirichlet prior
                p += math.log((float(cond_word_counts[word]) + alpha) /
                              (cond_num_words + alpha * num_words))

            if p > max_p:
                max_p = p
                max_label = label

        return max_label

    def train(self, words, label):
        self.label_counts[label] += 1
        for word in words:
            self.word_counts[label][word] += 1

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

    nb = NaiveBayes()
    for tweet in training_set:
        toks = ttokenize.tokenize(tweet.text)
        nb.train(toks, tweet.get_majority_vote())

    tm2 = time.time()

    print('  time=%0.3fs' % (tm2 - tm1))

    print('Testing accuracy on %d tweets' % test_set_size)
    tm1 = time.time()

    predictions = []
    references = []
    for tweet in test_set:
        references.append(tweet.get_majority_vote())
        toks = ttokenize.tokenize(tweet.text)
        predictions.append(nb.classify(toks))

    mat = nltk.ConfusionMatrix(references, predictions)
    tm2 = time.time()

    print mat.pp(show_percents=True)
    print ('%d of %d correct ==> %f%%' % (mat._correct, mat._total,
                                          float(mat._correct) / mat._total))
    print('  time=%0.3fs' % (tm2 - tm1))

if __name__ == '__main__':
    main()
