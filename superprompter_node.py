import os
import torch
import re
from transformers import T5Tokenizer, T5ForConditionalGeneration

class SuperPrompterNode:
    def __init__(self):
        self.modelDir = os.path.expanduser("~") + "/.models"
        self.tokenizer = None
        self.model = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Enter prompt here"}),
                "max_new_tokens": ("INT", {"default": 512, "min": 1, "max": 2048}),
                "repetition_penalty": ("FLOAT", {"default": 1.2, "min": 0.0, "max": 2.0, "step": 0.1}),
                "remove_incomplete_sentences": ("BOOLEAN", {"default": True}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("generated_text",)
    FUNCTION = "generate_text"
    CATEGORY = "text"

    def remove_incomplete_sentence(self, paragraph):
        return re.sub(r'((?:\[^.!?\](?!\[.!?\]))\*+\[^.!?\\s\]\[^.!?\]\*$)', '', paragraph.rstrip())

    def download_models(self):
        model_name = "roborovski/superprompt-v1"
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name, torch_dtype=torch.float16)
        os.makedirs(self.modelDir, exist_ok=True)
        self.tokenizer.save_pretrained(self.modelDir)
        self.model.save_pretrained(self.modelDir)
        print("Downloaded SuperPrompt-v1 model files to", self.modelDir)

    def load_models(self):
        if not all(os.path.exists(self.modelDir) for file in self.modelDir):
            self.download_models()
        else:
            print("Model files found. Skipping download.")

        self.tokenizer = T5Tokenizer.from_pretrained(self.modelDir)
        self.model = T5ForConditionalGeneration.from_pretrained(self.modelDir, torch_dtype=torch.float16)
        print("SuperPrompt-v1 model loaded successfully.")

    def generate_text(self, prompt, max_new_tokens, repetition_penalty, remove_incomplete_sentences):
        if self.tokenizer is None or self.model is None:
            self.load_models()

        seed = 1
        torch.manual_seed(seed)
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        systemprompt = "Expand the following prompt to add more detail:"
        input_ids = self.tokenizer(systemprompt + prompt, return_tensors="pt").input_ids.to(device)
        if torch.cuda.is_available():
            self.model.to('cuda')

        outputs = self.model.generate(input_ids, max_new_tokens=max_new_tokens, repetition_penalty=repetition_penalty,
                                      do_sample=True)

        dirty_text = self.tokenizer.decode(outputs[0])
        text = dirty_text.replace("<pad>", "").replace("</s>", "").strip()
        
        if remove_incomplete_sentences:
            text = self.remove_incomplete_sentence(text)
        
        return (text,)
