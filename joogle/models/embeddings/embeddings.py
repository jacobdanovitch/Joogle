import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from tqdm import tqdm_notebook as tqdm
from loguru import logger

import datetime
import random

class NGramLanguageModeler(nn.Module):
    def __init__(self, vocab, embedding_dim, context_size):
        super().__init__()

        self.vocab = vocab
        vocab_size = len(self.vocab)

        self.embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.linear1 = nn.Linear(context_size * embedding_dim, 256)
        self.linear2 = nn.Linear(256, 128)
        self.linear3 = nn.Linear(128, vocab_size)
        
        if torch.cuda.is_available():
            print("Using CUDA.")
            self = self.cuda()
        

    def forward(self, inputs):
        embeds = self.embeddings(inputs).view((1, -1))
        out = F.relu(self.linear1(embeds))
        out = F.relu(self.linear2(out))
        out = self.linear3(out)
        log_probs = F.log_softmax(out, dim=1)
        return log_probs
    
    def train(self, EPOCHS = 3, BATCH_SIZE = False):
        loss_function = nn.NLLLoss()
        optimizer = optim.SGD(self.parameters(), lr=0.001)

        logger.info("Begin training")
        losses = []
        for epoch in range(1, EPOCHS+1):
            total_loss = 0
            train_data = random.sample(self.vocab.ngrams, BATCH_SIZE) if BATCH_SIZE else self.vocab.ngrams
            
            i = 0
            for c1, c2, target in tqdm(train_data):
                context_idxs = torch.tensor([self.vocab.w2i[c1], self.vocab.w2i[c2]], dtype=torch.long)
                
                self.zero_grad()
                
                log_probs = self(context_idxs)
                loss = loss_function(log_probs, torch.tensor([self.vocab.w2i[target]], dtype=torch.long))
                loss.backward()
                optimizer.step()

                total_loss += loss.item()
                i+= 1
                
            model_name = f"EP{epoch}_TEP{EPOCHS}_BS{len(train_data)}.torch"          
            losses.append(total_loss/len(train_data))
            logger.info(f"Epoch {epoch}/{EPOCHS}: {losses[-1]}")
            
            self.save_progress(model_name)
        return losses
    
    def save_progress(self, model_name):
        logger.info(f"Saving model checkpoint to file: {model_name}")
        torch.save(self, model_name)