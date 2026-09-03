#通过查询扩展的方式
import dashscope
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

from RAG开发应用项目.config import GENERATE_MODEL, RETRIEVER_K, RERANK_MODEL, RERANK_TOPN
from RAG开发应用项目.data_processor import load_pdf, split_pdf
from RAG开发应用项目.vector_store import vectorize_chunks,get_embedding


def expand_query(query):
    """查询扩展：生成同意问法，提高召回率"""
    prompt=(f"""角色：你是一个语句拓展工具，
            任务：根据用户所输入的{query},生成同义的三个句子，以便于检索
            输出要求：每一个句子占一行输出,不需要解释""")
    resp=dashscope.Generation.call(
        model=GENERATE_MODEL,
        prompt=prompt,
    )
    subs=[line.strip() for line in resp.output.text.splitlines() if line.strip()]
    return [query]+subs
#构建混合检索器：向量语句+BM25关键词
def build_retriever(db,chunks):
    bm25=BM25Retriever.from_documents(chunks)
    bm25.k=RETRIEVER_K
    vector_ret=db.as_retriever(search_kwargs={"k":RETRIEVER_K})
    return EnsembleRetriever(retrievers=[vector_ret,bm25],
                             weights=[0.6,0.4])
#Rerank重排序
def rank_doc(query,docs):
    if not docs:
        return []
    texts=[d.page_content for d in docs]
    resp=dashscope.TextReRank.call(
        model=RERANK_MODEL,
        query=query,
        documents=texts,
        top_n=RERANK_TOPN,
    )
    return [docs[item["index"]]for item in resp.output.results]
#完整的检索全流程
def full_retriever(query,db,chunks):
    queries=expand_query(query)
    ensemble=build_retriever(db,chunks)
    all_docs=[]
    for q in queries:
        all_docs.extend(ensemble.invoke(q))
    #去重
    unique_doc=[]
    seen=set()
    for doc in all_docs:
        if doc.page_content not in seen:
            seen.add(doc.page_content)
            unique_doc.append(doc)
    return rank_doc(query,unique_doc)

if __name__=="__main__":
    file = load_pdf("C:\\Users\\范帅哥\\PycharmProjects\\PythonProject2\\src\\RAG开发应用项目\\input\\健康档案.pdf")
    chunks = split_pdf(file, "健康档案", "2026.9.2")
    db=vectorize_chunks(chunks)
    result=full_retriever("王五的医疗病史是什么",db,chunks)
    result_1=[d.page_content for d in result]
    for d in result_1:
        print(d)
        print("-"*50)
