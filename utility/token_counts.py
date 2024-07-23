from transformers import GPT2Tokenizer

class TokenCalculator:
    def __init__(self, model_name='gpt2'):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    def count_tokens(self, text):
        tokens = self.tokenizer.encode(text)
        return len(tokens)
    
def get_token(text):
    calculator = TokenCalculator()
    return calculator.count_tokens(text)