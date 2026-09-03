from RAG开发应用项目.config import PDF_PATH
from RAG开发应用项目.data_processor import load_pdf, split_pdf
from RAG开发应用项目.qa_engine import health_qa
from RAG开发应用项目.retriever import full_retriever
from RAG开发应用项目.vector_store import vectorize_chunks

if __name__=="__main__":
    query="王五是谁"
    # 第一步：加载文件并分块
    file = load_pdf(PDF_PATH)
    chunks = split_pdf(file, "健康档案", "2026.9.2")
    # 第二步：建立向量库
    db=vectorize_chunks(chunks)
    # 第三步：进行检索
    docs=full_retriever(query,db,chunks)
    # 第四步：问答
    results=health_qa(query,db,chunks)
    print("问题：",query)
    print("回答：",results)