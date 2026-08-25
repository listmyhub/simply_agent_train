from pydoc_data.topics import topics

from langchain_core.tools import tool
from langchain_tavily import TavilySearch

from agent.load import TAVILY_API_KEY

search_tool= TavilySearch(max_results=10,
                          topic="general")
@tool
def web_search(query: str):
    """在互联网上搜索信息

    Args:
        query:用户需要搜索的问题

    Returns:
        返回联网搜索到的信息和对应的网页地址
   """
    return search_tool.invoke({"query":query})

if "__main__" == __name__:
    # messages=search_tool.invoke({'query':"南京理工大学排名全国第几"})
    messages=web_search.invoke({"query":"南京理工大学和南京航空航天大学哪个更好"})
    print(messages['results'])
