# encoding:utf-8

'''
environment: D:\software\Anaconda\envs\ComplexEquipKGQA
'''

import os
import re
import json

LOGS_DIR="./logs"



def load_user_dialogue_context(user):
    """
    建立对应用户的log文档
    :param user:
    :return:
    """
    path=os.path.join(LOGS_DIR, '{}.json'.format(str(user)))
    if not os.path.exists(path):
        # 第一轮对话接收到accept的闲聊意图，以查询身份回复。
        return {"choice_answer":"hi, 工业设备诊断机器人小夏很高兴为你服务","slot_value":None}
    else:
        # 如果log文档存在，证明不是第一轮对话的accept 待整理
        with open(path,'r', encoding='utf8') as f:
            data=f.read()
            return json.loads(data)