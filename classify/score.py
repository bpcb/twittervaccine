#!/usr/bin/env python

"""A simple sentiment summing algorithm based on Nielsen:

http://arxiv.org/abs/1103.2903
"""

import collections
import string

# Note: '-', and "'" are omitted from string.punctuation; these
# characters are used by AFINN_111
PUNCTUATION = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~'

# hand-crafted sentiment scores for vaccine sentiment;
# all values are negative
VACCINE_SCORES = {
    "shouldn't" : -2,
    "should not": -2,
    "must not": -2,
    "mustn't": -2,
    "don't": -1,
    "do not": -2,
    "won't": -2,
    "will not": -2,
    "renounce": -1,
    "renounced": -1,
    "renounces": -1,
    "boycott": -3,
    "refuse": -3,
    "mandatory": -1,
    "forced": -3,
    "forces": -3,
    "forcing": -3,
    "coerce": -4,
    "coerced": -4,
    "coercing": -4,
    "required": -1,
    "requires": -1,
    "have to": -1,
    "avoid": -1,
    "never": -1,
    "untested", -1,
    "poison": -3,
    "not necessary": -1,
    "not vaccinating": -3,
    "not vaccinated": -3,
    "not vaccinate": -3,
}

def get_tokens(s):
    """Convert a string into a list of normalized tokens."""

    # Convert punctuation to whitespace, except for "-" and "'", which are
    # contained in AFINN-111
    s2 = s.translate(string.maketrans(PUNCTUATION, " " * len(PUNCTUATION)))
    toks = s2.split()
    return [t.lower() for t in toks]

class SentimentScorer(object):
    def __init__(self):
        self.ngrams = collections.OrderedDict([(k, {}) for k in [3, 2, 1]])

    @classmethod
    def from_afinn_111(cls):
        ws = cls()

        with open('AFINN-111.txt') as fh:
            for line in fh:
                toks = line.split()
                score = int(toks[-1])
                words = toks[:-1]

                d = ws.ngrams[len(words)]
                d[tuple(words)] = score

        return ws

    @classmethod
    def from_vaccine_phrases(cls):
        ws = cls()

        for phrase, score in VACCINE_SCORES.iteritems():
            key = tuple(phrase.split())
            d = ws.ngrams[len(key)]
            d[key] = score

        return ws

    def get_phrase_score(self, token_list, idx):
        for phrase_length, score_dict in self.ngrams.iteritems():
            phrase = tuple(token_list[idx:idx + phrase_length])
            if phrase in score_dict:
                return score_dict[phrase], phrase_length
        return 0, 1 # No match: assign zero score to 1 token

    def get_document_score(self, text, normalize=True):
        toks = get_tokens(text)
        idx = 0
        score = 0

        while idx < len(toks):
            phrase_score, phrase_length = self.get_phrase_score(toks, idx)
            score += phrase_score
            idx += phrase_length

        if normalize:
            return float(score) / len(toks)
        else:
            return score

if __name__ == '__main__':
    scorer =  SentimentScorer.from_afinn_111()
    print scorer.ngrams[3]
    print scorer.ngrams[2]
