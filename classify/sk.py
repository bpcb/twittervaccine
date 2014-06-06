#!/usr/bin/env python

import numpy as np
import pylab as pl
import nltk.stem
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import train_test_split
from sklearn.metrics import *

import extract

class StemmedTfidfVectorizer(TfidfVectorizer):
    """Apply stemming to the tokens of a TfidfClassifier."""
    def build_analyzer(self):
        stemmer = nltk.stem.SnowballStemmer('english')
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: [stemmer.stem(x) for x in analyzer(doc)]

def convert_labels_to_binary(Y, one_label_list):
    """Convert string labels to zero or ones."""
    pos = Y == one_label_list[0]
    for label in one_label_list[1:]:
        pos |= Y == sent_label

    X = np.zeros(Y.shape[0], dtype=np.int)
    X[pos] = 1

    return X

def create_classifier():
    cv = TfidfVectorizer(decode_error='ignore')
    clf = MultinomialNB()
    pipeline = Pipeline([('vect', cv), ('clf', clf)])
    return pipeline

if __name__ == "__main__":
    results = list(extract.extract_labled_tweets())
    _ids, _labels, _tweets = zip(*results)

    tweets = np.asarray(_tweets)
    labels = np.asarray(_labels)

    # remap z to 1, everything else to 0
    labels = convert_labels_to_binary(labels, ['z'])

    X_train, X_test, y_train, y_test = train_test_split(
        tweets, labels, test_size=0.2, random_state=0)
    clf = create_classifier()
    clf.fit(X_train, y_train)
    print ("Accuracy: %0.2f" % clf.score(X_test, y_test))

    y_preds = clf.predict(X_test)
    target_names = ['Non-negative', 'negative']
    print (classification_report(y_test, y_preds, target_names=target_names))
