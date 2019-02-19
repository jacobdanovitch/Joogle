import re
from build_dictionary import remove_punc

def flatten(l):
    return [item for sublist in l for item in sublist]

def make_bigrams(text):
    return [b for l in text for b in zip(re.split(r'\s+', l)[:-1], re.split(r'\s+', l)[1:])]
    
    
def jaccard(bigram, bigrams):
    if len(bigram) != 2:
        raise ValueError(f"Err: {bigram}")
    w1, w2 = bigram
    
    intersection = []
    union = []
    
    for (b1, b2) in bigrams:
        if (w1 == b1) or (w2 == b2):
            union.append((b1, b2))
            if (w1 == b1) and (w2 == b2): 
                intersection.append((b1, b2))
    
    assert len(union) >= len(intersection), f"Err: {bigram} {len(intersection), len(union)}"
    
    if len(union) == 0:
        return 0
    
    return len(intersection)/len(union)

def find_phrases(potential_phrases, bigrams, threshold):
    jcs = [(p, jaccard(p, bigrams)) for p in potential_phrases]
    return { "-".join(b): jc for (b, jc) in jcs if jc > threshold }


def join_phrases(t, phrases):
    for p in phrases:
        reg = p.replace("-", "[\s-]*")
        rep = re.sub(r"[\s-]*", "", p)
        t = re.sub(reg, rep, t)
    return t

def identify_candidates(corpus):
    candidates = flatten([re.findall(r"\b[a-zA-Z]{3,}\b-+\w*", remove_punc(t.lower())) for t in corpus])
    candidates = [tuple(p.split("-")) for p in candidates]
    return candidates

def index_phrases(corpus, threshold=0.8):
    candidates = identify_candidates(corpus)
    corpus = [remove_punc(t.lower(), rm_hyphens=True) for t in corpus]
    
    # text = " ".join(corpus).strip()
    
    bigrams = make_bigrams(corpus)
    phrases = find_phrases(candidates, bigrams, threshold)
    
    replace_fn = lambda t: join_phrases(t, phrases.keys())
    return list(map(replace_fn, corpus)), phrases
        
    
    
    
    