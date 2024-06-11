

import json

import requests


class AiStoreAzureGPTNode:
    def __init__(self):
        # self.__client = OpenAI()
        self.session_history = []  # 用于存储会话历史的列表
        self.seed=0
        self.system_content="You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."

    @classmethod
    def INPUT_TYPES(cls):
        model_list=[
                    "gpt-3.5",
                    "gpt-4",
                    "gpt-4o"
                    ]
        return {
            "required": {
                "api_key":("STRING", {"default": "api-key", "multiline": True,"dynamicPrompts": False}),
                "api_url":("STRING", {"default": "http://ai.com/api", "multiline": True,"dynamicPrompts": False}),
                "prompt": ("STRING", {"default":"hi","multiline": True,"dynamicPrompts": False}),
                "system_content": ("STRING", 
                                   {
                                       "default": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible.", 
                                       "multiline": True,"dynamicPrompts": False
                                       }),
                "model": ( model_list,  {"default": model_list[0]}),
                "seed": ("INT", {"default": 1, "min": 0, "max": 0xffffffffffffffff, "step": 1}),
                "context_size":("INT", {"default": 1, "min": 0, "max":30, "step": 1}),
            },
             "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    RETURN_TYPES = ("STRING","STRING","STRING",)
    RETURN_NAMES = ("text","messages","session_history",)
    FUNCTION = "generate_contextual_text"
    CATEGORY = "Liam/LLM"
    INPUT_IS_LIST = False
    OUTPUT_IS_LIST = (False,False,False,)

    def generate_contextual_text(self,
                                 api_key,
                                 api_url, 
                                 prompt, 
                                 system_content,
                                 model, 
                                seed,context_size,unique_id = None, extra_pnginfo=None):
        # 可以选择保留会话历史以维持上下文记忆
        # 或者在此处清除会话历史 self.session_history.clear()
        if seed!=self.seed:
            self.seed=seed
            self.session_history=[]
        
        # 把系统信息和初始信息添加到会话历史中
        if system_content:
            self.system_content=system_content
        # 把用户的提示添加到会话历史中
        # 调用API时传递整个会话历史
        session_history=crop_list_tail(self.session_history,context_size)
        messages=[{"role": "system", "content": self.system_content}]+session_history+[{"role": "user", "content": prompt}]
        # 调用API
        response_content = chat(api_key,api_url,messages)
        
        self.session_history=self.session_history+[{"role": "user", "content": prompt}]+[{'role':'assistant',"content":response_content}]
        
        return (response_content,json.dumps(messages, indent=4),json.dumps(self.session_history, indent=4),)

def chat(key,url,messages, max_tokens=1024,temperature=0,top_p=0.95,stream=False):
    input = generate_http_input(messages, max_tokens,temperature,top_p,stream)
    output = get_ai_store_chat(key,url,input, only_msg=True)
    return output

# 加工输入参数
def generate_http_input(messages, max_tokens=1024,temperature=0,top_p=0.95,stream=False):
    input = {
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "messages": messages,
        "stream": stream
    }
    return input

def get_ai_store_chat(key,url,input_json={}, only_msg = False):
        # Set the headers
        headers = {
            'Content-Type': 'application/json',
            'api-key': key
        }
        request_body = input_json
        # Send the request
        response = requests.post(url, headers=headers, data=json.dumps(request_body))
        # Print the msg
        # print(response.json())
        # Get the msg
        if only_msg:
            rs = response.json()
            choices = get_value(rs,'choices', None)
            if choices is None:
                print("[ERROR] get chatgpt:", rs)
                return ""
            return response.json()['choices'][0]['message']['content']
        return response.json()

def crop_list_tail(lst, size):
    if size >= len(lst):
        return lst
    elif size==0:
        return []
    else:
        return lst[-size:]
    
def get_value(db, key, default=''):
    if db and db.__contains__(key):
        return db[key]
    return default