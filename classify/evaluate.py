#!/usr/bin/env python

"""Evaluate the VSPS sentiment scores compared to labled training data."""

import extract
import publish

def evaluate(scorer):
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

    res = {'precision': float(tp) / (tp + fp),
           'recall':  float(tp) / (tp + fn),
           'accuracy': (float(tp) + float(tn)) / (tp + tn + fn + fp)
           }

    print res

