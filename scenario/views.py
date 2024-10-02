from django.conf import settings
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone
from scenario.models import Scenario
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain
from langchain.document_loaders import PyPDFLoader 
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import requests

import os


# Create your views here.
def title(request):
    return render(request, "scenario/title.html")

def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])

def index(request):
    # 環境変数
    openai_api_key = settings.OPENAI_API_KEY
    openai_api_base = settings.OPENAI_API_BASE
    
    # ChatOpenAIクラスのインスタンスを作成
    llm = ChatOpenAI(
        openai_api_key=openai_api_key,
        openai_api_base=openai_api_base,
        model_name="gpt-4o-mini",
        temperature=0
    )
    
    # OpenAI埋め込みモデルのインスタンスを作成
    embeddings_model = OpenAIEmbeddings(
        openai_api_base=openai_api_base
    )
    
    # テキストを読み込み、猫語を学習
    loader = TextLoader("scenario/learn_16personalities.txt")
    text = "\n".join([pages.page_content for pages in loader.load()])
    
    # テキストをチャンクに分割
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=20,
        length_function=len,
        add_start_index=True
    )
    documents = text_splitter.create_documents([text])

    # ベクトル化してChromaDBに保存
    db = Chroma.from_documents(documents, embeddings_model)
    retriever = db.as_retriever(search_kwargs={"k": 3})
    
    params = {} #テンプレートに渡すデータ
    
    #mbti診断
    user_mbti = "" #mbtiの診断結果を格納していく
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
                
            user_type = "" #MBTIから役職を算出
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
            # シナリオ生成処理
            user_job = request.POST.get("user_job")
            user_mbti = request.POST.get("user_mbti", "")
            user_type = request.POST.get("user_type", "")
            
            template = """
                あなたは猫の占い師です。
                あなたはユーザの性格を表すMBTIとユーザが将来なりたい職業が与えられます。
                ユーザが将来、その職業についた際のシナリオを作成してください。
                シナリオは以下のコンテンツを含めてください。
                1. ユーザはその仕事に向いているか
                2. ユーザがその仕事に就いた際にうまくいくこと、苦労すること
                3. ユーザがその仕事に就いた際の、起床から就寝までの1日のスケジュール
                4. 最後に、あなたが占い師としてユーザに伝えたいこと
                なお、シナリオは上記の1. ~ 4.について、1.、2.、3.、4.から始めてください。
                また、ユーザのことは"キミ"として、語尾は猫のように"ニャン"としてください。
                
                以下のcontextには、MBTIの詳細な情報が含まれていますので、必要であれば参考にしてください。
                {context}
                
                ユーザ: {question}
            """
            prompt = ChatPromptTemplate.from_template(template)
            chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser(verbose=True)
            )
            
            input = f"ユーザのmbtiは{user_mbti}だそうです。そんな性格のユーザは将来{user_job}になりたいと思っています。ユーザが将来{user_job}に就いた際のシナリオを作成してください。"
            output_by_retriever = chain.invoke(input)

            # 結果を保存
            params["user_mbti"] = user_mbti
            params["user_type"] = user_type
            params["user_scenario"] = output_by_retriever
            params["precaution"] = "#キャラ名#さんは気まぐれです。占い結果に当たり外れがあります。あくまで参考程度にお読みください。"
            
            user_data = Scenario(job=user_job, mbti=user_mbti, scenario=str(output_by_retriever))
            user_data.save()
            return redirect('output', scenario_id=user_data.id)
    
    params["scenarios"] = Scenario.objects.all()
    return render(request, 'scenario/main_page.html', params)

def result(request, scenario_id):
    try:
        scenario = Scenario.objects.get(pk=scenario_id)
    except Scenario.DoesNotExist:
        raise Http404("Scenario does not exist")
    context = {
        'scenario_data': scenario
    }
    return render(request, "scenario/scenario.html", context)