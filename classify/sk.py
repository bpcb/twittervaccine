#!/usr/bin/env python

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split

import extract

def convert_labels_to_binary(Y, one_label_list):
    """Convert string labels to zero or ones."""
    pos = Y == one_label_list[0]
    for label in one_label_list[1:]:
        pos |= Y == sent_label

    X = np.zeros(Y.shape[0], dtype=np.int)
    X[pos] = 1

    return X

def create_classifier():
    cv = CountVectorizer()
    clf = MultinomialNB()
    pipeline = Pipeline([('vect', cv), ('clf', clf)])
    return pipeline

if __name__ == "__main__":
    results = list(extract.extract_classified_tweets(1000))
    _ids, votes, texts = zip(*results)

    tweets = np.asarray(texts)
    labels = np.asarray(votes)

    labels = convert_labels_to_binary(labels, ['-'])

    X_train, X_test, y_train, y_test = train_test_split(
        tweets, labels, test_size=0.2, random_state=0)
    clf = create_classifier()
    clf.fit(X_train, y_train)
    print clf.score(X_test, y_test)