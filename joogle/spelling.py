from nltk.corpus import stopwords

# https://stackoverflow.com/questions/18658106/quick-implementation-of-character-n-grams-using-python
def char_ngram(w, n=3):
    return [w[i:i+n] for i in range(len(w)-n+1)]

def j(grams1, grams2):
    A = set(grams1)
    B = set(grams2)
    return len(A.intersection(B))/len(A.union(B))

def score(word, vocab):
    gram_in = char_ngram(word)
    return {w: j(gram_in, gram) for (w, gram) in vocab.items()}
        
"""
Low threshold because the UI always takes the top candidate as of right now.
This will be improved/deprecated in the future.
"""
def spell_check(m, vocab, min_word_len=4, threshold=0.25):
    if m in vocab or len(m) < min_word_len or m in stopwords.words():
        return [(m, 1)]

    if m.endswith('s') and m[:-1] in vocab:
        return [(m[:-1], 1)]
    
    matches = [(w, scr) for (w, scr) in score(m, vocab).items() if scr > threshold]
    return sorted(matches, key=lambda x: x[1], reverse=True)
