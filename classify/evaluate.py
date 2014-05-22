#!/usr/bin/env python

"""Evaluate the VSPS sentiment scores compared to labled training data."""

import extract
import publish

from sklearn.metrics import precision_recall_fscore_support

def evaluate(scorer):
    """Evaluate a scorer using PSU labels."""
    # confusion matrix: label, result => count
    results = {(x,y) : 0 for x in ['-', 'X'] for y in ['-', 'X']}

    for _id, label, text in extract.extract_classified_tweets():
        score = scorer.get_document_score(text, normalize=False)
        if score < 0:
            result = '-'
        else:
            result = 'X'
        results[(label, result)] += 1

    return results

def display_results(results):
    print results

    tp = results[('-', '-')]
    tn = results[('X', 'X')]
    fp = results[('X', '-')]
    fn = results[('-', 'X')]

    precision = float(tp) / (tp + fp)
    recall =  float(tp) / (tp + fn)
    accuracy = (float(tp) + float(tn)) / (tp + tn + fn + fp)
    fscore = 2 * precision * recall / (precision + recall)

    print precision, recall, accuracy, fscore

def evaluate_revised(scorer):
    """Evaluate a scorer using revised labels."""

    y_true = []
    y_pred = []

    def get_score(text):
        score = scorer.get_document_score(text, normalize=False)
        if score < 0:
             return '-'
        else:
            return 'X'

    res = [(label, get_score(text)) for _id, label, text in
            extract.extract_labeled_tweets()]
    y_true, y_pred = zip(*res)

    p, r, f, s = precision_recall_fscore_support(y_true, y_pred, pos_label='-')
    correct = sum(1 for label, pred in zip(y_true, y_pred) if label==pred)
    accuracy = float(correct) / len(y_true)
    print 'precision=%.3f recall=%.3f fscore=%.3f accuracy=%.3f' % (
        p[0], r[0], f[0], accuracy)
