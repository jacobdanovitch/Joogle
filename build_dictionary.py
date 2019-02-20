from nltk.corpus import stopwords
from nltk import regexp_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

import string
import re
import json

# stopwords = open("data/stopwords.english").readlines()


def punctuation_regex(rm_hyphens, rm_asterisk):
    punc = string.punctuation
    if not rm_hyphens:
        punc = punc.replace('-', '')
    if not rm_asterisk:
        punc = punc.replace('*', '')
    
    punc_reg = r"\b(\w*\d\w*)\b|"+f"[{punc}]" # rm punctuation, words w/ nums
    return re.compile(punc_reg)

def remove_punc(txt, rep_with=' ', rm_hyphens=False, rm_asterisk=False):
    return re.sub(punctuation_regex(rm_hyphens, rm_asterisk), rep_with, txt)

def tokenize(txt, pattern=r"\b[a-zA-Z]{3,}\b-*\w*"): # only words >= 3 char
    return regexp_tokenize(txt, pattern)
    
def lemmatize(tokens, lm=WordNetLemmatizer()):
    return list(map(lm.lemmatize, tokens)) 


def clean(txt, struct=set, rm_stopwords=True):
    txt = remove_punc(txt.lower(), rm_hyphens=True)
    tokens = tokenize(txt)
    if rm_stopwords:
        tokens = set(tokens).difference(stopwords.words())#stopwords)
    
    return struct(lemmatize(tokens))


