import os
from transformers import AutoTokenizer, AutoModel
from peft import LoraConfig, get_peft_model
from .BaseLLM import BaseLLM
import torch 

class ChatGLM2GPT(BaseLLM):
    def __init__(self, model = "glm2-6b"):
        super(ChatGLM2GPT, self).__init__()
        if model == "glm2-6b":
            self.tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True)
            self.model = AutoModel.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True).half().cuda()
        if model == "haruhi-fusion":
            self.tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True)
            self.model = AutoModel.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True).half().cuda()

            config = LoraConfig(
                r=16,
                lora_alpha=32,
                inference_mode=True,
                lora_dropout=0.05,
                #bias="none",
                task_type="CAUSAL_LM"
            )

            self.model = PeftModel.from_pretrained(model, "silk-road/Chat-Haruhi-Fusion_B")
        else:
            raise Exception("Unknown GLM model")
        self.messages = ""

    def initialize_message(self):
        self.message = ""

    def ai_message(self, payload):
        self.messages = self.messages + "\n " + payload 

    def system_message(self, payload):
        self.messages = self.messages + "\n " + payload 

    def user_message(self, payload):
        self.messages = self.messages + "\n " + payload 

    def get_response(self):
        with torch.no_grad():
            response, history = self.model.chat(self.tokenizer, input, history=[])
        return response
        
    def print_prompt(self):
        print(type(self.messages))
        print(self.messages)

