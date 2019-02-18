from nltk.corpus import stopwords
from nltk import regexp_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

import string
import re
import json


def punctuation_regex(rm_hyphens):
    punc = string.punctuation
    if not rm_hyphens:
        punc = punc.replace('-', '')
    
    punc_reg = r"\b(\w*\d\w*)\b|"+f"[{punc}]" # rm punctuation, words w/ nums
    return re.compile(punc_reg)

def remove_punc(txt, rep_with=' ', rm_hyphens=False):
    return re.sub(punctuation_regex(rm_hyphens), rep_with, txt)

def tokenize(txt, pattern=r"\b[a-zA-Z]{3,}\b-*\w*"): # only words >= 3 char
    return regexp_tokenize(txt, pattern)
    
def lemmatize(tokens, lm=WordNetLemmatizer()):
    return list(map(lm.lemmatize, tokens)) 


def clean(txt, struct=set, rm_stopwords=True):
    txt = remove_punc(txt.lower(), rm_hyphens=True)
    tokens = tokenize(txt)
    if rm_stopwords:
        tokens = set(tokens).difference(stopwords.words())
    
    return struct(lemmatize(tokens))




