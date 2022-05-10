# encoding:utf-8

'''
environment: D:\software\Anaconda\envs\ComplexEquipKGQA
'''

import json
import requests
import random
# from py2neo import Graph

from nlu.sklearn_classification.clf_model import CLFModel
from nlu.intent_recg_fuzz.intent_subrecg_model import *
from nlu.recognize_entity_and_reply.recognize_entity import *

# from utils.json_utils import dump_user_dialogue_context, load_user_dialogue_context
from config import *






clf_model=CLFModel('./nlu/sklearn_classification/model_file/')
def classifier(text):
    """
    判断是否是闲聊意图，以及是什么类型
    :param text:
    :return:
    """
    return clf_model.predict(text)

def subintent_classifier(text):
    """
    通过post方式请求知识查询的意图细分类服务
    暂时是基于fuzz实现
    :param text:
    :return: {"label":intent,"confidence":confidence}
    """
    return intent_classifier(text)






# def semantic_parser(text,user):
#     """
#     对用户输入文本进行解析，然后填槽，确定回复策略
#     :param text:
#     :param user:
#     :return:
#             填充slot_info中的["slot_values"]
#             填充slot_info中的[“intent_strategy”]
#     """
#     # 对知识查询意图进行二次分类
#     intent_receive=intent_classifier(text)
#     print("subintent_receive:",intent_receive)
#     return intent_receive




def chitchat_bot(intent):
    """
    如果是闲聊，就从闲聊回复语料里随机选择一个返回给用户
    :param inten:
    :return:
    """
    return random.choice(chitchat_corpus.get(intent))

def medical_bot(text,user):
    """
    如果确定是知识查询意图，则使用该函数进行问答
    :param text:
    :param user:
    :return:
    """
    # 对知识查询意图进行二次分类
    intent_receive = subintent_classifier(text)
    print("subintent_receive:", intent_receive)
    confidence=intent_receive['confidence']
    knowledge_reply_main(text, intent_receive['label'])
    return



