from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from agent.my_llm import llm

#创建提示词模板（单轮提示词模板）
# prompt_template=ChatPromptTemplate.from_template(
#     "尽你可能回答我的问题."
#     "你的输出格式必须是包含'movies_name','year','director','rate'为键的JSON对象"
#     "{question}")
# chain=prompt_template|llm|SimpleJsonOutputParser()
# rep=chain.invoke({"question":"介绍一下大话西游"})
# print(rep)
#创建多轮提示词模板
prompt=ChatPromptTemplate.from_messages(
    [("system","你是智能语音助手，请用简洁的语言回答问题，"),
     MessagesPlaceholder(
         "chat_history"),
     ("human","{question}"),
     ]
)
#构造一条链
chain=prompt|llm
#维护好历史对话
chat_history=[]
rep=chain.invoke({"chat_history":chat_history,"question":"大话西游的导演是谁"})
print(rep)
chat_history.append(AIMessage(content=rep.content))
chat_history.append(HumanMessage(content="大话西游的导演是谁"))
#带上历史进行第二轮回答
rep1=chain.invoke({"chat_history":chat_history,"question":"大话西游的导演今年多少岁"})
print(rep1.content)
