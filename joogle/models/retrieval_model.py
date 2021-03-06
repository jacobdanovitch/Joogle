import re
import json
import pandas as pd

# from ..construct_index import build_postings
# from phrase_indexing import index_phrases, join_phrases
# from spelling import spell_check, char_ngram
# from build_dictionary import clean, remove_punc
from .. import build_postings, index_phrases, join_phrases, spell_check, char_ngram, clean, remove_punc

class BaseRM:
    def __init__(self, data_path="data/catalogue-uottawa-ca.json", posting_path="model/uottawa.postings.json"):
        self.data = pd.read_json(data_path)[["id", "title", "body"]]
        corpus, self.phrases = index_phrases(list(map(' '.join, self.data.body.apply(lambda x: clean(x, struct=list, rm_stopwords=False)).tolist())))
        self.data["cleaned"] = corpus

        if posting_path:
            with open(posting_path) as f:
                self.term_dict = json.load(f)
                for t in self.term_dict.keys():
                    self.term_dict[t] = {int(k):v for k, v in self.term_dict[t].items()}
        else:
            self.index, self.term_dict = build_postings(corpus)

        self.vocab = self.build_vocab()
            
            
    def preprocess_query(self, q, **kwargs):
        q = join_phrases(q, self.phrases)
        return q
    
    
    def build_vocab(self):
        vocab = {w: char_ngram(w) for w in self.term_dict.keys()}
        return vocab
    
    def check_spelling(self, query):        
        query = query.lower().strip()
        query = join_phrases(query, self.phrases)
        q = re.findall(r'\w+', remove_punc(query))

        corrections = {}
        for w in q:
            match = spell_check(w, self.vocab)
            if match:
                corrections[w] = match[0][0]
            
        if not corrections:
            return False

        corrected = " ".join((corrections.get(w) or w) for w in q)
        return (query != corrected) and corrected
        
        
        
        
        
