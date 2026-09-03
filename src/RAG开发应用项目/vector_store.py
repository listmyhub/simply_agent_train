
import os

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings

from RAG开发应用项目.config import DASHSCOPE_API_KEY, EMBEDDING_MODEL, VECTOR_BD_PATH, COLLECTION_NAME

os.environ["DASHSCOPE_API_KEY"] =DASHSCOPE_API_KEY
def get_embedding():
    return DashScopeEmbeddings(
        model=EMBEDDING_MODEL
    )
#根据分块的结果创建向量库
#建立向量库
def vectorize_chunks(chunks):
    embedding=get_embedding()
    if os.path.exists(VECTOR_BD_PATH) and os.listdir(VECTOR_BD_PATH):
        """加载已有向量库"""
        db=Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embedding,
            persist_directory=VECTOR_BD_PATH,
        )
    else:
        db=Chroma.from_documents(chunks,
                                 collection_name=COLLECTION_NAME,
                                 embedding=embedding,
                                 persist_directory=VECTOR_BD_PATH,
                                 )
    return db