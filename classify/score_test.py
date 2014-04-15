import unittest
import score

"""Unit tests of SentimentScorer.

Execute via nosetests.
"""

CASES = [("This is Buoyant but I _CAN't staNd_ it!!!", -1, -1.0 / 8),
         ("blockbuster of biased !!!BITCHES!!!", -4, -4.0 / 4),
         ("This is a neutral document; there isn't really much to see here.", 0, 0.0),
         ("This code is broken!!!", -1, -1.0/4),
         ("This shit does not work; it's a total greenwashing", -10, -10.0/9),
        ]

class ScoreTest(unittest.TestCase):
    def setUp(self):
        self.scorer = score.SentimentScorer.from_afinn_111()

    def test_unnormalized_pharses(self):
        for text, unnorm, norm in CASES:
            self.assertEquals(self.scorer.get_document_score(text, False), unnorm)
