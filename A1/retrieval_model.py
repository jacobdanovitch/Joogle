import re
import json
import pandas as pd

from construct_index import build_postings
from phrase_indexing import index_phrases, join_phrases
from spelling import spell_check, char_ngram
from build_dictionary import clean, remove_punc

class BaseRM:
    def __init__(self, data_path="data/catalogue-uottawa-ca.json", posting_path="model/uottawa.postings.json"):
        self.data = pd.read_json(data_path).set_index("id")[["title", "body"]]
        corpus, self.phrases = index_phrases(self.data.body.tolist())
        self.data["cleaned"] = corpus

        if posting_path:
            with open(posting_path) as f:
                self.term_dict = json.load(f)
                for t in self.term_dict.keys():
                    self.term_dict[t] = {int(k):v for k, v in self.term_dict[t].items()}
        else:
            self.index, self.term_dict = build_postings(corpus)
            
            
    def preprocess_query(self, q, **kwargs):
        q = join_phrases(q, self.phrases)
        return q
    
    
    def build_vocab(self):
        vocab = list(self.term_dict.keys())
        vocab = {w: char_ngram(w) for w in vocab}
        return vocab
    
    def check_spelling(self, query):        
        vocab = self.build_vocab()
        
        query = query.lower().strip()
        query = join_phrases(query, self.phrases)
        q = re.findall(r'\w+', remove_punc(query))

        corrections = {}
        for w in q:
            try:
                corrections[w] = spell_check(w, vocab)[0][0]
            except:
                pass
            
        if not corrections:
            return False

        corrected = " ".join((corrections.get(w) or w) for w in q)
        return (query != corrected) and corrected
        
        
        
        
        