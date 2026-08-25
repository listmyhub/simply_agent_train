from langchain.agents import create_agent
from agent.my_llm import llm
from agent.tools.继承父类工具 import mysearchagent

# def send_email(to:str,subject:str,body:str):
#     """给一个人发送邮件"""
#     email={
#         "to":to,
#         "subject":subject,
#         "body":body
#     }
#     return f"邮件已发送至{to}"
#创建一个工具
my_search_agent = mysearchagent()
agent=create_agent(
    llm,
    tools=[my_search_agent],
    system_prompt="你是智能助手，请始终使用my_search_agent来搜索信息"
)
#本地先测试一下定义的工具是否有效
if __name__=="__main__":
    print(my_search_agent.name)
    print(my_search_agent.description)
    print(my_search_agent.args)
    print(my_search_agent.args_schema.model_json_schema())
    rep=my_search_agent.invoke({"query":"帮我看一下2026年8月28号南京的天气"})
    print(rep)