import sqlite3
from urllib.parse import quote_plus

from langgraph.checkpoint.mysql.pymysql import PyMySQLSaver
from langgraph.checkpoint.sqlite import SqliteSaver

# user="root"
# host="127.0.0.1"
# password= "Fan760821@"
# database= "langchain_memory"
# port=3306
# safe_pwd=quote_plus(password)
# with PyMySQLSaver.from_conn_string(f"mysql+pymysql://{user}:{safe_pwd}@{host}:{port}/{database}") as checkponiter:
#
#     checkpoints=checkponiter
#连接sqlite
connection=sqlite3.connect("./resource/memory_db.db",check_same_thread=False)
#初始化checkpoint
checkpointer=SqliteSaver(connection)
#自动建表
checkpointer.setup()