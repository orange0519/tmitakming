import threading
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from linebot.exceptions import LineBotApiError

import os
app = Flask(__name__)


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import time
import datetime
import schedule
#時間偏移+8hour
a = datetime.datetime.today()
o = datetime.timedelta(hours=8)
#print((a+o).strftime("%Y-%m-%d_%H:%M"))
# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('serviceAccount.json')

# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)
db = firestore.client()
def query_Get():
    # 初始化firestore
    
    #Get Collection
    doc_ref = db.collection('Detector').document('gas')
    localtime = time.asctime(time.localtime(time.time()))
    temp = '監測時間 => '+ localtime + '\n' 
    try:
        doc = doc_ref.get()
        # 透過 to_dict()將文件轉為dictionary
        temp +=  'PM2.5 => {}'.format(doc.to_dict()['PM2.5']) + '\n' + '二氧化碳 => {}'.format(doc.to_dict()['CO2']) + '\n' + '酒精 => {}'.format(doc.to_dict()['Ethanol']) + '\n' + '一氧化碳 => {}'.format(doc.to_dict()['CO']) + '\n'
        # print("文件內容為：{}".format(doc.to_dict()))
        # print(temp)
    except:
        print("指定文件的路徑{}不存在，請檢查路徑是否正確".format(path))
        # print(temp)

#def query_insert():
    




# Channel Access Token
line_bot_api = LineBotApi( 'MIgVrNiPJz5nNBDgMYE7/pmAl8fR2kue2oyLonZowuDtFVC2LNe/U0LNJ73GolHxMVfv2g0uj5pQJcNZOPKwOSJ7rQ133IeKj3Cn2ZGYJ6HG6Yb3OkmtSgfdI0fomqs7YoqOILlBcYy53AXWLxixcAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('8c54ffae7c41efd0d30013d1e13f7a1a')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

#字串匹配 用來是否呼叫沫兒的
import re
MoReply = False  #沫兒未確認匹配不回覆訊息

to = "U59f95fe4a4acf87b3433b626f41679b8" #userID 推播用


def job():
    a = datetime.datetime.today()
    o = datetime.timedelta(hours=8)
  #  if int((a+o).strftime("%M")) == 0:
  #  line_bot_api.push_message('Cd28e03928239ba4bfb9ba96f758861d4', TextSendMessage(
  #      text="報時~ 現在時間："+(a+o).strftime("%Y-%m-%d %H:%M:%S")))
    line_bot_api.push_message('C18d381b48c034f3de0af914fe1fe524f', TextSendMessage(text="報時~ 現在時間："+(a+o).strftime("%Y-%m-%d %H:%M:%S")))
    timer = threading.Timer(60, job)
    timer.start()




# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

      
    if re.match('沫兒',event.message.text):
        MoReply = True #沫兒確認匹配成功
    message = TextSendMessage(text='沫兒收到您的回覆囉!')
    if re.search('我帥嗎',event.message.text):
        message = TextSendMessage(text='沫兒覺得勝舢最帥了!')
    if re.search('回報車內狀況',event.message.text):
        message = TextSendMessage(text=temp)
    # message = TextSendMessage(text=event.message.text)
    if re.search('profile_user',event.message.text):
        user_id = event.source.user_id
        message = TextSendMessage(text=user_id)
    if re.search('profile_group', event.message.text):
        group_id = event.source.group_id
        message = TextSendMessage(text=group_id)
    if re.search('profile_room', event.message.text):
        room_id = event.source.room_id
        message = TextSendMessage(text=room_id)
    if re.search('測試推播',event.message.text):
        
        line_bot_api.push_message('C18d381b48c034f3de0af914fe1fe524f', TextSendMessage(text=(a+o).strftime("%Y-%m-%d %H:%M:%S")))
  
    if MoReply == True:
        line_bot_api.reply_message(event.reply_token, message)
    









if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    timer = threading.Timer(60, job)
    timer.start()
    job()
