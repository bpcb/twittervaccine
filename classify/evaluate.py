#!/usr/bin/env python

"""Evaluate the VSPS sentiment scores compared to labled training data."""

import extract
import publish

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

def evaluate_revised(scorer):
    """Evaluate a scorer using revised labels."""

    results = {(x,y) : 0 for x in ['-', 'X'] for y in ['-', 'X']}

    for _id, label, text in extract.extract_labeled_tweets():
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

