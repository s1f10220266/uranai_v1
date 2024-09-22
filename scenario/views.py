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
    
    params = {} #htmlに渡すデータ
    
    user_mbti = ""
    #mbti診断
    if request.method == "POST":    
        if request.POST.get("action") == "mbti_gen":
            question_names = { #クイズの回答
                'e_or_i_0': 0, 'e_or_i_1': 0, 'e_or_i_2': 0, 'e_or_i_3': 0,
                's_or_n_0': 0, 's_or_n_1': 0, 's_or_n_2': 0, 's_or_n_3': 0,
                't_or_f_0': 0, 't_or_f_1': 0, 't_or_f_2': 0, 't_or_f_3': 0,
                'p_or_j_0': 0, 'p_or_j_1': 0, 'p_or_j_2': 0, 'p_or_j_3': 0
            }
            result_e_or_i = 0
            result_s_or_n = 0
            result_t_or_f = 0
            result_p_or_j = 0
            for n in list(question_names): #辞書型のquestion_namesからキーだけ取得
                question_names[n] = int(request.POST.get(n, 0))
            for eval in list(question_names):
                if eval.startswith('e'):
                    result_e_or_i += question_names[eval]
                elif eval.startswith('s'):
                    result_s_or_n += question_names[eval]
                elif eval.startswith('t'):
                    result_t_or_f += question_names[eval]
                else:
                    result_p_or_j += question_names[eval]
                    
            if result_e_or_i >= 0:
                user_mbti += 'E'
            else:
                user_mbti += 'I'
                
            if result_s_or_n >= 0:
                user_mbti += 'S'
            else:
                user_mbti += 'N'
                
            if result_t_or_f >= 0:
                user_mbti += 'T'
            else:
                user_mbti += 'F'
                
            if result_p_or_j >= 0:
                user_mbti += 'P'
            else:
                user_mbti += 'J'
                
            user_type = ""
            if (user_mbti == "INTJ"):
                user_type = "建築家"
            elif (user_mbti == "INTP"):
                user_type = "論理学者"
            elif (user_mbti == "ENTJ"):
                user_type = "指揮官"
            elif (user_mbti == "ENTP"):
                user_type = "討論者"
            elif (user_mbti == "INFJ"):
                user_type = "提唱者"
            elif (user_mbti == "INFP"):
                user_type = "仲介者"
            elif (user_mbti == "ENFJ"):
                user_type = "主人公"
            elif (user_mbti == "ENFP"):
                user_type = "運動家"
            elif (user_mbti == "ISTJ"):
                user_type = "管理者"
            elif (user_mbti == "ISFJ"):
                user_type = "擁護者"
            elif (user_mbti == "ESTJ"):
                user_type = "幹部"
            elif (user_mbti == "ESFJ"):
                user_type = "領事"
            elif (user_mbti == "ISTP"):
                user_type = "巨匠"
            elif (user_mbti == "ISFP"):
                user_type = "冒険家"
            elif (user_mbti == "ESTP"):
                user_type = "起業家"
            elif (user_mbti == "ESFP"):
                user_type = "エンターテイナー"
        
            params["user_mbti"] = user_mbti
            params["user_type"] = user_type
        if request.POST.get("action") == "scenario_gen":
            user_job = request.POST.get("user_job")
            intro = [HumanMessage(content="""
            あなたは占い師です。 
            ユーザが自身の性格を意味するMBTIと将来なりたい職業をあなたに相談します。
            それらの情報からユーザが将来その職業に就いたときどうなるのか占い、そのシナリオを作成してください。
            シナリオは以下の内容を含み、ユーザにとってためになるものであり、読みやすくまとめられていて、読んでいて面白いものにしてください。
            1. ユーザはその仕事に向いているのかどうか
            2. ユーザがその仕事に就いた時うまくいくこと、苦労すること
            3. ユーザがその仕事についた時、どのようなスケジュールの一日を過ごすか、出勤時間~退勤時間、残されたプライベートの時間
            4. 最後に、あなたが占い師としてユーザに伝えたいこと
            """)]
            user_mbti = request.POST.get("user_mbti", "")
            user_type = request.POST.get("user_type", "")
            params["user_mbti"] = user_mbti
            params["user_type"] = user_type
            
            message = [HumanMessage(content=f"ユーザのmbtiは{user_mbti}だそうです。そんな性格のユーザは将来{user_job}になりたいと思っています。ユーザが将来{user_job}に就いた際のシナリオを作成してください。")]
            result = chat(intro + message)
            arranged_result = (result.content).replace("。", "。\n")
            params["user_scenario"] = arranged_result
            params["precaution"] = "#キャラ名#さんは気まぐれです。占い結果に当たり外れがあります。あくまで参考程度にお読みください。"
        
    return render(request, 'scenario/top_page.html', params)
