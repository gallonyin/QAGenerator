"""
    目标：将大段文档通过gpt3.5识别变成一问一答的问答对。
    流程：1.gpt自动获取合适的问题；2.gpt自动根据问题和文档生成问答对。
    优点：几乎无需人工介入，自动获取问题，自动根据问题生成问答对。
    缺点：受限于大模型输入长度限制，可能无法一次性输入全部文档。
    建议：使用gpt3.5-16k可以一次输入大量文本。

    FAQ：
    1.Q：gpt两个步骤是否可以合并成一个请求让gpt返回，可以节省约一半的时间和tokens？
      A：拆成两次主要是因为问题可能需要人工微调修改后再去生成答案，这样可以提高知识库质量，当然也可以全部自动处理。
    2.Q：大模型有字数限制无法大文档一次输入？
      A：目前这个没有好的解决办法，只能通过预先拆分大文档为多个文档片段后分批执行。
"""
import datetime
import time

import requests


url = 'http://proxy.chat.carlife.host/v1/chat/completions'

# 替换为您自己的API密钥
api_key = 'sk-xxx'

model = "gpt-3.5-turbo-16k"

prompt1 = '''
#01 你是一个问答对数据集处理专家。

#02 你的任务是根据我给出的内容，生成适合作为问答对数据集的问题。

#03 问题要尽量短，不要太长。

#04 一句话中只能有一个问题。

#05 生成的问题必须宏观、价值，不要生成特别细节的问题。

#06 生成问题示例：

"""

权益型基金的特点有哪些方面？

介绍一下产品经理。

"""

#07 以下是我给出的内容：

"""

{{此处替换成你的内容}}

"""
'''

prompt2 = '''
#01 你是一个问答对数据集处理专家。

#02 你的任务是根据我的问题和我给出的内容，生成对应的问答对。

#03 答案要全面，多使用我的信息，内容要更丰富。

#04 你必须根据我的问答对示例格式来生成：

"""

{"content": "基金分类有哪些", "summary": "根据不同标准，可以将证券投资基金划分为不同的种类：（1）根据基金单位是否可增加或赎回，可分为开放式基金和封闭式基金。开放式基金不上市交易（这要看情况），通过银行、券商、基金公司申购和赎回，基金规模不固定；封闭式基金有固定的存续期，一般在证券交易场所上市交易，投资者通过二级市场买卖基金单位。（2）根据组织形态的不同，可分为公司型基金和契约型基金。基金通过发行基金股份成立投资基金公司的形式设立，通常称为公司型基金；由基金管理人、基金托管人和投资人三方通过基金契约设立，通常称为契约型基金。我国的证券投资基金均为契约型基金。（3）根据投资风险与收益的不同，可分为成长型、收入型和平衡型基金。（4）根据投资对象的不同，可分为股票基金、债券基金、货币基金和混合型基金四大类。"}

{"content": "基金是什么", "summary": "基金，英文是fund，广义是指为了某种目的而设立的具有一定数量的资金。主要包括公积金、信托投资基金、保险基金、退休基金，各种基金会的基金。从会计角度透析，基金是一个狭义的概念，意指具有特定目的和用途的资金。我们提到的基金主要是指证券投资基金。"}

#05 我的问题如下：

"""

{{此处替换成你上一步生成的问题}}

"""

#06 我的内容如下：

"""

{{此处替换成你的内容}}

"""
'''


def generate_question(text_content, more=False):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    content = "生成适合作为问答对的问题"
    if more:
        content = "尽可能多生成适合作为问答对的问题"
    prompt = prompt1.replace("{{此处替换成你的内容}}", text_content)
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": content}
        ]
    }
    start_time = time.time()
    response = requests.post(url, headers=headers, json=data, verify=False)
    print("耗时", time.time() - start_time)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]['content']
    else:
        print(f"Error: {response.status_code}")
        print(response.content)
        return None


def generate_qa(text_content, question_text=None):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    prompt = prompt2.replace("{{此处替换成你上一步生成的问题}}", question_text).replace("{{此处替换成你的内容}}", text_content)
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "拼成问答对"}
        ]
    }
    start_time = time.time()
    response = requests.post(url, headers=headers, json=data, verify=False)
    print("耗时", time.time() - start_time)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]['content']
    else:
        print(f"Error: {response.status_code}")
        print(response.content)
        return None


def write_to_file(content):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"new_file_{timestamp}.txt"
    with open(file_name, "w") as file:
        file.write(content)
    print("File 'new_file.txt' has been created and written.")


def read_file(file_name):
    try:
        with open(file_name, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")


def main():
    text_content = read_file("input_file.txt")
    print('text_content\n', text_content)
    question_text = generate_question(text_content=text_content, more=True)
    print('question_text\n', question_text)
    qa_text = generate_qa(text_content=text_content, question_text=question_text)
    print('qa_text\n', qa_text)
    write_to_file(qa_text)


main()
