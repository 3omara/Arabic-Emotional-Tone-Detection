import sys
import os
sys.path.append('./Scripts')
sys.path.append('./Files')
sys.path.append('./Datasets')

from nltk.corpus import stopwords
import nltk

import json
from scipy.sparse import csr_matrix
from scipy.sparse import hstack

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

import lexicon
from lexicon import calc_lexicon

def count_vectorize(X):
    count_vec = CountVectorizer(ngram_range=(1,1))
    return count_vec.fit_transform(X)

def tfidf_vectorize(X):
    tfidf_vec = TfidfVectorizer()
    return tfidf_vec.fit_transform(X)

def lexicon_calculate(X):
    tweet_train_lex = []
    for tweet in X:
        tweet_train_lex.append(calc_lexicon(u"%s" %tweet))

    tweet_lex_train_sparse = csr_matrix(tweet_train_lex)
    train_feature_matrix = hstack((count_vectorize(X), tweet_lex_train_sparse))

    return train_feature_matrix

def write_dict(path, dict):
    with open(path, 'w') as convert_file:
        convert_file.write(json.dumps(dict))

def read_dict(path):
    with open(path) as f:
        data = f.read()
    return json.loads(data)



