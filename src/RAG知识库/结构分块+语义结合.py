import os
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import MarkdownHeaderTextSplitter

from RAG知识库.load1 import DASHSCOPE_API_KEY
from RAG知识库.递归分块 import text
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
vector_stores=Chroma.from_documents(final_split,
    embedding=embedings,
    persist_directory="./vector_db"
)

