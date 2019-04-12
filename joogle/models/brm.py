from .retrieval_model import BaseRM
from .. import remove_punc, tokenize, join_phrases, spell_check

import boolean
import re


"""
Boolean Retrieval Model
"""
class BRM(BaseRM):
    def __init__(self, data_path="data/catalogue-uottawa-ca.json", posting_path="model/uottawa.postings.json"):
        super(BRM, self).__init__(data_path, posting_path)
        self.algebra = boolean.BooleanAlgebra()

    
    def preprocess_query(self, q, rm_stopwords=False):
        q = super(BRM, self).preprocess_query(q)
        q = join_phrases(q, self.phrases)
        q = remove_punc(q, rep_with='', rm_hyphens=True, rm_asterisk=False)
        
        wildcards = re.findall(r"\w+\*[^\w]*", q)
        for wc in wildcards:
            wc = wc.replace(" ", "")
            if not wc.endswith("*"):
                continue
            root = wc.replace("*", "")
            rep = f"({'|'.join((w for w in self.build_vocab() if w.startswith(root)))})"
            q = q.replace(wc, rep)

        q = self.algebra.parse(q)
        return q
        """
        for s in q.get_symbols():
            s.obj = s.obj.lower()
            
        return q
        """

    
    def query(self, q, top_n=None):
        q = self.preprocess_query(q)
        def curried_match(d):
            return self.match(q, d)

        mask = self.data.cleaned.apply(curried_match)
        out = self.data[mask][["title", "body"]]
        if top_n:
            return out[:top_n]
        return out

    def match(self, expr, d): # https://booleanpy.readthedocs.io/en/latest/users_guide.html
        return bool(expr.subs({s: (s.TRUE if s.obj in d else s.FALSE) for s in expr.get_symbols()}, simplify=True))
    
    
    def check_spelling(self, query):
        def stringify_expr(q):
            return str(q).lower().replace("|", " OR ").replace("&", " AND ")
        
        vocab = self.build_vocab()
        q = self.preprocess_query(query)
        cp = stringify_expr(q).replace("-", "")
        
        for s in q.get_symbols():
            s.obj = spell_check(s.obj, vocab)[0][0]

        corrected = stringify_expr(q)
        return (corrected != cp) and corrected

