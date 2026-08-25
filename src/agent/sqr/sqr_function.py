import json
from typing import Optional, List
from urllib.parse import quote_plus

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.dialects.mysql import mysqldb

from agent.sqr.log日志 import log


class mysqrdatabase:
    def __init__(self,connection_string):
        """
        连接字符串
       格式为 mysql+pymysql://user:password@host:port/database
        """
        self.engine=create_engine(connection_string,pool_size=5,pool_recycle=3600)

    def get_sqlname(self)->list[str]:
        try:
            inspector=inspect(self.engine)
            return inspector.get_table_names()
        except Exception as e:
            log.exception(e)
            raise ValueError(f"error:{str(e)}")
    def get_tables_comments(self)->list[dict]:
        """
        获取表中的名称和描述信息，

        Returns:
            List[dict]:一个字典列表，里面包含"table_name"和“table_comments"
        """
        try:
            #构建查询语句
            query=text("""
                       SELECT TABLE_NAME,TABLE_COMMENT
                       FROM INFORMATION_SCHEMA.TABLES
                       WHERE tABLE_SCHEMA=DATABASE()
                        AND TABLE_TYPE = 'BASE TABLE'
                        ORDER BY TABLE_NAME
                        """)
            with self.engine.connect() as connection:
                result=connection.execute(query)
                #将结果转成字典列表，便于后续处理
                table_info=[{'table_name':row[0],'table_comment':row[1]} for row in result]
                return table_info
        except Exception as e:
            log.exception(e)
            raise ValueError(f"error:{str(e)}")


    def get_table_schema(self,table_names:Optional[List[str]]=None)->list:
        """
        获取指定表的模式信息

        Args:
            table_names:表名列表，如果为空则为None

        """
        try:
            inspector=inspect(self.engine)
            table_info=""
            tanle_to_process=table_names if table_names else self.get_sqlname()
            for table_name in tanle_to_process:
                #获取表的结构信息
                columns=inspector.get_columns(table_name)
                #使用get_pk_constraint 替代
                pk_constraint=inspector.get_pk_constraint(table_name)
                primary_keys=pk_constraint['constrained_columns']if pk_constraint else None
                forein_keys=inspector.get_foreign_keys(table_name)
                indexs=inspector.get_indexes(table_name)

                # 构建表的描述
                table_info+=f"表名：{table_name}\n"
                table_info+="列信息：\n"
                for column in columns:
                    #检查该列是否在主键列表中
                    pk_constraint="(主键）" if column["name"] in primary_keys else " "
                    #如果字段注释，不存在就填无注释
                    comment=column.get("comment","无注释")
                    table_info+=f"-{column['name']}:{str(column['type'])}{pk_constraint}[注释：{comment}\n"
                if forein_keys:
                    table_info+="外键信息：\n"
                    for fk in forein_keys:
                        table_info+=f"-{fk['constrained_columns']}->{fk['referred_table']}.{fk['referred_columns']}\n"
                if indexs:
                    table_info+="索引信息:\n"
                    for i in indexs:
                        if not i['name'].startswith('sqlite_'):
                            table_info+=f"-{i['name']}->{i['column_names']} ({'唯一' if i['unique'] else ''})\n\n"
            return table_info
        except Exception as e:
            log.exception(e)
            raise ValueError(f"error:{str(e)}")


    def excute_query(self,query:str)->str:
        """
        执行sql查询并返回结果

        Args:
            query:SOL查询语句

        """
        #安全检查
        forbid_keywords=['insert','update','delete','drop','truncate','grant','alter','create']
        query_lower=query.lower().strip()
         #检查是否是以selct开头
        if not query_lower.startswith(('select','with')) and any(keyword in query_lower for keyword in forbid_keywords):
            raise ValueError("出于安全考虑")

        try:
            with self.engine.connect() as connection:
                result=connection.execute(text(query))
                columns=result.keys()
                rows=result.fetchmany(100)
                if not rows:
                    return "查询为空"
                #格式化结果
                result_data=[]
                for row in rows:
                    row_dict={}
                    for i,col in enumerate(columns):
                        try:
                            if row[i] is not None:
                                json.dumps(row[i])
                                row_dict[col]=row[i]
                        except Exception as e:
                            row_dict[col]=str(row[i])
                    result_data.append(row_dict)
                return json.dumps(result_data,ensure_ascii=False,indent=2)
        except Exception as e:
            log.exception(e)
            raise ValueError(f"error:{str(e)}")
    def validate_query(self,query:str)->str:
        #基本语法检查
        if not query or not query.strip():
            return "错误：查询不为空"
        #检查是否以select或with开头
        query_lower=query.lower().strip()
        if not query_lower.startswith(('select','with')):
            return "警告："
        #尝试解析查询
        try:
            with self.engine.connect() as connection:
                # pased_query=text(query)
                # complied=pased_query.compile(compile_kwargs={"literal_binds":True})
                # return "SQL 看起来正确"
                if self.engine.dialect.name=="mysql":
                    explain_query=text(f"EXPLAIN {query}")
                else:
                    explain_query=text(f"EXPLAIN {query}")
                connection.execute(explain_query)
                return "SQL 查询语法正确"
        except Exception as e:
            log.exception(e)
            # raise ValueError(f"error:{str(e)}")
            return "SQL 语法错误"




if __name__ == '__main__':
    user="root"
    host="127.0.0.1"
    password= "Fan760821@"
    database= "world"
    port=3306
    safe_pwd=quote_plus(password)
    manager=mysqrdatabase(f"mysql+pymysql://{user}:{safe_pwd}@{host}:{port}/{database}")
    manager.get_sqlname()
    print(manager.get_sqlname())
    print(manager.get_tables_comments())
    print(manager.get_table_schema(['city']))

