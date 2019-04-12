from itertools import chain

from nltk.util import ngrams as _ngrams
from nltk import word_tokenize

import torch

# Default word tokens
PAD_token = 0  # Used for padding short sentences
SOS_token = 1  # Start-of-sentence token
EOS_token = 2  # End-of-sentence token

# https://pytorch.org/tutorials/beginner/chatbot_tutorial.html

class Vocab:
    def __init__(self, col):
        self.ngrams = Vocab.get_ngrams(col, struct=list)
        self.i2w = dict(enumerate(set(chain(*self.ngrams))))
        self.w2i = dict(map(reversed, self.i2w.items()))
    
    @staticmethod
    def build_ngrams(x, n=3):
        return _ngrams(x, n, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>')

    @staticmethod
    def get_ngrams(col, n=3, struct=iter):
        return struct(chain(*col.apply(Vocab.build_ngrams)))

    def sent2tensor(self, sent):
        return torch.tensor([self.w2i[w] for w in sent], dtype=torch.long)
    
    def __len__(self):
        return len(self.w2i)



class DeprVocab:
    def __init__(self, name=None):
        self.name = name
        self.word2index = {}
        self.word2count = {}
        self.index2word = {PAD_token: "PAD", SOS_token: "SOS", EOS_token: "EOS"}
        self.num_words = 3  # Count SOS, EOS, PAD
        self.ngrams = []
    
    def addList(self, word_list):
        for word in word_list:
            self.addWord(word)
        self.save_ngrams(word_list)
    
    def addSentence(self, sentence):
        self.addList(sentence.split(' '))

    def addWord(self, word):
        if word not in self.word2index:
            self.word2index[word] = self.num_words
            self.word2count[word] = 1
            self.index2word[self.num_words] = word
            self.num_words += 1
        else:
            self.word2count[word] += 1
            
    def save_ngrams(self, w, n=3):
        grams = [(w[i:i+n-1], w[i+n-1]) for i in range(len(w)-n+1)]
        self.ngrams.extend(grams)
        
        return grams
    
    def sent2tensor(self, sent):
        return torch.tensor([self.word2index[w] for w in sent], dtype=torch.long)
    
    def __len__(self):
        return self.num_words