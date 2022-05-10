import pandas as pd
import jieba
import re
import jieba.posseg as pseg
from thefuzz import process
import random

path='./nlu/recognize_entity_and_reply/data/'
corpus_name=path+"corpus_new_modify.xlsx"
corpus=pd.read_excel(corpus_name)
#加载自定义词典--根据石油钻井平台定制
jieba.load_userdict(path+'dict2.txt')


def find_question(corpus,label):
    """
    :param corpus: 语料 以pandas series格式
    :param label: 分类的类型 int
    :return: 指定label下的question list格式
    """
    question_list = corpus['question'][corpus.label == label].values.tolist()
    return question_list

def find_entity(question):
    """
    :param question: str 问题
    :return: two entities
    """
    print('问题：', question)
    seg_list = pseg.cut(question)
    components = []
    indicators = []
    times=[]
    for word, flag in seg_list:
        #print('%s %s' % (word, flag))
        if flag == 'bj': #部件类
            components.append(word)
        if flag == 'zb': #指标类
            indicators.append(word)
        if flag == 't':  #时间
            times.append(word)
    return components,indicators,times

def answer_retrieval(label,question):
    components, indicators, time = find_entity(question)
    if label == 'reason':
    #故障类根据问题和KG里的entity做相似度匹配，相似度>=50 则会回复KG entity中相应的答案
        KG_0_name=path+'KG_symptom_reason.xlsx'
        KG_symptom_reason=pd.read_excel(KG_0_name)
        KG_0_symptoms=KG_symptom_reason['symptom'].values.tolist()
        KG_0_reason=KG_symptom_reason['reason'].values.tolist()
        KG_entity,score=process.extractOne(question, KG_0_symptoms)[0],process.extractOne(question, KG_0_symptoms)[1]
        if score >=50:
            idx=KG_0_symptoms.index(KG_entity)
            answer=KG_0_reason[idx]
            print("该问题的原因是：", answer)
            flag=1
            return flag,answer
        elif 20<= score <50:
            flag = 2
            print("请问您问的是",KG_entity,"的故障原因吗？")
            judge=input("请回复Y/N：")
            if judge == 'Y':
                return flag,KG_entity
            else:
                print("很抱歉没有理解你的意思呢~")
        else:
            print("很抱歉没有理解你的意思呢~")
            flag=3
            return flag,flag
    elif label == 'solution':
        KG_1_name=path+'KG_symptom_solution.xlsx'
        KG_symptom_solution=pd.read_excel(KG_1_name)
        KG_1_symptoms=KG_symptom_solution['symptom'].values.tolist()
        KG_1_solutions=KG_symptom_solution['solution'].values.tolist()
        KG_entity,score=process.extractOne(question, KG_1_symptoms)[0],process.extractOne(question, KG_1_symptoms)[1]
        if score >=50:
            idx=KG_1_symptoms.index(KG_entity)
            answer=KG_1_solutions[idx]
            print("该问题的解决方法是：", answer)
            flag=1
            return flag,answer
        elif 20 <= score < 50:
            print("请问您问的是",KG_entity,"的解决方法吗？")
            flag=2
            judge = input("请回复Y/N：")
            if judge == 'Y':
                return flag, KG_entity
            else:
                print("您说的我有点不明白，您可以换个问法问我哦~")
        else:
            print("您说的我有点不明白，您可以换个问法问我哦~")
            flag=3
            return flag,flag
    elif label == 'maintenance':
        KG_4_name = path+'KG_component_maintenance.xlsx'
        KG_component_maintenance = pd.read_excel(KG_4_name)
        KG_4_components = KG_component_maintenance['component'].values.tolist()
        KG_4_maintenances = KG_component_maintenance['maintenance'].values.tolist()
        idxes = []
        for component in components:
            try:
                idx = KG_4_components.index(component)
                idxes.append(idx)
            except ValueError:
                pass  # do nothing!
        if len(idxes):
            answer=KG_4_maintenances[idxes[-1]]
            print(KG_4_components[idxes[-1]],"的保养方法是：", answer)
            flag=1
            return flag,answer
        else:
            flag = 2
            randlist=random.sample(range(0,len(KG_4_components)),2)
            print("请问您想对哪个部件进行保养查询，如",KG_4_components[randlist[0]],",",KG_4_components[randlist[1]],"等")
            judge = input("请回复上述任一部件：")
            if judge != KG_4_components[randlist[0]] and judge != KG_4_components[randlist[1]]:
                print("非常抱歉，我还不知道如何回答您，我正在努力学习中~")
                flag=3
            return flag, judge

    elif label == 'monitor' or  label == 'other' :
        print("非常抱歉，我还不知道如何回答您，我正在努力学习中~")
        flag=3
        return flag,flag


def knowledge_reply_main(question, label):
    flag, item = answer_retrieval(label, question)

    runs = 5
    for run in range(runs):
        if flag == 2:
            flag, item = answer_retrieval(label, item)
            if flag == 1 or flag == 3:
                break
        elif flag == 1 or flag == 3:
            break
    if run + 1 == runs:
        print("非常抱歉，我还不知道如何回答您，我正在努力学习中~")

    return

# if __name__ == '__main__':
#     label = 0
#     list_questions = find_question(corpus, label)
#
#     question = list_questions[1]
#     flag, item = answer_retrieval(label, question)
#
#     runs = 5
#     for run in range(runs):
#         if flag == 2:
#             flag, item = answer_retrieval(label, item)
#             if flag == 1 or flag == 3:
#                 break
#         elif flag == 1 or flag == 3:
#             break
#     if run + 1 == runs:
#         print("非常抱歉，我还不知道如何回答您，我正在努力学习中~")
