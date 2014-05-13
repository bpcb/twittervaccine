#!/usr/bin/env python

import score
import evaluate

scorer = score.SentimentScorer.from_vaccine_phrases()
results = evaluate.evaluate(scorer)
evaluate.display_results(results)
