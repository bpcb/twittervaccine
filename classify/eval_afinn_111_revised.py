#!/usr/bin/env python

import score
import evaluate

scorer = score.SentimentScorer.from_afinn_111()
results = evaluate.evaluate_revised(scorer)
evaluate.display_results(results)
