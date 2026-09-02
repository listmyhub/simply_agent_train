import os
from enum import unique
from typing import List

import dashscope
from langchain_chroma import Chroma
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import MarkdownHeaderTextSplitter

from RAG知识库.load1 import DASHSCOPE_API_KEY
from RAG知识库.递归分块 import text
from agent.my_llm import llm

#先进行结构化分块
md_spliter=MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#","一级标题"),
        ("##","二级标题"),
        ("###","三级标题")
    ]
)
#对每一章节进行语义分块
os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY
embedings=DashScopeEmbeddings(
    model="text-embedding-v4"
)
senmatic_split=SemanticChunker(
    embeddings=embedings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=80,
    sentence_split_regex=r"(?<=[。！？ \n])\s*",
    min_chunk_size=50
)
splits=md_spliter.split_text(text.strip())
final_split=[]
for doc in splits:
    sematic_chunk=senmatic_split.split_documents([doc])
    for chunk in sematic_chunk:
        if  chunk.page_content.strip():
            chunk.metadata.update(doc.metadata)
            final_split.append(chunk)
#创建向量库
if os.path.exists("./vector_db"):
    print("向量库已经存在，直接加载")
    vector_stores=Chroma(
        embedding_function=embedings,
        persist_directory="./vector_db")
else:
    print("向量库不存在，直接生成")
    vector_stores=Chroma.from_documents(final_split,
        embedding=embedings,
        persist_directory="./vector_db"
    )
#重排序
def rerank_retreive(query:str,db,retreive_k=6):
    raw_retreives=db.similarity_search(query,retreive_k)
    # 重排序
    resp = dashscope.TextReRank.call(
        model="qwen3-rerank", top_n=3,
        query=query,
        documents=[d.page_content for d in raw_retreives]
    )
    out_rep=[raw_retreives[item['index']] for item in resp.output.results]
    return out_rep
#混合检索
bm25_retriever=BM25Retriever.from_documents(final_split)
bm25_retriever.k=3
vector_retriever=vector_stores.as_retriever(search_kwargs={"k":3})
ensemble_retriever=EnsembleRetriever(
    retrievers=[vector_retriever,bm25_retriever],
    weights=[0.6,0.4]
)
#语句拓展检索
#调用模型将用户问题拓展
def generate_query(query:str)->List[str]:
    promot=f"""你是一个帮助用户拓展语句的工具，
    根据用户输入的问题{query}，
    生成3个语义相同的句子，用于检索。
    不要解释，只要结果
    每一句单独一行，一共三行。
    """
    resp=dashscope.Generation.call(
        model="qwen-turbo",
        prompt=promot
    )
    text=resp.output.text
    subs=[line.strip() for line in text.splitlines() if line.strip()]
    return [query]+subs
#将拓展后的的问题全部进行检索后合并去重
def expansion_rertiever(query:str):
    expansion_query=generate_query(query)
    unique=[]
    seen=set()
    retrieved=[]
    for doc in expansion_query:
        retrievers=vector_stores.similarity_search(doc,3)
        retrieved.extend(retrievers)
    for d in retrieved:
        if d.page_content not in seen:
            seen.add(d.page_content)
            unique.append(d)
    return unique
#再次进行重排序
def rerank_again(query:str,uniqued:List[Document]):
    resp=dashscope.TextReRank.call(
        model="qwen3-rerank", top_n=3,
        query=query,
        documents=[d.page_content for d in uniqued]
    )
    out_rep=[uniqued[item['index']] for item in resp.output.results]
    return out_rep




if __name__=="__main__":
    rep1=rerank_retreive("RAG基础流程是什么",vector_stores)
    print(rep1)
    resp=ensemble_retriever.invoke("RAG基础流程是什么")
    print(resp)
    print(generate_query("RaG的基础流程是什么"))
    uniqued=expansion_rertiever("RaG的基础流程是什么")
    print(uniqued)
    print(rerank_again("RaG的基础流程是什么",uniqued))