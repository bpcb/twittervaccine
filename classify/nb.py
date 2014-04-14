#!/usr/bin/env python

from collections import Counter, defaultdict
import math

"""Andrew's implementation of NaiveBayes."""

class NaiveBayes(object):

    def __init__(self):
        # Map from label to total count; used to compute prior
        self.label_counts = Counter()

        # Data counts: map from label to Counter of words;
        # used to compute data likelihood
        self.word_counts = defaultdict(Counter)

    def classify(self, datum, alpha=1.0):
        words, label = datum

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
                p += math.log((float(cond_word_counts[word]) + alpha) / (cond_num_words + alpha * num_words))


            if p > max_p:
                max_p = p
                max_label = label

        return max_label

    def train(self, data):
        for words, label in data:
            self.label_counts[label] += 1

            for word in words:
                self.word_counts[label][word] += 1
