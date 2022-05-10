# -*- coding:utf-8 -*-

import json
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

file="./nlu/intent_recg_fuzz/data/subclassification_data.txt"

def sigmoid(x):
    return 1./(1.+np.exp(-x))

def intent_classifier(text):
    """
    用fuzz的方法进行用户意图细分类
    :param text:
    :return:
    """
    with open(file, 'r') as dic:
        choices = json.load(dic)
    a= process.extractOne(text, choices["choices_0"], scorer=fuzz.token_set_ratio)
    b = process.extractOne(text, choices["choices_1"], scorer=fuzz.token_set_ratio)
    c = process.extractOne(text, choices["choices_2"], scorer=fuzz.token_set_ratio)
    d = process.extractOne(text, choices["choices_3"], scorer=fuzz.token_set_ratio)
    e = process.extractOne(text, choices["choices_4"], scorer=fuzz.token_set_ratio)
    score = [a[1], b[1], c[1], d[1], e[1]]
    total=sum(score)
    if max(score) == a[1]:
        label = "reason"
        confidence=a[1]/total
    if max(score) == b[1]:
        label = "solution"
        confidence = b[1] / total
    if max(score) == c[1]:
        label = "maintenance"
        confidence = c[1] / total
    if max(score) == d[1]:
        label = "monitor"
        confidence = d[1] / total
    if max(score) == e[1]:
        label = "others"
        confidence = e[1] / total
    output={"label":label, "confidence": sigmoid(confidence)}

    return output


# if __name__ == '__main__':
#     text="请问噪声大是什么原因"
#     output= intent_classifier(text)
#     print(output)




