
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, create_model
from agent.my_llm import  llm
from typing import Type

# class searches(BaseModel):
#     query:str=Field(...,description="需要搜索的信息")


class mysearchagent(BaseTool):
    name:str="mysearchagent"
    description:str="进行联网搜索的工具"
    # 第一种方式
    # args_schema:Type[BaseModel]= searches
    #第二种方式
    def __init__(self):
        super().__init__()
        self.args_schema=create_model("searches",query=(str,Field(...,description="需要搜索的信息")))
    def _run(self,query:str)->str:
        try:
            response = llm.web_search.web_search(
                search_engine="search_pro",
                search_query=query)
            if response.search_result:
                return "/n/n".join([d.content for d in response.search_result])
            else:
                return "没有搜索到任何结果"
        except Exception as e:
            print(e)
            return f"error:{e}"
