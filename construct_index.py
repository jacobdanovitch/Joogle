import json
from math import log10
from collections import Counter

import numpy as np
import pandas as pd

from build_dictionary import clean


def build_postings(txt, dataset="uottawa", to_file=True):
    term_dict = dict()
    index = [(i, clean(t, struct=list)) for i, t in enumerate(txt)]

    for i, doc in index:
        for term in doc:
            if term in term_dict:
                if i in term_dict[term]:
                    term_dict[term][i] += 1
                else:
                    term_dict[term][i] = 1
            else:
                term_dict[term] = {i: 1}

    if to_file:
        with open(f"model/{dataset}.postings.json", "w") as f:
            f.write(json.dumps(term_dict, indent=4))
    
    return index, term_dict



def to_sparse(posting, dim):
    c = Counter(posting)
    return [c[i] if i in c else 0 for i in range(dim)]


def sparse_term_matrix(term_dict, dim):
    return pd.DataFrame.from_dict(term_dict).fillna(0)


def l2norm(v):
    return np.array(v)/np.linalg.norm(v, ord=2)
