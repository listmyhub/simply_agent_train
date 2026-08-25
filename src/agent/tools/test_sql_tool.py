import unittest
from typing import Any, List, Optional
from urllib.parse import quote_plus

from langchain_core.tools import BaseTool
from pydantic import create_model,Field
from pydantic.v1.schema import schema

from agent.sqr.log日志 import log
from agent.sqr.sqr_function import mysqrdatabase


class ListSqlTool(BaseTool):
    """列出sql的表名和描述信息工具"""
    name:str="test_sql_tool"
    description:str="理解人类语言，从sql中获取tables 的描述和表名等信息"
    db_manager:mysqrdatabase

    def _run(self)->str:
        try:
            schemas=self.db_manager.get_tables_comments()
            result=f"这个数据库一共有{len(schemas)}个table:\n\n"
            for i,schema in enumerate(schemas):
                name=schema['table_name']
                comments=schema['table_comment']

                if comments.isspace() or not comments:
                    comments_display="暂时没有描述"
                else:
                    comments_display=comments
                result+=f"{i+1}. 表名:{name}\n\n"
                result+=f"   描述:{comments_display}\n\n"
            return result
        except Exception as e:
            log.exception(e)
            raise ValueError(f"eero:{e}")
    async def _arun(self)->str:
        return self._run()
class schemassqltool(BaseTool):
    """测试sql 的模式工具"""
    name:str="schemas_sql_tool"
    description:str = "输出数据库指定表名的模式,包括定义，主键和外键，输入表名列表，以获取对应的模式信息"
    db_manager:mysqrdatabase
    def __init__(self,**kwargs)->None:
        super().__init__(**kwargs)
        # self.db_manager=db_manager
        self.args_schema=create_model("schemassqltoolargs",table_names=(Optional[List[str]],Field(...,description="输入指定的表名列表，以获取信息")))
    def _run(self,table_names:Optional[List[str]]=None)->str:
        try:
            table_schema=self.db_manager.get_table_schema(table_names)
            return table_schema if table_schema else "未查询到该表"
        except Exception as e:
            log.exception(e)
            raise ValueError(f"erro:{e}")
    async  def _arun(self,table_names:Optional[List[str]]=None)->str:
        return self._run()
class excutesqltool(BaseTool):
    """查询并执行sql语句"""
    name:str="excute_sql_tool"
    description:str = "输出执行sql语句后的结果，输入是需要是标准的select语句"
    db_manager:mysqrdatabase
    def __init__(self,**kwargs)->None:
        super().__init__(**kwargs)
        # self.db_manager=db_manager
        self.args_schema=create_model("excute_sql_toolargs",query=(str,Field(...,description="输入需要执行的标准的SELECT语句")))
    def _run(self,query:str)->str:
        try:
            result=self.db_manager.excute_query(query=query)
            return result if result else "执行结果为空"
        except Exception as e:
            log.exception(e)
            raise ValueError(f"erro:{e}")
    async def _arun(self,query:str)->str:
        return self._run(query)
class sqlchecktool(BaseTool):
    """检查sql语句有效性的工具"""
    name:str="sqlchecktool"
    description:str = "对sql语句进行检查，检查他的有效性"
    db_manager:mysqrdatabase
    def __init__(self,**kwargs)->None:
        super().__init__(**kwargs)
        # self.db_manager=db_manager
        self.args_schema=create_model("sqlchecktooargs",query=(str,Field(...,description="需要检查的sql语句")))

    def _run(self,query:str)->str:
        try:
            result=self.db_manager.validate_query(query=query)
            return result if result else "查询失败"
        except Exception as e:
            log.exception(e)
            raise ValueError(f"erro:{e}")
    async def _arun(self,query:str)->str:
        return self._run(query)

if __name__ == '__main__':
    user = "root"
    host = "127.0.0.1"
    password = "Fan760821@"
    database = "world"
    port = 3306
    safe_pwd =quote_plus(password)
    manager = mysqrdatabase(f"mysql+pymysql://{user}:{safe_pwd}@{host}:{port}/{database}")
    # name=manager.get_sqlname()
    # tool=ListSqlTool(db_manager=manager)
    # print(tool.invoke({}))
    # tool =schemassqltool(db_manager=manager)
    # print(tool.invoke({"table_names":["city","country"]}))
    # tool = excutesqltool(db_manager=manager)
    # print(tool.invoke({"query":'select * from city'}))
    tool = sqlchecktool(db_manager=manager)
    print(tool.invoke({"query": 'select * from city'}))




