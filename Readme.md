## ChatHaruhi2.0的测试项目

主要用于开发和测试ChatHaruhi2.0

主要是原项目太大了每次clone和测试太慢

这个项目会在2.0初步功能开发完成后关闭。

请大家回去找原项目 https://github.com/LC1332/Chat-Haruhi-Suzumiya

- 选择性移除了ChatHaruhi( https://github.com/LC1332/Haruhi-2-Dev ) 下chromadb的依赖 ，在text_folder载入, hugging_face载入和jsonl载入下 默认使用一个NaiveDB而不是ChromaDB。
- TODO: 增加adapter，支持即使用openai建库仍然可以用任意的embedding进行query

# ChatHaruhi2.0的文档

## 初步使用

目前ChatHaruhi可以使用pip直接安装

```shell
pip -q install chatharuhi
```

依赖的库为

```shell
pip -q install transformers openai tiktoken langchain datasets
```

### 从hugging face载入角色

从hugging face载入一个数据集，接口是这样的

```python
from chatharuhi import ChatHaruhi

chatbot = ChatHaruhi( role_from_hf = 'silk-road/linghuchong', \
                      llm = 'openai')

response = chatbot.chat(role='小师妹', text = '冲哥。')
print(response)
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

**role_name = 的载入方式仍然依赖chromaDB**

### HuggingFace和jsonl载入

目前推荐jsonl或者Hugging Face的方式载入，如下:

这些角色可以通过

```python
chatbot = ChatHaruhi( role_from_hf = 'silk-road/ChatHaruhi-from-RoleLLM/Jack-Sparrow', \
                      llm = 'openai',
                      embedding = 'bge_en')
```

这里要求silk-road/ChatHaruhi-from-RoleLLM的数据集项目下必须有Jack-Sparrow.jsonl

也可以使用


```python
chatbot = ChatHaruhi( role_from_hf = 'Your_local_jsonl', \
                      llm = 'openai',
                      embedding = 'bge_en')
```

来进行载入

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

这些角色可以通过语法糖(比如角色名haruhi)进行载入

```python
chatbot = ChatHaruhi( role_name = 'haruhi', llm = 'openai')

response = chatbot.chat(role='阿虚', text = '我看新一年的棒球比赛要开始了！我们要去参加吗？')
print(response)
```

新角色我打算做到hugging face接口上去了，那样可玩性会强一些。

### RoleLLM的95个英文角色

这些角色可以通过

```python
chatbot = ChatHaruhi( role_from_hf = 'silk-road/ChatHaruhi-from-RoleLLM/Jack-Sparrow', \
                      llm = 'openai',
                      embedding = 'bge_en')
```

来载入，如果你希望英文问答，embedding可以选取bge_en， 如果你希望都是中文问答，可以使用默认的（不输入或者输入luotuo_openai）。（这个库我只做了这两个embedding，如果想要更多的embedding需要重新抽取了）

角色 | 电影 | 中文 | 字段 
---|---|---|---
HAL 9000  |  2001-A-Space-Odyssey  |  《2001太空漫游》中的HAL 9000电脑 | silk-road/ChatHaruhi-from-RoleLLM/HAL 9000
Colonel Nathan R. Jessep  |  A-Few-Good-Men  |  《好汉两三个》中的内森·R·杰瑟普上校 | silk-road/ChatHaruhi-from-RoleLLM/Colonel Nathan R. Jessep
Antonio Salieri  |  Amadeus  |  《阿玛迪斯》中的安东尼奥·萨列里 | silk-road/ChatHaruhi-from-RoleLLM/Antonio Salieri
Stifler  |  American-Pie  |  《美国派》中的斯蒂夫勒 | silk-road/ChatHaruhi-from-RoleLLM/Stifler
Paul Vitti  |  Analyze-That  |  《心理分析那件事》中的保罗·维蒂 | silk-road/ChatHaruhi-from-RoleLLM/Paul Vitti
Alvy Singer  |  Annie-Hall  |  《安妮·霍尔》中的阿尔维·辛格 | silk-road/ChatHaruhi-from-RoleLLM/Alvy Singer
Violet Weston  |  August-Osage-County  |  《奥塞奇郡的八月》中的紫罗兰·韦斯顿 | silk-road/ChatHaruhi-from-RoleLLM/Violet Weston
Willie Soke  |  Bad-Santa  |  《坏圣诞老人》中的威利·索克 | silk-road/ChatHaruhi-from-RoleLLM/Willie Soke
Gaston  |  Beauty-and-the-Beast  |  《美女与野兽》中的加斯顿 | silk-road/ChatHaruhi-from-RoleLLM/Gaston
The Dude  |  Big-Lebowski,-The  |  《大勒布斯基》中的“大佬” | silk-road/ChatHaruhi-from-RoleLLM/The Dude
Murphy MacManus  |  Boondock-Saints,-The  |  《天使之城》中的墨菲·麦克马纳斯 | silk-road/ChatHaruhi-from-RoleLLM/Murphy MacManus
Paul Conroy  |  Buried  |  《活埋》中的保罗·康罗伊 | silk-road/ChatHaruhi-from-RoleLLM/Paul Conroy
Truman Capote  |  Capote  |  《卡波特》中的杜鲁门·卡波特 | silk-road/ChatHaruhi-from-RoleLLM/Truman Capote
Mater  |  Cars-2  |  《赛车总动员2》中的玛特 | silk-road/ChatHaruhi-from-RoleLLM/Mater
Andrew Detmer  |  Chronicle  |  《编年史》中的安德鲁·德特默 | silk-road/ChatHaruhi-from-RoleLLM/Andrew Detmer
Coriolanus  |  Coriolanus  |  《科里奥兰纳斯》中的主角 | silk-road/ChatHaruhi-from-RoleLLM/Coriolanus
Benjamin Button  |  Curious-Case-of-Benjamin-Button,-The  |  《本杰明·巴顿奇事》中的本杰明·巴顿 | silk-road/ChatHaruhi-from-RoleLLM/Benjamin Button
John Keating  |  Dead-Poets-Society  |  《死亡诗社》中的约翰·基廷 | silk-road/ChatHaruhi-from-RoleLLM/John Keating
Wade Wilson  |  Deadpool  |  《死侍》中的韦德·威尔逊 | silk-road/ChatHaruhi-from-RoleLLM/Wade Wilson
Jim Morrison  |  Doors,-The  |  《门》中的吉姆·莫里森 | silk-road/ChatHaruhi-from-RoleLLM/Jim Morrison
Queen Elizabeth I  |  Elizabeth-The-Golden-Age  |  《伊丽莎白：黄金时代》中的伊丽莎白一世女王 | silk-road/ChatHaruhi-from-RoleLLM/Queen Elizabeth I
Jeff Spicoli  |  Fast-Times-at-Ridgemont-High  |  《瑞奇蒙特高中时光》中的杰夫·斯皮科利 | silk-road/ChatHaruhi-from-RoleLLM/Jeff Spicoli
Fred Flintstone  |  Flintstones,-The  |  《石头家族》中的弗雷德·弗林斯通 | silk-road/ChatHaruhi-from-RoleLLM/Fred Flintstone
Freddy Krueger  |  Freddy-vs.-Jason  |  《弗雷迪对杰森》中的弗雷迪·克鲁格 | silk-road/ChatHaruhi-from-RoleLLM/Freddy Krueger
Tyrion Lannister  |  Game_of_Thrones  |  《权力的游戏》中的提利昂·兰尼斯特 | silk-road/ChatHaruhi-from-RoleLLM/Tyrion Lannister
James Brown  |  Get-on-Up  |  《起身舞蹈》中的詹姆斯·布朗 | silk-road/ChatHaruhi-from-RoleLLM/James Brown
Walt Kowalski  |  Gran-Torino  |  《老无所依》中的沃尔特·科瓦尔斯基 | silk-road/ChatHaruhi-from-RoleLLM/Walt Kowalski
John Coffey  |  Green-Mile,-The  |  《绿里奇迹》中的约翰·科菲 | silk-road/ChatHaruhi-from-RoleLLM/John Coffey
Theodore Twombly  |  Her  |  《她》中的西奥多·特温布利 | silk-road/ChatHaruhi-from-RoleLLM/Theodore Twombly
Gregory House  |  House-M.D.  |  《豪斯医生》中的格雷戈里·豪斯 | silk-road/ChatHaruhi-from-RoleLLM/Gregory House
Sonny  |  I,-Robot  |  《我，机器人》中的桑尼 | silk-road/ChatHaruhi-from-RoleLLM/Sonny
Colonel Hans Landa  |  Inglourious-Basterds  |  《无耻混蛋》中的汉斯·兰达上校 | silk-road/ChatHaruhi-from-RoleLLM/Colonel Hans Landa
Judge Dredd  |  Judge-Dredd  |  《德莱德法官》中的法官德莱德 | silk-road/ChatHaruhi-from-RoleLLM/Judge Dredd
Juno MacGuff  |  Juno  |  《朱诺》中的朱诺·麦克夫 | silk-road/ChatHaruhi-from-RoleLLM/Juno MacGuff
Po  |  Kung-Fu-Panda  |  《功夫熊猫》中的阿宝 | silk-road/ChatHaruhi-from-RoleLLM/Po
Professor G.H. Dorr  |  Ladykillers,-The  |  《夫人杀手》中的G.H.多尔教授 | silk-road/ChatHaruhi-from-RoleLLM/Professor G.H. Dorr
Fletcher Reede  |  Liar-Liar  |  《撒谎的男人》中的弗莱彻·里德 | silk-road/ChatHaruhi-from-RoleLLM/Fletcher Reede
Abraham Lincoln  |  Lincoln  |  《林肯》中的亚伯拉罕·林肯 | silk-road/ChatHaruhi-from-RoleLLM/Abraham Lincoln
Frank T.J. Mackey  |  Magnolia  |  《木兰花》中的弗兰克 T.J. 麦凯 | silk-road/ChatHaruhi-from-RoleLLM/Frank T.J. Mackey
Malcolm X  |  Malcolm-X  |  《马尔科姆X》中的马尔科姆X | silk-road/ChatHaruhi-from-RoleLLM/Malcolm X
Leonard Shelby  |  Memento  |  《记忆碎片》中的伦纳德·谢尔比 | silk-road/ChatHaruhi-from-RoleLLM/Leonard Shelby
Harvey Milk  |  Milk  |  《牛奶》中的哈维·牛奶 | silk-road/ChatHaruhi-from-RoleLLM/Harvey Milk
Randle McMurphy  |  One-Flew-Over-the-Cuckoo's-Nest  |  《飞越疯人院》中的兰德尔·麦克默菲 | silk-road/ChatHaruhi-from-RoleLLM/Randle McMurphy
Jack Sparrow  |  Pirates-of-the-Caribbean-Dead-Man's-Chest  |  《加勒比海盗》中的杰克·斯派洛船长 | silk-road/ChatHaruhi-from-RoleLLM/Jack Sparrow
John Dillinger  |  Public-Enemies  |  《公敌》中的约翰·迪林格 | silk-road/ChatHaruhi-from-RoleLLM/John Dillinger
Lestat de Lioncourt  |  Queen-of-the-Damned  |  《诅咒女王》中的莱斯塔特·德·莱昂科特 | silk-road/ChatHaruhi-from-RoleLLM/Lestat de Lioncourt
Tyler Hawkins  |  Remember-Me  |  《记得我》中的泰勒·霍金斯 | silk-road/ChatHaruhi-from-RoleLLM/Tyler Hawkins
Caesar  |  Rise-of-the-Planet-of-the-Apes  |  《猩球崛起》中的凯撒 | silk-road/ChatHaruhi-from-RoleLLM/Caesar
Jack  |  Room  |  《房间》中的杰克 | silk-road/ChatHaruhi-from-RoleLLM/Jack
James Carter  |  Rush-Hour-2  |  《尖峰时刻2》中的詹姆斯·卡特 | silk-road/ChatHaruhi-from-RoleLLM/James Carter
Jigsaw  |  Saw  |  《电锯惊魂》中的拼图杀手 | silk-road/ChatHaruhi-from-RoleLLM/Jigsaw
John Doe  |  Se7en  |  《七宗罪》中的约翰·多 | silk-road/ChatHaruhi-from-RoleLLM/John Doe
Jackie Moon  |  Semi-Pro  |  《半职业球员》中的杰基·月亮 | silk-road/ChatHaruhi-from-RoleLLM/Jackie Moon
Sherlock Holmes  |  Sherlock-Holmes  |  《夏洛克·福尔摩斯》中的夏洛克·福尔摩斯 | silk-road/ChatHaruhi-from-RoleLLM/Sherlock Holmes
Shrek  |  Shrek  |  《史莱克》中的史莱克 | silk-road/ChatHaruhi-from-RoleLLM/Shrek
Pat Solitano  |  Silver-Linings-Playbook  |  《乌云背后的幸福线》中的帕特·索利塔诺 | silk-road/ChatHaruhi-from-RoleLLM/Pat Solitano
Karl Childers  |  Sling-Blade  |  《刀锯》中的卡尔·柴尔德斯 | silk-road/ChatHaruhi-from-RoleLLM/Karl Childers
Peter Parker  |  Spider-Man  |  《蜘蛛侠》中的彼得·帕克 | silk-road/ChatHaruhi-from-RoleLLM/Peter Parker
Bruno Antony  |  Strangers-on-a-Train  |  《列车上的陌生人》中的布鲁诺·安东尼 | silk-road/ChatHaruhi-from-RoleLLM/Bruno Antony
Seth  |  Superbad  |  《超级糟糕》中的塞思 | silk-road/ChatHaruhi-from-RoleLLM/Seth
Caden Cotard  |  Synecdoche,-New-York  |  《纽约奇缘》中的卡登·科塔德 | silk-road/ChatHaruhi-from-RoleLLM/Caden Cotard
Travis Bickle  |  Taxi-Driver  |  《出租车司机》中的特拉维斯·比克尔 | silk-road/ChatHaruhi-from-RoleLLM/Travis Bickle
Stanley Ipkiss  |  Mask,-The  |  《面具》中的斯坦利·伊普基斯 | silk-road/ChatHaruhi-from-RoleLLM/Stanley Ipkiss
Lyn Cassady  |  Men-Who-Stare-at-Goats,-The  |  《盯羊的男人》中的林恩·卡萨迪 | silk-road/ChatHaruhi-from-RoleLLM/Lyn Cassady
Michael Scott  |  The_Office  |  《办公室》中的迈克尔·斯科特 | silk-road/ChatHaruhi-from-RoleLLM/Michael Scott
Robert Angier  |  Prestige,-The  |  《名望》中的罗伯特·安吉尔 | silk-road/ChatHaruhi-from-RoleLLM/Robert Angier
Rachel Lang  |  The-Rage-Carrie-2  |  《瑞秋的愤怒：凯丽2》中的瑞秋·朗 | silk-road/ChatHaruhi-from-RoleLLM/Rachel Lang
Dr. Frank-N-Furter  |  Rocky-Horror-Picture-Show,-The  |  《洛奇恐怖秀》中的弗兰克·N·福特医生 | silk-road/ChatHaruhi-from-RoleLLM/Dr. Frank-N-Furter
Jack Torrance  |  Shining,-The  |  《闪灵》中的杰克·托兰斯 | silk-road/ChatHaruhi-from-RoleLLM/Jack Torrance
Tom Ripley  |  Talented-Mr.-Ripley,-The  |  《天才雷普利》中的汤姆·雷普利 | silk-road/ChatHaruhi-from-RoleLLM/Tom Ripley
D_Artagnan  |  Three-Musketeers,-The  |  《三剑客》中的达达尼昂 | silk-road/ChatHaruhi-from-RoleLLM/D_Artagnan
Stephen Hawking  |  Theory-of-Everything,-The  |  《万物理论》中的斯蒂芬·霍金 | silk-road/ChatHaruhi-from-RoleLLM/Stephen Hawking
Thor  |  Thor-Ragnarok  |  《雷神：诸神黄昏》中的雷神索尔 | silk-road/ChatHaruhi-from-RoleLLM/Thor
James Bond  |  Tomorrow-Never-Dies  |  《明日帝国》中的詹姆斯·邦德 | silk-road/ChatHaruhi-from-RoleLLM/James Bond
Mark Renton  |  Trainspotting  |  《迷幻列车》中的马克·伦顿 | silk-road/ChatHaruhi-from-RoleLLM/Mark Renton
Tugg Speedman  |  Tropic-Thunder  |  《热带惊雷》中的塔格·斯皮德曼 | silk-road/ChatHaruhi-from-RoleLLM/Tugg Speedman
David Aames  |  Vanilla-Sky  |  《香草天空》中的大卫·艾姆斯 | silk-road/ChatHaruhi-from-RoleLLM/David Aames
Rorschach  |  Watchmen  |  《守望者》中的罗夏克 | silk-road/ChatHaruhi-from-RoleLLM/Rorschach
Jordan Belfort  |  Wolf-of-Wall-Street,-The  |  《华尔街之狼》中的乔丹·贝尔福特 | silk-road/ChatHaruhi-from-RoleLLM/Jordan Belfort
Logan  |  X-Men-Origins-Wolverine  |  《X战警：金刚狼》中的洛根 | silk-road/ChatHaruhi-from-RoleLLM/Logan
Judy Hoops  |  Zootopia  |  《疯狂动物城》中的朱迪·胡普斯 | silk-road/ChatHaruhi-from-RoleLLM/Judy Hoops
Doctor Who  |  Doctor_Who  |  《神秘博士》中的博士 | silk-road/ChatHaruhi-from-RoleLLM/Doctor Who
Blair Waldorf  |  Gossip_Girl  |  《绯闻女孩》中的布莱尔·沃尔多夫 | silk-road/ChatHaruhi-from-RoleLLM/Blair Waldorf
Raylan Givens  |  Justified  |  《正当防卫》中的雷兰·吉文斯 | silk-road/ChatHaruhi-from-RoleLLM/Raylan Givens
Mary Sibley  |  Salem  |  《塞勒姆》中的玛丽·西布利 | silk-road/ChatHaruhi-from-RoleLLM/Mary Sibley
Lucifer Morningstar  |  Lucifer  |  《路西法》中的路西法·晨星 | silk-road/ChatHaruhi-from-RoleLLM/Lucifer Morningstar
Sheldon Cooper  |  The_Big_Bang_Theory  |  《生活大爆炸》中的谢尔顿·库珀 | silk-road/ChatHaruhi-from-RoleLLM/Sheldon Cooper
Twilight Sparkle  |  My_Little_Pony__Friendship_is_Magic  |  《我的小马驹：友谊之魔》中的暮光星辉 | silk-road/ChatHaruhi-from-RoleLLM/Twilight Sparkle
Oliver Queen  |  Arrow  |  《绿箭侠》中的奥利弗·皇后 | silk-road/ChatHaruhi-from-RoleLLM/Oliver Queen
Leroy Jethro Gibbs  |  NCIS  |  《海军罪案调查处》中的利洛伊·杰斯罗·吉布斯 | silk-road/ChatHaruhi-from-RoleLLM/Leroy Jethro Gibbs
Angel  |  Angel  |  《天使》中的天使 | silk-road/ChatHaruhi-from-RoleLLM/Angel
Klaus Mikaelson  |  The_Originals  |  《始祖家族》中的克劳斯·米卡尔森 | silk-road/ChatHaruhi-from-RoleLLM/Klaus Mikaelson
Queen Catherine  |  Reign  |  《王权》中的凯瑟琳女王 | silk-road/ChatHaruhi-from-RoleLLM/Queen Catherine
Dr. Hannibal Lecter  |  Hannibal  |  《汉尼拔》中的汉尼拔·莱克特医生 | silk-road/ChatHaruhi-from-RoleLLM/Dr. Hannibal Lecter
Coach Eric Taylor  |  Friday_Night_Lights  |  《星期五之光》中的教练埃里克·泰勒 | silk-road/ChatHaruhi-from-RoleLLM/Coach Eric Taylor




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

目前可以通过embedding字段来指定所使用的embedding模型

```python
if embedding == 'luotuo_openai':
    embed_name = 'luotuo_openai'
elif embedding == 'bge_en':
    embed_name = 'bge_en_s15'
```

目前支持这两个，luotuo_openai会在中文下使用luotuo模型，英文下使用openai模型

bge_en会使用bge_small_en_v1.5的模型

## 后处理

