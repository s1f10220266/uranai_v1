from django.conf import settings
from django.shortcuts import render
#from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.schema import  HumanMessage #, AIMessage, SystemMessage
import requests

import os


# Create your views here.
def index(request):
    # 環境変数
    openai_api_key = settings.OPENAI_API_KEY
    openai_api_base = settings.OPENAI_API_BASE
    
    chat = ChatOpenAI(
        openai_api_key=openai_api_key,
        openai_api_base=openai_api_base,
        temperature=0
    )
    
    params = {}
    
    selected = { #デフォルトで選択されている選択肢
        "q1_1": "E",
        "q1_2": "E",
        "q2_1": "S",
        "q2_2": "S",
        "q3_1": "T",
        "q3_2": "T",
        "q4_1": "P",
        "q4_2": "P",
    }
    
    result_user_mbti = ""
    #mbti診断
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "scenario_gen":
            #ユーザの解答結果を得る
            q11_ans = request.POST.get("q1-1", "E")
            q12_ans = request.POST.get("q1-2", "E")
            q21_ans = request.POST.get("q2-1", "S")
            q22_ans = request.POST.get("q2-2", "S")
            q31_ans = request.POST.get("q3-1", "T")
            q32_ans = request.POST.get("q3-2", "T")
            q41_ans = request.POST.get("q4-1", "P")
            q42_ans = request.POST.get("q4-2", "P")
            
            #ラジオボタンの選択を保存
            selected["q1_1"] = q11_ans
            selected["q1_2"] = q12_ans
            selected["q2_1"] = q21_ans
            selected["q2_2"] = q22_ans
            selected["q3_1"] = q31_ans
            selected["q3_2"] = q32_ans
            selected["q4_1"] = q41_ans
            selected["q4_2"] = q42_ans
            
        
            #アルファベットを01の数値に変換
            q11 = 1 if q11_ans == 'E' else 0
            q12 = 1 if q12_ans == 'E' else 0
            q21 = 1 if q21_ans == 'S' else 0
            q22 = 1 if q22_ans == 'S' else 0
            q31 = 1 if q31_ans == 'T' else 0
            q32 = 1 if q32_ans == 'T' else 0
            q41 = 1 if q41_ans == 'P' else 0
            q42 = 1 if q42_ans == 'P' else 0

        
            tmp_user_mbti = 0 #MBTIの結果
        
            if ((q11 & q12) != 0):
                tmp_user_mbti |= (1<<3)
            if ((q21 & q22) != 0):
                tmp_user_mbti |= (1<<2)
            if ((q31 & q32) != 0):
                tmp_user_mbti |= (1<<1)
            if ((q41 & q42) != 0):
                tmp_user_mbti |= (1<<0)
                
            print("debag: ", bin(tmp_user_mbti))

            #結果からmbtiを診断する
            for i in range(3, -1, -1):
                if (i == 3):
                    if ((tmp_user_mbti) & (1<<i) != 0):
                        result_user_mbti += "E"
                    else:
                        result_user_mbti += "I"
                elif (i == 2):
                    if ((tmp_user_mbti) & (1<<i) != 0):
                        result_user_mbti += "S"
                    else:
                        result_user_mbti += "N"
                elif (i == 1):
                    if ((tmp_user_mbti) & (1<<i) != 0):
                        result_user_mbti += "T"
                    else:
                        result_user_mbti += "F"
                elif (i == 0):
                    if ((tmp_user_mbti) & (1<<i) != 0):
                        result_user_mbti += "P"
                    else:
                        result_user_mbti += "J"
                    
            user_type = ""
            if (result_user_mbti == "INTJ"):
                user_type = "建築家"
            elif (result_user_mbti == "INTP"):
                user_type = "論理学者"
            elif (result_user_mbti == "ENTJ"):
                user_type = "指揮官"
            elif (result_user_mbti == "ENTP"):
                user_type = "討論者"
            elif (result_user_mbti == "INFJ"):
                user_type = "提唱者"
            elif (result_user_mbti == "INFP"):
                user_type = "仲介者"
            elif (result_user_mbti == "ENFJ"):
                user_type = "主人公"
            elif (result_user_mbti == "ENFP"):
                user_type = "運動家"
            elif (result_user_mbti == "ISTJ"):
                user_type = "管理者"
            elif (result_user_mbti == "ISFJ"):
                user_type = "擁護者"
            elif (result_user_mbti == "ESTJ"):
                user_type = "幹部"
            elif (result_user_mbti == "ESFJ"):
                user_type = "領事"
            elif (result_user_mbti == "ISTP"):
                user_type = "巨匠"
            elif (result_user_mbti == "ISFP"):
                user_type = "冒険家"
            elif (result_user_mbti == "ESTP"):
                user_type = "起業家"
            elif (result_user_mbti == "ESFP"):
                user_type = "エンターテイナー"
            
            params["user_mbti"] = result_user_mbti
            params["user_type"] = user_type
            user_job = request.POST.get("user_job")    
            message = [HumanMessage(content=f"ユーザのmbtiは{result_user_mbti}だそうです。そんな性格のユーザは将来{user_job}になりたいと思っています。ユーザが将来{user_job}に就いた際のシナリオを作成してください。")]
            result = chat(message)
            params["user_scenario"] = result.content
            
    return render(request, 'scenario/top_page.html', params)
