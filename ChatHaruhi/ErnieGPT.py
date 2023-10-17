# ErnieGPT.py
import erniebot 
#以下密钥信息从os环境获取
import os

# appid = os.environ['APPID']
# api_secret = os.environ['APISecret'] 
# api_key = os.environ['APIKey']
erniebot.access_token = os.environ["ErnieAccess"]

from .BaseLLM import BaseLLM

    


class ErnieGPT(BaseLLM):

    def __init__(self,model="ernie-bot",api_type="aistudio"):
        super(ErnieGPT,self).__init__()
        if model not in ["ernie-bot", "ernie-bot-turbo", "ernie-vilg-v2", "ernie-text-embedding"]:
            raise Exception("Unknown Ernie model")
        # SparkApi.answer =""
        self.messages = ""
        erniebot.api_type = api_type
        

    def initialize_message(self):
        self.messages = ""

    def ai_message(self, payload):
        self.messages = self.messages + "AI: " + payload  

    def system_message(self, payload):
        self.messages = self.messages + "System: " + payload 

    def user_message(self, payload):
        self.messages = self.messages + "User: " + payload  

    def get_response(self):
        # question = checklen(getText("user",Input))
        response = erniebot.ChatCompletion.create(model='ernie-bot', messages=[{"role": "user", "content": self.messages}])
        # message_json = [{"role": "user", "content": self.messages}]
        # SparkApi.answer =""
        # SparkApi.main(appid,api_key,api_secret,self.Spark_url,self.domain,message_json)
        return response["result"]
    
    def print_prompt(self):
        for message in self.messages:
            print(f"{message['role']}: {message['content']}")
