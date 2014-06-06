#!/usr/bin/env python

"""Use scikit's multinomial naive bayes to classify tweets."""

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB

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
    cv = CountVectorizer(decode_error='ignore')
    clf = MultinomialNB()
    pipeline = Pipeline([('vect', cv), ('clf', clf)])
    return pipeline

class MultinomialNBScorer(object):
    def __init__(self):
        results = list(extract.extract_labeled_tweets())
        _ids, _labels, _tweets = zip(*results)

        tweets = np.asarray(_tweets)
        labels = np.asarray(_labels)

        # remap non-negative ('X') to 1, negative 0
        labels = convert_labels_to_binary(labels, ['X'])

        self.clf = create_classifier()
        self.clf.fit(tweets, labels)

    def get_document_score(self, text):
        """Score of a document is the probability that it's non-negative."""
        preds = self.clf.predict_proba([text])
        print preds
        return preds[0][1]

if __name__ == '__main__':
    scorer = MultinomialNBScorer()
    print scorer.get_document_score("vaccines are shocking, terrible poison.  do not get vaccinated! avoid avoid!")
    print scorer.get_document_score("sunshine and roses are nice things")
    print scorer.get_document_score("another shocking warning about swine flu vaccine")
