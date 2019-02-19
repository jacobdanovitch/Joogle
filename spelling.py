def char_ngram(w, n=2):
    return [w[i:i+n] for i in range(len(w)-n+1)]

def ratio(a, b):
    return len([ch for ch in b if ch in a]) / len(b)

def match(m, vocab):
    m = char_ngram(m)
    return {w: ratio(chars, m) for (w, chars) in vocab.items()}
        
def spell_check(m, vocab, threshold=0.75):
    if m in vocab:
        return [(m, 1)]
    
    matches = match(m, vocab)    
    sorted_matches = reversed(sorted(matches.items(), key=lambda x: x[1]))
    
    return [(w, score) for (w, score) in sorted_matches if score > threshold]