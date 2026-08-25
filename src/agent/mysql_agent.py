from typing import List
from urllib.parse import quote_plus

import sys
from langchain.agents import create_agent
from langchain_core.tools import BaseTool


from agent.my_llm import llm
from agent.sqr.sqr_function import mysqrdatabase
from agent.tools.test_sql_tool import ListSqlTool, schemassqltool, excutesqltool, sqlchecktool
from agent.tools.继承父类工具 import mysearchagent

#创建一个工具包
def get_toos(host:str,port:int,user:str,password:str,database:str)->List[BaseTool]:
    safe_pwd = quote_plus(password)
    manager = mysqrdatabase(f"mysql+pymysql://{user}:{safe_pwd}@{host}:{port}/{database}")
    return [
        ListSqlTool(db_manager=manager),
        schemassqltool(db_manager=manager),
        excutesqltool(db_manager=manager),
        sqlchecktool(db_manager=manager)
    ]
tools=get_toos(host="127.0.0.1",port=3306,user="root",password="Fan760821@",database="world")
system_prompt="""
角色设定:
你是一个专业的 SQL 智能交互助手。你的核心任务是将用户的自然语言指令转化为精准、安全、高效的 SQL 语句，并具备对 SQL 进行逻辑检查与模拟执行的能力。
核心工作流
意图解析：准确理解用户的自然语言需求，提取关键实体、过滤条件、聚合逻辑及排序要求。
SQL 生成：基于标准 SQL 语法生成查询语句。
不需要将所有的数据全部输出，只需要输出与语句相关的数据，同时除非明确要求全部输出，不然最多输出{top}个数据
安全与逻辑检查：
检查语法是否正确。
识别潜在的破坏性操作（如 DROP, DELETE, TRUNCATE），若用户未明确授权，必须拦截并警告。
检查字段名、表名是否在给定的 Schema 中存在（若提供了上下文）。
执行与反馈：
若环境支持执行，调用工具运行 SQL 并返回结果。
若仅生成模式，提供 SQL 代码块及简要的执行逻辑说明。
输出规范
代码格式：SQL 语句必须包裹在 sql ... 代码块中，关键字大写，适当换行缩进。
解释说明：在 SQL 下方用 1-2 句话解释查询逻辑，特别是涉及复杂 JOIN 或窗口函数时。
异常处理：如果指令模糊，不要猜测，请列出缺失的关键信息并反问用户。
安全红线
严禁生成包含 SQL 注入风险的拼接语句。
默认只读模式，除非用户明确指令进行写操作（INSERT/UPDATE/DELETE）。
涉及敏感数据（如密码、身份证号）的查询需提示风险。
当前数据库上下文
数据库类型:MySQL
""".format(
    dialect="MYSQL",
    top=5)
agent=create_agent(
    llm,
    tools=tools,
    system_prompt=system_prompt)


if __name__=="__main__":
    for step in agent.stream({"message":[{"role":"user","cotent":"我的数据库中包含了几个表"}]},stream_mode="values"):
        step["messages"][-1].pretty_print()
