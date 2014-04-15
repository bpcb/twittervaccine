#!/usr/bin/env python

"""A simple sentiment summing algorithm based on Nielsen:

http://arxiv.org/abs/1103.2903
"""

import collections
import string

# Note: '-', and "'" are omitted from string.punctuation; these
# characters are used by AFINN_111
PUNCTUATION = '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~'

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

        return score

if __name__ == '__main__':
    scorer =  SentimentScorer.from_afinn_111()
    p1 = "This is Buoyant but I _CAN't staNd_ it!!!"
    print scorer.get_document_score(p1, False)
