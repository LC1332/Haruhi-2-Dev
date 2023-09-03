## ChatHaruhi2.0的测试项目

主要用于开发和测试ChatHaruhi2.0

主要是原项目太大了每次clone和测试太慢

这个项目会在2.0初步功能开发完成后关闭。

请大家回去找原项目 https://github.com/LC1332/Chat-Haruhi-Suzumiya


# ChatHaruhi2.0的文档

## 初步使用

目前ChatHaruhi可以使用pip直接安装

```shell
pip -q install chatharuhi
```

依赖的库为

```shell
pip -q install transformers openai tiktoken langchain chromadb zhipuai
```

### 使用语法糖载入

安装完成之后可以使用语法糖直接调用

这个例子见[notebook](https://github.com/LC1332/Haruhi-2-Dev/blob/main/notebook/test_GLMPro.ipynb)

```python
from chatharuhi import ChatHaruhi

chatbot = ChatHaruhi( role_name = 'haruhi', llm = 'openai')

response = chatbot.chat(role='阿虚', text = '我看新一年的棒球比赛要开始了！我们要去参加吗？')
print(response)
```

这就可以直接进行调用了。

### 分开载入system_prompt和story_db

更完整的用法，是分开对system_prompt和story_db进行设置

这个例子见[notebook](https://github.com/LC1332/Haruhi-2-Dev/blob/main/notebook/test_LangChainOpenAILLM.ipynb)

```shell
wget -q https://github.com/LC1332/Haruhi-2-Dev/raw/main/data/characters/haruhi/haruhi.zip
unzip -q haruhi.zip -d /content/new_output
```

先下载和解压对应的文件，然后使用更完整的初始化方法

```python
from chatharuhi import ChatHaruhi

db_folder = '/content/new_output/content/haruhi'
system_prompt = '/content/new_output/content/system_prompt.txt'

chatbot = ChatHaruhi( system_prompt = system_prompt,\
                      llm = 'openai' ,\
                      story_db = db_folder)

response = chatbot.chat(role='阿虚', text = 'Haruhi, 你好啊')
print(response)
```

这样就可以使用了。


### 如果story_db还没有被抽取

如果你的人物还没有抽取story_db，可以使用这个方法去初始化

这个例子见[notebook](https://github.com/LC1332/Haruhi-2-Dev/blob/main/notebook/test_PrintLLM.ipynb)

```python
from chatharuhi import ChatHaruhi

text_folder = '/content/Haruhi-2-Dev/data/characters/haruhi/texts'

system_prompt = '/content/Haruhi-2-Dev/data/characters/haruhi/system_prompt.txt'

chatbot = ChatHaruhi( system_prompt = system_prompt,\
                      llm = 'debug' ,\
                      story_text_folder = text_folder)

chatbot.chat(role='阿虚', text = 'Haruhi, 你好啊')
```

这个时候chatbot会自动抽取text_folder中的embedding，时候还可以用

```python
chatbot.save_story_db('/content/haruhi')
```

的方式保存chormaDB到文件夹，下次就不用重新抽取了。基础的用法介绍到这里。后面是更详细的章节

### 计划中的特征

我计划增加一个更方便大家share角色的接口，即从hugging face载入一个数据集，目前计划的接口是这样的

```python
from chatharuhi import ChatHaruhi

chatbot = ChatHaruhi( role_from_hf = 'silk-road/linghuchong', \
                      llm = 'openai')

response = chatbot.chat(role='小师妹', text = '冲哥。')
print(response)
```

有空就到时候实现一下。约定一下hf上需要的格式和规定一下抽取embedding的代码


## 不同LLM的支持

目前支持llm切换为不同的模型。目前支持这些模型

```python
if model_name == 'openai': # openai turbo 3.5 模型
    from .LangChainGPT import LangChainGPT
    return (LangChainGPT(), tiktokenizer)
elif model_name == 'debug': # 用于debug，直接打印出prompt的模型（甚至你可以输入回去表现出正常的行为）
    from .PrintLLM import PrintLLM
    return (PrintLLM(), tiktokenizer)
elif model_name == 'spark': # 星火大模型
    from .SparkGPT import SparkGPT
    return (SparkGPT(), tiktokenizer)
elif model_name == 'GLMPro': # GLMPro的在线接口
    from .GLMPro import GLMPro
    return (GLMPro(), tiktokenizer)
elif model_name == "ChatGLM2GPT": # 通过ChatHaruhi-54K训练得到的模型
    from .ChatGLM2GPT import ChatGLM2GPT, GLM_tokenizer
    return (ChatGLM2GPT(), GLM_tokenizer)
```

现在ChatGLM2的本地模型还有一些bug。正在调试中，百川我们也训练了。有空回头推上去。

## ChatHaruhi Gradio 2.0的部署

现在Gradio的部署非常简单，代码在 https://github.com/LC1332/Chat-Haruhi-Suzumiya/tree/main/ChatHaruhi2.0/gradioDemo 中

## 目前支持的角色

目前role_name支持的角色可以在role_name_to_file中看到。目前是支持这些

```python

role_name_Haruhiu = {'汤师爷': 'tangshiye', 'tangshiye': 'tangshiye', 'Tangshiye': 'tangshiye', 
                     '慕容复': 'murongfu', 'murongfu': 'murongfu', 'Murongfu': 'murongfu', 
                     '李云龙': 'liyunlong', 'liyunlong': 'liyunlong', 'Liyunlong': 'liyunlong', 
                     'Luna': 'Luna', '王多鱼': 'wangduoyu', 'wangduoyu': 'wangduoyu', 
                     'Wangduoyu': 'wangduoyu', 'Ron': 'Ron', '鸠摩智': 'jiumozhi', 
                     'jiumozhi': 'jiumozhi', 'Jiumozhi': 'jiumozhi', 'Snape': 'Snape', 
                     '凉宫春日': 'haruhi', 'haruhi': 'haruhi', 'Haruhi': 'haruhi', 
                     'Malfoy': 'Malfoy', '虚竹': 'xuzhu', 'xuzhu': 'xuzhu', 
                     'Xuzhu': 'xuzhu', '萧峰': 'xiaofeng', 
                     'xiaofeng': 'xiaofeng', 'Xiaofeng': 'xiaofeng', '段誉': 'duanyu', 
                     'duanyu': 'duanyu', 'Duanyu': 'duanyu', 'Hermione': 'Hermione', 
                     'Dumbledore': 'Dumbledore', '王语嫣': 'wangyuyan', 'wangyuyan': 
                     'wangyuyan', 'Wangyuyan': 'wangyuyan', 'Harry': 'Harry', 
                     'McGonagall': 'McGonagall', '白展堂': 'baizhantang', 
                     'baizhantang': 'baizhantang', 'Baizhantang': 'baizhantang', 
                     '佟湘玉': 'tongxiangyu', 'tongxiangyu': 'tongxiangyu', 
                     'Tongxiangyu': 'tongxiangyu', '郭芙蓉': 'guofurong', 
                     'guofurong': 'guofurong', 'Guofurong': 'guofurong', '流浪者': 'wanderer', 
                     'wanderer': 'wanderer', 'Wanderer': 'wanderer', '钟离': 'zhongli', 
                     'zhongli': 'zhongli', 'Zhongli': 'zhongli', '胡桃': 'hutao', 'hutao': 'hutao', 
                     'Hutao': 'hutao', 'Sheldon': 'Sheldon', 'Raj': 'Raj', 
                     'Penny': 'Penny', '韦小宝': 'weixiaobao', 'weixiaobao': 'weixiaobao', 
                     'Weixiaobao': 'weixiaobao', '乔峰': 'qiaofeng', 'qiaofeng': 'qiaofeng', 
                     'Qiaofeng': 'qiaofeng', '神里绫华': 'ayaka', 'ayaka': 'ayaka', 
                     'Ayaka': 'ayaka', '雷电将军': 'raidenShogun', 'raidenShogun': 'raidenShogun', 
                     'RaidenShogun': 'raidenShogun', '于谦': 'yuqian', 'yuqian': 'yuqian', 
                     'Yuqian': 'yuqian', 'Professor McGonagall': 'McGonagall', 
                     'Professor Dumbledore': 'Dumbledore'}

```

新角色我打算做到hugging face接口上去了，那样可玩性会强一些。


## 改变ChatBot的记忆

现在暂时没有暴露这个接口，可以用强行赋值的方法，在chat之前改变chatbot的记忆


```python
from chatharuhi import ChatHaruhi

chatbot = ChatHaruhi( role_name = 'haruhi',\
                      llm = 'openai' )

chatbot.dialogue_history = [('鲁鲁:「Haruhi，我是新同学鲁鲁」','春日:「你好呀鲁鲁」')]

response = chatbot.chat(role='阿虚', text = '这个新同学是什么来头')
print(response)
```

不然chatbot会自己把记忆存储在`chatbot.dialogue_history = []`中。

dialogue_history是一个list of tuple，分别是格式化的user的query和bot的response，也可以是None

None的话，这一行就不会放到记忆里，所以可以去构造单独bot的或者单独user的记忆。

## Embedding模型

目前可以通过embedding字段


## 后处理

