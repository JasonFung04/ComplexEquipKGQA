# encoding:utf-8

'''
environment: D:\software\Anaconda\envs\ComplexEquipKGQA
'''
from flask import Flask, render_template, request, jsonify
import sanic,sanic_cors, sanic_openapi
import json



import os
import itchat
import json

from sanic import Sanic, response
from sanic_cors import CORS
from sanic_openapi import swagger_blueprint, doc

from modules import chitchat_bot, classifier, medical_bot
from utils.json_utils import load_user_dialogue_context
# dump_user_dialogue,


def delete_cache(file_name):
    """
    清除缓存数据，切换账号登入
    :param file_name:
    :return:
    """
    if os.path.exists(file_name):
        os.remove(file_name)

# @itchat.msg_register(["Text"]) #msg_type
# def text_reply(msg):
#     """
#     微信入口
#     :param msg:
#     :return:
#     """
#     user_intent= classifier(msg["Text"])  #对用户输入进行初分类
#     print("user_intent:", user_intent)
#     if user_intent in ["greet","goodbye","deny","isbot"]:
#         reply=chitchat_bot(user_intent)
#
#
#         msg.user.send(reply)


# """"
# 部署网页接口
# """
#app=Sanic(__name__)
#CORS(app)
#
#app.blueprint(swagger_blueprint)
#app.config["API_VERSION"]="0.1"
#app.config["API_ITILE"]="DIALOG_SERVICE: Sanic-OpenAPI"
#
#server_port=int(os.getenv('SERVER_PORT', 8080))
#@app.post("/bot/message")
#@doc.summary("Let us have a chat")
#@doc.consumes(doc.JsonBody({"message": str}), location="body")

def message(sender, text):
    """
    sanic入口
    :param request:
    :return:
    """
    # 获取用户ID和用户输入
    # ps：即使是相同用户，每次对话(多轮)都希望ID是不同的
    # v1版本只做到单轮对话
    #sender=request.json.get("sender")
    #message=request.json.get("message")
    print("sender:{},message:{}".format(sender,text))
    # 判断用户意图是否属于闲聊类
    user_intent = classifier(text)  #---------------------------测试message中问..是什么原因，检测结果为isbot，模型有待进一步训练22/04/26
    print("user_intent:", user_intent)
    if user_intent in ["greet", "goodbye", "deny", "isbot"]:
        reply = chitchat_bot(user_intent)
        print(reply)
        return reply
    elif user_intent== "accept":
        # 若是第一轮对话接收到accept的闲聊意图，以查询身份回复。
        # 若是第n(n!=1)轮对话...
        reply=load_user_dialogue_context(sender)
        reply=reply.get("choice_answer")
        print(reply)
        return reply
    # Knowledge Inquiry
    else:
        reply = medical_bot(text,sender)
        return reply



if __name__=='__main__':
    """
    测试用例：
    你好
    你是机器人吗
    再见
    不是这样的
    """
    # 打开下面注释可以清楚对话日志缓存
    # delete_cache(file_name='/logs/loginInfo.pkl')

    # 打开下面对话使用swagger在网页段进行对话
    #app.run(host="127.0.0.1", port=server_port)  #ps 链接已经建立 但网址在浏览器打不开

    #仅测试函数 message()
    sender=input("请输入用户id：")
    text=input("你好，我是机器人小夏，请问你有什么问题吗：")
    answer = message(sender, text) 



#创建Flask对象app并初始化
app = Flask(__name__)


#通过python装饰器的方法定义路由地址
@app.route("/")
#定义方法 用jinjia2引擎来渲染页面，并返回一个index.html页面
def root():
    msg0 = sender
    msg1 = text
    msg2 = answer
    return render_template("index.html", id = msg0, answer = msg2, question = msg1)
    

@app.route('/data')
def data():
    return render_template('data.html')

    
@app.route('/addquestion', methods = ['POST'])
def receive():
    json_data = request.json
    print('recv:',json_data)
    return json_data

app.run(port=8080)

