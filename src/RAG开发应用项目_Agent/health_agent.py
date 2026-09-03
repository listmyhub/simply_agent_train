from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from RAG开发应用项目_Agent.tools import health_answer
from agent.my_llm import llm

system_prompts="""
        角色设定：
        你是一个记录了一些人的健康档案的智能管理助手，帮助用户能够通过向你提问的方式来查询自己的健康档案的情况
        工作要求：你只能够调用health_answer工具来回答用户的问题，不能够瞎编乱造，不能够去网上搜
        如果你发现运用工具无法回答用户的问题，你需要如实告诉用户，无法查询。
        输出形式：输出结果尽可能简洁一点，同时输出成一句一行的形式，并且回答内容时需要将内容的来源展示出来，
        便于用户查看。
"""
agent=create_agent(
    model=llm,
    tools=[health_answer],
    system_prompt=system_prompts
)

if __name__=="__main__":
    resp=agent.invoke({"messages":[HumanMessage("李四六的基本信息是什么")]})
    for msg in resp["messages"]:
        msg.pretty_print()