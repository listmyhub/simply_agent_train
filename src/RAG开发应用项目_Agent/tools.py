from langchain_chroma import Chroma
from langchain_core.tools import tool

from RAG开发应用项目.config import EMBEDDING_MODEL, COLLECTION_NAME, VECTOR_BD_PATH, PDF_PATH
from RAG开发应用项目.data_processor import load_pdf, split_pdf
from RAG开发应用项目.qa_engine import health_qa
from RAG开发应用项目.vector_store import get_embedding, vectorize_chunks

file=load_pdf(PDF_PATH)
chunks=split_pdf(file,"健康档案","2026.9.2")
bd=vectorize_chunks(chunks)
@tool
def health_answer(query:str)->str:
    """根据用户的问题进行检索健康档案问答

    Args:
        query:用户所需查询的问题

    Returns:
        返回根据健康档案所检索的资料所生成的字符串答案
    """
    global bd,chunks
    return health_qa(query,bd,chunks)

