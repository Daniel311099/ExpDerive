


import torch


class BaseDecoder():
    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    def decode(self, phrase, embedding):
        # tokenize phrase and append it to embedding
        # pass to model
        tokens = self.tokenizer(phrase, return_tensors="pt")
        tokens.to(self.device)
        embedding = torch.cat((embedding, tokens['input_ids'][0]))
        
        

class FuncDecoder(BaseDecoder):
    pass

class ArgDecoder(BaseDecoder):
    pass
