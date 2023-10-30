import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class SummaryController:
    def __init__(self, model: AutoModelForSeq2SeqLM, tokenizer: AutoTokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def transform(self, text: str) -> str:
        prefix = "summary: "
        inputs = prefix + text
        inputs = self.tokenizer(inputs, max_length=512, truncation=True, return_tensors="pt")
        output = self.model.generate(**inputs, num_beams=3, do_sample=True, min_length=10, max_length=512)
        decoded_output = self.tokenizer.batch_decode(output, skip_special_tokens=True)[0]
        result = nltk.sent_tokenize(decoded_output.strip())[0]
        return result