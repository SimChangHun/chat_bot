### 로컬 한글 출력용 ###
import sys
import io
import random
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
########################

## slacker import #####
# from slacker import Slacker
#
# slack = Slacker('<>')
#######################
import json
import os
import re
import urllib.request

from urllib import parse #인코딩용 임포트

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

slack_token = "<>"
slack_client_id = "<>"
slack_client_secret = "<>"
slack_verification = "<>"
sc = SlackClient(slack_token)

# def pre_answer():
#     keywords = ["잠시만요."]
#     return u'\n'.join(keywords)

def _crawl_word_keywords(text):
    # URL 데이터를 가져올 사이트 url 입력
    #slack.chat.post_message('#general', 'testing sorry')
    #en_lan = '가'.encode('utf-8')
    #print(en_lan) #\xea\xb0\x80 ->%ea%b0%80
    #url = "https://www.wordrow.kr/%EC%8B%9C%EC%9E%91%ED%95%98%EB%8A%94-%EB%A7%90/%EA%B0%80/%EC%84%B8%20%EA%B8%80%EC%9E%90"
    ##임시변수##

    ###########

    keywords = []
    if "싸피" in text:
        keywords.append("아 싸피! 삼성이 만든 최고의 SW프로그래머 양성 프로그램이죠!\n\n\n\n\n\n\n라고 말하면 되나요?")
    elif "넌" and "누구야" in text:
        keywords.append("전 끝말잇기봇 동생이에요. 정해진 대답밖에 못해요!")
    elif "안녕" in text:
        keywords.append("안녕하세요?")
    elif "두둠칫" in text:
        keywords.append("⊂_? \n　 ＼＼  Λ＿Λ \n　　＼ (  ' ㅅ '  )  두둠칫\n"\
                ">　⌒? \n　　　/ 　 へ＼\n　　 /　　/　＼＼ \n　　 ?　ノ　　 ?_つ \n"\
                "　　/　/ 두둠칫 \n　 /　/| \n　(　(? \n　|　|、＼ \n　| ? ＼ ⌒) \n　| |　　) / \n(`ノ\n")
    elif "sigh" in text:
        keywords.append("............................................________\n"\
        "....................................,.-'\"...................``~., \n"\
        ".............................,.-\"...................................\"-., \n"\
        ".........................,/...............................................\":,\n"\
        ".....................,?......................................................,\n"\
        ".................../...........................................................,} \n"\
        "................./......................................................,:\'^`..} \n"\
        ".............../...................................................,:\"........./ \n"\
        "..............?.....__.........................................:`.........../ \n"\
        "............./__.(.....\"~-,_..............................,:`........../ \n"\
        ".........../(_....\"-,_........\"~,_..........................,:`..........._/ \n"\
        "..........{.._$;_......\"=,_.......\"-,_.............,.---,},.~\";/.......}\n"\
        "...........((.....*~_.......\"=-._......\";,,./`..../\"............../ \n"\
        "...,,,___.\'~,......\"~.,....................`.....}............../ \n"\
        "............(....\'=-,,.......`........................(......;_,,-\" \n"\
        "............/.\'~,......`-...................................../ \n"\
        ".............`~.*-,.....................................|,./.....,__ \n"\
        ",,_..........}.>-._...................................|..............`=~-, \n"\
        ".....\'=~-,__......`,................................. \n"\
        "...................`=~-,,.,............................... \n"\
        "................................\':,,...........................`..............__ \n"\
        ".....................................\'=-,...................,%\'>--==\'` \n"\
        "........................................_..........._,-%.......` \n"\
        "...................................,  ")
    else:
        keywords.append("제가 모르는 문장이네요(´・ω・`)")

    return u'\n'.join(keywords)
    '''
    keywords = []

    data_list = []

    count = 0
    s_text = text.split() #들어온 채팅을 분할
    a_word = [o_word for o_word in s_text[1]] #첫 단어를 글자로 나눔
    e_word = parse.quote(a_word[2]) #마지막 글자 e_word
    #i_word = text[0]
    #keywords.append(i_word)
    #keywords.append("hi")
    #keywords.append("{}".format(e_word))


    #글자로 시작하는 단어 모두 저장
    for i in range(1, 5):
        if count != 0 and count < 100 :
            break #마지막장이면 아웃

        count = 0 #카운트 초기화
        #백과사전 가서 마지막글자 e_world로 시작하는거 검색
        url = "https://www.wordrow.kr/%EC%8B%9C%EC%9E%91%ED%95%98%EB%8A%94-%EB%A7%90/" + e_word +"/%EC%84%B8%20%EA%B8%80%EC%9E%90?%EC%AA%BD="+str(i)
        soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

        w_table = soup.find("div", class_="table")
        if w_table.find("span", class_="h4 text-warning"):#지면
            keywords.append("제가 졌어요ㅠㅠ")
            return u'\n'.join(keywords)

        for datas in w_table.find_all("h3", class_="card-caption"):
            for word_des in datas.find_all("a"):
                data_list.append(word_des.get_text().strip())
                count += 1


    ran_num = random.randrange(1,len(data_list)) #랜덤숫자 정함
    keywords.append("{} 쿵쿵따!".format(data_list[ran_num])) #랜덤단어 출력

    return u'\n'.join(keywords)
    '''

# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        # sc.api_call(
        #     "chat.postMessage",
        #     channel=channel,
        #     text="기다려주세요"
        # )

        keywords = _crawl_word_keywords(text)
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=keywords
        )

        return make_response("App mention message has been sent", 200,)

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})

@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                            })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000)
