import numpy as np
import pandas as pd
import nltk

class Sequencer():

    def __init__(self, tweets, embedding_dict, padding):

        self.tweets = tweets
        self.embed = embedding_dict
        self.padding = padding

    def text_to_vec(self, tweet):
        vec = []
        tweet = tweet.split()

        for word in tweet:
            try:                
                vec.append(self.embed[word])
            except:
                pass
        
        return np.array(vec).flatten()

    def padder(self, vec):

        if self.padding - len(vec) > 0:
            pad = np.zeros(self.padding - len(vec))
            vec = np.append(vec, pad)

        return vec[:self.padding].flatten()
        

    