from retrieval_model import *
from construct_index import sparse_term_matrix

from math import log10
import json

import numpy as np
import pandas as pd


class Stats:
    @staticmethod
    def tf_idf(df, word):
        tf = df.loc[:, word]
        df_i = len(df[df[word] > 0])

        idf = log10(len(df) / df_i)
        return tf*idf

    @staticmethod
    def sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod # https://stackoverflow.com/questions/34968722/how-to-implement-the-softmax-function-in-python
    def softmax(x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0) # only difference

    @staticmethod # https://stackoverflow.com/questions/44607537/convert-array-into-percentiles
    def pctiles(x):
        return [ (len(list(np.where(np.array(x)<=i)[0]))/len(x))*100  for i in x]




"""
Vector Space Model
"""
class VSM(BaseRM):
    def __init__(self, data_path="data/catalogue-uottawa-ca.json", posting_path="model/uottawa.postings.json"):
        super(VSM, self).__init__(data_path, posting_path)
        self.d_w = self.weight_matrix()

    def preprocess_query(self, q, struct=list, rm_stopwords=True):
        q = super(VSM, self).preprocess_query(q)
        q = clean(q, struct=struct, rm_stopwords=rm_stopwords)
        return q
    
    def rank(self, q):
        q = self.preprocess_query(q, struct=set)
        try:
            return self.d_w.loc[:, set(q)].T.apply(sum).sort_values(ascending=False)
        except:
            return None

    def query(self, q, top_n=10, confidence_method=Stats.sigmoid):
        res = self.rank(q)
        if res is None:
            return None
        out = self.data.loc[res.head(10).index]
        
        if confidence_method:
            res = confidence_method(res)
            probs = pd.Series(res).rename("confidence")
        
            out = out.join(pd.DataFrame(probs))
        
        out.index.name = "id"
        return out[:top_n][["title", "body", "confidence"]]

    def weight_matrix(self):
        df = sparse_term_matrix(self.term_dict, len(self.data))
        return pd.DataFrame(list(map(lambda x: Stats.tf_idf(df, x), df.columns))).T 




