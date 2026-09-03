import datetime
import re
from typing import List

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from RAG开发应用项目.config import CHUNK_SIZE, CHUNK_OVERLAP, PDF_PATH


#脱敏档案
def desensite(text:str)->str:
    """移除个人敏感信息"""
    text=re.sub(r"1[3-9]\d{9}","***",text)#手机号码
    text=re.sub(r"\d{17}[\dXx]","***",text)#身份证号
    text=re.sub(r"(姓名|患者|体检人)[:：]\s*\S+",r"\1: ***",text)
    return text


#按页加载pdf文件
def load_pdf(path:str):
    loader=PyMuPDFLoader(path)
    page_docs=loader.load()
    return page_docs
#对加载后的pdf进行分块切片
def split_pdf(docs:List[Document],archive_name:str,record_time:str):
    """先对doc进性脱敏"""
    for doc in docs:
        doc.page_content=desensite(doc.page_content)
        doc.metadata["archive_name"]=archive_name
        doc.metadata["record_time"]=record_time
        doc.metadata["archive_type"]="健康档案"
        doc.metadata["process_time"]=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    """进行分块操作，子块继承父块的元数据"""
    spliter=RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["/n/n","/n","。",";"," ",""]
    )
    chunks=spliter.split_documents(docs)
    return chunks


if "__main__" == __name__:
    file=load_pdf(PDF_PATH)
    chunks=split_pdf(file,"健康档案","2026.9.2")
    chunk=[d.page_content for d in chunks]
    print(chunk)
