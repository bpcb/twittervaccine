#!/usr/bin/env python

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

import extract

def convert_labels_to_binary(Y, one_label_list):
    """Convert string labels to zero or ones."""
    pos = Y == one_label_list[0]
    for label in one_label_list[1:]:
        pos |= Y == sent_label

    X = np.zeros(Y.shape[0], dtype=np.int)
    X[pos] = 1

    return X

if __name__ == "__main__":
    results = list(extract.extract_classified_tweets(1000))
    _ids, votes, texts = zip(*results)

    tweets = np.asarray(texts)
    labels = np.asarray(votes)

    labels = convert_labels_to_binary(labels, ['-'])
    print labels
