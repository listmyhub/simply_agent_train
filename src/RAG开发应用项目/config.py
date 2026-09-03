#该项目的全局配置
from agent.load import DASHSCOPE_API_KEY
#API配置
DASHSCOPE_API_KEY=DASHSCOPE_API_KEY
#模型配置
EMBEDDING_MODEL="text-embedding-v4"
GENERATE_MODEL="qwen-turbo"
RERANK_MODEL="qwen3-rerank"
#路径配置
PDF_PATH="./input/ "
VECTOR_BD_PATH="./vector.db"
COLLECTION_NAME="demo001"
#分块配置
CHUNK_SIZE=600
CHUNK_OVERLAP=100
#检索配置
RETRIEVER_K=4
RERANK_TOPN=3


