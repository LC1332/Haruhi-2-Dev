# SparkGPT.py
import SparkApi
#以下密钥信息从控制台获取
appid = "219faa1b"     #填写控制台中获取的 APPID 信息
api_secret = "OWFmOTJhOTVmYWNkNWU4MGEwMzE3MmRj"   #填写控制台中获取的 APISecret 信息
api_key ="b01212368a9a141b05475cf9dd298f63"    #填写控制台中获取的 APIKey 信息


from .BaseLLM import BaseLLM

    


class SparkGPT(BaseLLM):

    def __init__(self, model="Spark2.0"):
        super(SparkGPT,self).__init__()
        if model == "Spark2.0":
            self.domain = "generalv2"    # v2.0版本
            self.Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
        elif model == "Spark1.5":
            self.domain = "general"   # v1.5版本
            self.Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
        else:
            raise Exception("Unknown Spark model")
        # SparkApi.answer =""
        self.messages = []
        

    def initialize_message(self):
        self.messages = []

    def ai_message(self, payload):
        self.messages.append(payload)

    def system_message(self, payload):
        self.messages.append(payload)

    def user_message(self, payload):
        self.messages.append(payload)

    def get_response(self):
        SparkApi.answer =""
        SparkApi.main(appid,api_key,api_secret,self.Spark_url,self.domain,self.messages)
        return SparkApi.answer
    
    def print_prompt(self):
        for message in self.messages:
            print(message)
