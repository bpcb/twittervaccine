from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string

# Note: "not" and "no" removed from lucene stopword list
STOPWORDS = ["a", "and", "are", "as", "at", "be", "but", "by",  "for",
"if", "in", "into", "is", "it", "of", "on", "or", "s", "such",
"t", "that", "the", "their", "then", "there", "these", "they", "this", "to",
"was", "will", "with"]

def remove_punctuation(s):
    """Remove punctuation from a string; same algorithm as the PSU study.

    Note that '!' are preserved.

    Also note that this code smashes together tokens without spaces:
    "red,yellow,blue" => "redyellowblue".
    """
    return s.translate(string.maketrans("",""),
                       string.punctuation.replace("!", ""))

def tokenize(text):
    """Convert a string into a sequence of normalized words.

    The methodology here follows the PSU study:
    https://github.com/salathegroup/vaccine-sentiment/blob/master/analysis/sentiment-calculation/classifier/classify.py
"""
    stemmer = PorterStemmer()

    it1 = text.split()
    it2 = (x.lower() for x in it1)
    it3 = (remove_punctuation(x) for x in it2)
    it4 = [stemmer.stem(x) for x in it3]

    return it4

