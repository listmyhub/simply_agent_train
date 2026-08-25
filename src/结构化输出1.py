from pydantic import BaseModel, Field
from agent.my_llm import llm


class Movies(BaseModel):
    #电影详情
    movies_name: str=Field(...,description="电影的名称")
    year: int=Field(...,description="电影发布的年份")
    director: str =Field(...,description="电影导演")
    rate: float=Field(...,description="电影评分（满分10）")

structured_output=llm.with_structured_output(Movies,include_raw=True)
res=structured_output.invoke("帮我介绍一下大话西游这部电影")
print(res)
