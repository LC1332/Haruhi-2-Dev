
import os

from .utils import luotuo_openai_embedding, tiktokenizer

from .utils import response_postprocess

from .utils import cached

def get_text_from_data( data ):
    if "text" in data:
        return data['text']
    elif "enc_text" in data:
        from .utils import base64_to_string
        return base64_to_string( data['enc_text'] )
    else:
        print("warning! failed to get text from data ", data)
        return ""
    
def get_db_from_type( db_type ):
    if db_type in ["chroma","Chroma","ChromaDB","chromadb"]:
        from .ChromaDB import ChromaDB
        ans = ChromaDB()
        return ans
    elif db_type in ["naive"]:
        from .NaiveDB import NaiveDB
        ans = NaiveDB()
        return ans
    else:
        try:
            from .ChromaDB import ChromaDB
            ans = ChromaDB()
        except:
            ans = NaiveDB()
        return ans


class ChatHaruhi:

    def __init__(self, system_prompt = None, \
                 role_name = None, role_from_hf = None,
                 role_from_jsonl = None,  \
                 story_db=None, story_text_folder = None, \
                 llm = 'openai', \
                 embedding = 'luotuo_openai', \
                 max_len_story = None, max_len_history = None,
                 verbose = False,
                 db_type = None):
        super(ChatHaruhi, self).__init__()
        self.verbose = verbose

        # constants
        self.story_prefix_prompt = "Classic scenes for the role are as follows:\n"
        self.k_search = 19
        self.narrator = ['旁白', '', 'scene','Scene','narrator' , 'Narrator']
        self.dialogue_divide_token = '\n###\n'
        self.dialogue_bra_token = '「'
        self.dialogue_ket_token = '」'

        if system_prompt:
            self.system_prompt = self.check_system_prompt( system_prompt )

        # TODO: embedding should be the seperately defined, so refactor this part later
        if llm == 'openai':
            # self.llm = LangChainGPT()
            self.llm, self.tokenizer = self.get_models('openai')
        elif llm == 'debug':
            self.llm, self.tokenizer = self.get_models('debug')
        elif llm == 'spark':
            self.llm, self.tokenizer = self.get_models('spark')
        elif llm == 'GLMPro':
            self.llm, self.tokenizer = self.get_models('GLMPro')
        elif llm == 'GLM3Turbo':
            self.llm, self.tokenizer = self.get_models('GLM3Turbo')
        elif llm == "GLM4":
            self.llm, self.tokenizer = self.get_models('GLM4')
        elif llm == 'ChatGLM2GPT':
            self.llm, self.tokenizer = self.get_models('ChatGLM2GPT')
            self.story_prefix_prompt = '\n'
        elif llm == "BaiChuan2GPT":
            self.llm, self.tokenizer = self.get_models('BaiChuan2GPT')
        elif llm == "BaiChuanAPIGPT":
            self.llm, self.tokenizer = self.get_models('BaiChuanAPIGPT')
        elif llm == "ernie3.5":
            self.llm, self.tokenizer = self.get_models('ernie3.5')
        elif llm == "ernie4.0":
            self.llm, self.tokenizer = self.get_models('ernie4.0')
        elif llm == "foo" or llm == "Foo":
            self.llm, self.tokenizer = self.get_models('foo')
        elif "qwen" in llm:
            self.llm, self.tokenizer = self.get_models(llm)
        else:
            print(f'warning! undefined llm {llm}, use openai instead.')
            self.llm, self.tokenizer = self.get_models('openai')

        if embedding == 'luotuo_openai':
            self.embedding = luotuo_openai_embedding
        elif embedding == 'bge_en':
            from .utils import get_bge_embedding
            self.embedding = get_bge_embedding
        elif embedding == 'bge_zh':
            from .utils import get_bge_zh_embedding
            self.embedding = get_bge_zh_embedding
        else:
            print(f'warning! undefined embedding {embedding}, use luotuo_openai instead.')
            self.embedding = luotuo_openai_embedding

        self.db_type = db_type
        
        if role_name:

            self.role_name = role_name # although it seems that the name will be automatically assigned

            from .role_name_to_file import get_en_role_name
            en_role_name = get_en_role_name( role_name )

            role_from_hf = "silk-road/ChatHaruhi-RolePlaying/" + en_role_name
            
            # # TODO move into a function
            # from .role_name_to_file import get_folder_role_name
            # # correct role_name to folder_role_name
            # role_name, url = get_folder_role_name(role_name)

            # unzip_folder = f'./temp_character_folder/temp_{role_name}'
            # db_folder = os.path.join(unzip_folder, f'content/{role_name}')
            # system_prompt = os.path.join(unzip_folder, f'content/system_prompt.txt')

            # if not os.path.exists(unzip_folder):
            #     # not yet downloaded
            #     # url = f'https://github.com/LC1332/Haruhi-2-Dev/raw/main/data/character_in_zip/{role_name}.zip'
            #     import requests, zipfile, io
            #     r = requests.get(url)
            #     z = zipfile.ZipFile(io.BytesIO(r.content))
            #     z.extractall(unzip_folder)

            # if self.verbose:
            #     print(f'loading pre-defined character {role_name}...')
            # if self.db_type == None:
            #     self.db_type = "chroma"
            # elif not self.db_type in ["chroma","Chroma","ChromaDB","chromadb"]:
            #     print("warning! directly load folder from dbtype ", self.db_type, " has not been implemented yet, change back to chroma, or try use role_from_hf to load role instead")
            #     self.db_type = "chorma"
            # self.db = get_db_from_type(self.db_type)
            # self.db.load(db_folder)
            # self.system_prompt = self.check_system_prompt(system_prompt)

        if role_from_hf:

            self.role_name = role_from_hf # ensure that characters load this way also get their names

            if self.db_type == None:
                self.db_type = "naive"

            from datasets import load_dataset

            if role_from_hf.count("/") == 1:
                dataset = load_dataset(role_from_hf)
                datas = dataset["train"]
            elif role_from_hf.count("/") >= 2:
                split_index = role_from_hf.index('/') 
                second_split_index = role_from_hf.index('/', split_index+1)
                dataset_name = role_from_hf[:second_split_index] 
                split_name = role_from_hf[second_split_index+1:]
                
                fname = split_name + '.jsonl'
                dataset = load_dataset(dataset_name,data_files={'train':fname})
                datas = dataset["train"]
            
            if embedding == 'luotuo_openai':
                embed_name = 'luotuo_openai'
            elif embedding == 'bge_en':
                embed_name = 'bge_en_s15'
            elif embedding == 'bge_zh':
                embed_name = 'bge_zh_s15'
            else:
                print('warning! unkown embedding name ', embedding ,' while loading role')
                embed_name = 'luotuo_openai'

            texts, vecs, self.system_prompt = self.extract_text_vec_from_datas(datas, embed_name)

            self.build_story_db_from_vec( texts, vecs )

        elif role_from_jsonl:
            if self.db_type == None:
                self.db_type = "naive"

            import json
            datas = []
            with open( role_from_jsonl , encoding="utf-8") as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        # 逐行处理JSON数据
                        datas.append(data)
                    except:
                        print("warning! failed to load json line ", line)

            if embedding == 'luotuo_openai':
                embed_name = 'luotuo_openai'
            elif embedding == 'bge_en':
                embed_name = 'bge_en_s15'
            elif embedding == 'bge_zh':
                embed_name = 'bge_zh_s15'
            else:
                print('warning! unkown embedding name ', embedding ,' while loading role')
                embed_name = 'luotuo_openai'

            texts, vecs, self.system_prompt = self.extract_text_vec_from_datas(datas, embed_name)

            self.build_story_db_from_vec( texts, vecs )
            
        elif story_db:
            if self.db_type == None:
                self.db_type = "chroma"
            elif not self.db_type in ["chroma","Chroma","ChromaDB","chromadb"]:
                print("warning! directly load folder from dbtype ", self.db_type, " has not been implemented yet, change back to chroma,or try use role_from_hf to load role instead")
                self.db_type = "chorma"
            self.db = get_db_from_type(self.db_type)
            self.db.load(story_db)
        elif story_text_folder:
            if self.db_type == None:
                self.db_type = "naive"
            # print("Building story database from texts...")
            self.db = self.build_story_db(story_text_folder) 
        else:
            self.db = None
            print('warning! database not yet figured out, both story_db and story_text_folder are not inputted.')
            # raise ValueError("Either story_db or story_text_folder must be provided")
        

        self.max_len_story, self.max_len_history = self.get_tokenlen_setting('openai')

        if max_len_history is not None:
            self.max_len_history = max_len_history
            # user setting will override default setting

        if max_len_story is not None:
            self.max_len_story = max_len_story
            # user setting will override default setting

        self.dialogue_history = []

    def extract_text_vec_from_datas( self, datas, embed_name ):
        # extract text and vec from huggingface dataset
        # return texts, vecs
        from .utils import base64_to_float_array

        texts = []
        vecs = []
        for data in datas:
            if data[embed_name] == 'system_prompt':
                system_prompt = get_text_from_data( data )
            elif data[embed_name] == 'config':
                pass
            else:
                vec = base64_to_float_array( data[embed_name] )
                text = get_text_from_data( data )
                vecs.append( vec )
                texts.append( text )
        return texts, vecs, system_prompt

        

    def check_system_prompt(self, system_prompt):
        # if system_prompt end with .txt, read the file with utf-8
        # else, return the string directly
        if system_prompt.endswith('.txt'):
            with open(system_prompt, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return system_prompt
    

    def get_models(self, model_name):

        # TODO: if output only require tokenizer model, no need to initialize llm
        
        # return the combination of llm, embedding and tokenizer
        if model_name == 'openai':
            from .LangChainGPT import LangChainGPT
            return (LangChainGPT(), tiktokenizer)
        elif model_name == 'debug':
            from .PrintLLM import PrintLLM
            return (PrintLLM(), tiktokenizer)
        elif model_name == 'spark':
            from .SparkGPT import SparkGPT
            return (SparkGPT(), tiktokenizer)
        elif model_name == 'GLMPro':
            from .GLMPro import GLMPro
            return (GLMPro(), tiktokenizer)
        elif model_name == 'GLM3Turbo':
            from .GLMAPI import GLMAPI
            return (GLMAPI(model="glm-3-turbo"), tiktokenizer)
        elif model_name == 'GLM4':
            from .GLMAPI import GLMAPI
            return (GLMAPI(model="glm-4"),tiktokenizer)
        elif model_name == 'ernie3.5':
            from .ErnieGPT import ErnieGPT
            return (ErnieGPT(), tiktokenizer)
        elif model_name == 'ernie4.0':
            from .ErnieGPT import ErnieGPT
            return (ErnieGPT(model="ernie-bot-4"), tiktokenizer)
        elif model_name == "ChatGLM2GPT":
            from .ChatGLM2GPT import ChatGLM2GPT, GLM_tokenizer
            return (ChatGLM2GPT(), GLM_tokenizer)
        elif model_name == "BaiChuan2GPT":
            from .BaiChuan2GPT import BaiChuan2GPT, BaiChuan_tokenizer
            return (BaiChuan2GPT(), BaiChuan_tokenizer)
        elif model_name == "BaiChuanAPIGPT":
            from .BaiChuanAPIGPT import BaiChuanAPIGPT
            return (BaiChuanAPIGPT(), tiktokenizer)
        elif model_name == "foo":
            from .FooLLM import FooLLM
            return (FooLLM(), tiktokenizer)
        elif "qwen" in model_name:
            if model_name == "qwen118k_raw":
                from .Qwen118k2GPT import Qwen118k2GPT, Qwen_tokenizer
                return (Qwen118k2GPT(model = "Qwen/Qwen-1_8B-Chat"), Qwen_tokenizer)
            from huggingface_hub import HfApi 
            from huggingface_hub.hf_api import ModelFilter
            qwen_api = HfApi()
            qwen_models = qwen_api.list_models(
                filter = ModelFilter(model_name=model_name),
                author = "silk-road"             
            )
            qwen_models_id = []
            for qwen_model in qwen_models:
                qwen_models_id.append(qwen_model.id)
                # print(model.id)
            if "silk-road/" + model_name in qwen_models_id:
                from .Qwen118k2GPT import Qwen118k2GPT, Qwen_tokenizer
                return (Qwen118k2GPT(model = "silk-road/" + model_name), Qwen_tokenizer)
            else:
                print(f'warning! undefined model {model_name}, use openai instead.')
                from .LangChainGPT import LangChainGPT
                return (LangChainGPT(), tiktokenizer) 
            # print(models_id)
        else:
            print(f'warning! undefined model {model_name}, use openai instead.')
            from .LangChainGPT import LangChainGPT
            return (LangChainGPT(), tiktokenizer)
        
    def get_tokenlen_setting( self, model_name ):
        # return the setting of story and history token length
        if model_name == 'openai':
            return (1500, 1200)
        else:
            print(f'warning! undefined model {model_name}, use openai instead.')
            return (1500, 1200)
        
    def build_story_db_from_vec( self, texts, vecs ):
        self.db = get_db_from_type(self.db_type)

        self.db.init_from_docs( vecs, texts)

    def build_story_db(self, text_folder):
        # 实现读取文本文件夹,抽取向量的逻辑
        db = get_db_from_type(self.db_type)

        strs = []

        # scan all txt file from text_folder
        for file in os.listdir(text_folder):
            # if file name end with txt
            if file.endswith(".txt"):
                file_path = os.path.join(text_folder, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    strs.append(f.read())

        if self.verbose:
            print(f'starting extract embedding... for { len(strs) } files')

        vecs = []

        ## TODO: 建立一个新的embedding batch test的单元测试
        ## 新的支持list batch test的embedding代码
        ## 用新的代码替换下面的for循环
        ## Luotuo-bert-en也发布了，所以可以避开使用openai
        
        for mystr in strs:
            vecs.append(self.embedding(mystr))

        db.init_from_docs(vecs, strs)

        return db
    
    def save_story_db(self, db_path):
        self.db.save(db_path)

    def generate_prompt( self, text, role):
        from .FooLLM import FooLLM
        if isinstance(self.llm, FooLLM):
            prompt = ""
            messages = self.generate_messages( text, role )
            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                if role == "AI":
                    prompt += content + "\n"
                elif role == "System":
                    prompt += content + "\n"
                elif role == "User":
                    prompt += content + "\n"
            return prompt
        else:
            print("suggest to set llm = foo later")
            from langchain.schema import (
                AIMessage,
                HumanMessage,
                SystemMessage
            )
            messages = self.generate_messages( text, role )
            prompt = ""
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    prompt += msg.content + "\n"
                elif isinstance(msg, AIMessage):
                    prompt += msg.content + "\n"
                elif isinstance(msg, SystemMessage):
                    prompt += msg.content + "\n"
            return prompt


    def generate_messages( self, text, role):
        # add system prompt
        self.llm.initialize_message()
        self.llm.system_message(self.system_prompt)

        # add story
        query = self.get_query_string(text, role)
        self.add_story( query )
        self.last_query = query

        # add history
        self.add_history()

        # add query
        self.llm.user_message(query)

        return self.llm.messages
    
    def append_response( self, response, last_query = None ):
        if last_query == None:
            last_query_record = ""
            if hasattr( self, "last_query" ):
                last_query_record = self.last_query
        else:
            last_query_record = last_query

        # record dialogue history
        self.dialogue_history.append((last_query_record, response))

    @cached  
    def chat(self, text, role):
        # add system prompt
        self.llm.initialize_message()
        self.llm.system_message(self.system_prompt)
    

        # add story
        query = self.get_query_string(text, role)
        self.add_story( query )

        # add history
        self.add_history()

        # add query
        self.llm.user_message(query)
        
        # get response
        response_raw = self.llm.get_response()

        response = response_postprocess(response_raw, self.dialogue_bra_token, self.dialogue_ket_token)

        # record dialogue history
        self.dialogue_history.append((query, response))



        return response
    
    def get_query_string(self, text, role):
        if role in self.narrator:
            return role + ":" + text
        else:
            return f"{role}:{self.dialogue_bra_token}{text}{self.dialogue_ket_token}"
        
    def add_story(self, query):

        if self.db is None:
            return
        
        query_vec = self.embedding(query)

        stories = self.db.search(query_vec, self.k_search)
        
        story_string = self.story_prefix_prompt
        sum_story_token = self.tokenizer(story_string)
        
        for story in stories:
            story_token = self.tokenizer(story) + self.tokenizer(self.dialogue_divide_token)
            if sum_story_token + story_token > self.max_len_story:
                break
            else:
                sum_story_token += story_token
                story_string += story + self.dialogue_divide_token

        self.llm.user_message(story_string)
        
    def add_history(self):

        if len(self.dialogue_history) == 0:
            return
        
        sum_history_token = 0
        flag = 0
        for query, response in reversed(self.dialogue_history):
            current_count = 0
            if query is not None:
                current_count += self.tokenizer(query) 
            if response is not None:
                current_count += self.tokenizer(response)
            sum_history_token += current_count
            if sum_history_token > self.max_len_history:
                break
            else:
                flag += 1

        if flag == 0:
            print('warning! no history added. the last dialogue is too long.')

        for (query, response) in self.dialogue_history[-flag:]:
            if query is not None:
                self.llm.user_message(query)
            if response is not None:
                self.llm.ai_message(response)
