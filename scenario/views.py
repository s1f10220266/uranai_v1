from django.conf import settings
from django.shortcuts import render
from langchain.agents import Tool, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import requests

import os


# Create your views here.
def index(request):
    params = {}
    
    # 環境変数
    openai_api_key = settings.OPENAI_API_KEY
    openai_api_base = settings.OPENAI_API_BASE
    
    chat = ChatOpenAI(
        openai_api_key=openai_api_key,
        openai_api_base=openai_api_base,
        temperature=0
    )
    
    if request.method == 'POST':
        user_job = request.POST.get('job')
        user_mbti = request.POST.get('mbti')
        message = [HumanMessage(content=f"ユーザのmbtiは{user_mbti}だそうです。そんな性格のユーザは将来{user_job}になりたいと思っています。ユーザが将来{user_job}に就いた際のシナリオを作成してください。")]
        
        result = chat(message)
        params['user_scenario'] = result.content
    return render(request, 'scenario/top_page.html', params)
