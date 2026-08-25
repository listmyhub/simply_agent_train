from langchain_community.chat_models import ChatZhipuAI
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from zhipuai import ZhipuAI

from agent.load import DEEPSEEK_API_KEY, ZHIPU_API_KEY, ALIBL_BSUL, ALIBL_API_KEY
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_core.prompts import ChatPromptTemplate
# llm=init_chat_model(
#     model="deepseek-chat",
#     model_provider="openai",
#     api_key=DEEPSEEK_API_KEY,
#     base_url="https://api.deepseek.com/v1/",
#     temperature=0.7,
#     max_tokens=2048
# )
# res=llm.invoke("简单介绍一下langchain1.0")
# print(res)
# llm=ChatOpenAI(
#     model="deepseek-chat",
#     api_key=DEEPSEEK_API_KEY,
#     base_url="https://api.deepseek.com/v1",
#     temperature=0.7
# # )
# llm=ChatDeepSeek(
#     model="deepseek-chat",
#     api_key=DEEPSEEK_API_KEY,
#     # base_url="https://api.deepseek.com/v1",
#     temperature=0.7
# )
#res=llm.invoke("hello deepseek")
# print(res)


# llm = ChatOpenAI(
#     model="deepseek-v4-pro",
#     temperature=0.7,
#     api_key=DEEPSEEK_API_KEY,
#     base_url="https://api.deepseek.com")
# # )
#zhipuai模型的调用
# llm=ZhipuAI(api_key=ZHIPU_API_KEY)
#利用langchain来调用zhipuai
# llm=ChatZhipuAI(api_key=ZHIPU_API_KEY,
#                 model="glm-4.6v-flash",
#                 temperature=0.5)
# Qwen模型的调用
llm=ChatOpenAI(
    model="qwen3.5-plus",
    temperature=0.7,
    api_key=ALIBL_API_KEY,
    base_url=ALIBL_BSUL
)