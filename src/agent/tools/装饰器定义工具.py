from langchain_core.tools import tool
from pydantic import tools, BaseModel, Field
from agent.load import ZHIPU_API_KEY

#定义工具的第一种方法Goolge
# @tool("my_search_agent",parse_docstring=True)
# def my_search_agent(query:str)->str:
#     """联网搜索所有公开的信息。
#
#     Args:
#         query : 需要上网搜索的信息。
#
#     Returns:
#         返回搜索的结果。
#     """
#第二种方法
class searches(BaseModel):
    query:str =Field(...,description="需要联网搜索的信息")
@tool("my_agent",args_schema=searches,description="在互联网上搜索相关的信息的工具")
def my_search_agent(query):
    try:
        response=llm.web_search.web_search(
        search_engine="search_pro",
        search_query=query)
        if response.search_result:
            return "/n/n".join([d.content for d in response.search_result])
        else:
            return "没有搜索到任何结果"
    except Exception as e:
        print(e)
        return f"error:{e}"