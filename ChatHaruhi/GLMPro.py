from .BaseLLM import BaseLLM
import os

zhipu_api = os.environ['ZHIPU_API']

import zhipuai
import time

class GLMPro( BaseLLM ):
    def __init__(self, model="chatglm_pro"):
        super(GLMPro,self).__init__()

        zhipuai.api_key = zhipu_api

        self.model_name = model

        self.prompts = []
        

    def initialize_message(self):
        self.prompts = []

    def ai_message(self, payload):
        self.prompts.append({"role":"assistant","content":payload})

    def system_message(self, payload):
        self.prompts.append({"role":"user","content":payload})

    def user_message(self, payload):
        self.prompts.append({"role":"user","content":payload})

    def get_response(self):
        zhipuai.api_key = zhipu_api
        max_test_name = 5
        sleep_interval = 1

        request_id = None

        # try submit asychonize request until success
        for test_time in range( max_test_name ):
            response = zhipuai.model_api.async_invoke(
                model = self.model_name,
                prompt = self.prompts,
                temperature = 0)
            if response['success'] == True:
                request_id = response['data']['task_id']
                break
            else:
                print('submit GLM request failed, retrying...')

        if request_id:
            # try get response until success
            for test_time in range( 2 * max_test_name ):
                result = zhipuai.model_api.query_async_invoke_result( request_id )
                if result['code'] == 200 and result['data']['task_status'] == 'SUCCESS':
                    choices = result['data']['choices']
                    if len( choices ) > 0:
                        return choices[-1]['content']
                    
                # other wise means failed
                print('get GLM response failed, retrying...')
                # sleep for 1 second
                time.sleep( sleep_interval )
        else:
            print('submit GLM request failed, please check your api key and model name')
            return ''
    
    def print_prompt(self):
        for message in self.prompts:
            print(f"{message['role']}: {message['content']}")