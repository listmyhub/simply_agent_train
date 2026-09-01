import dashscope
# from RAG知识库.

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
res=rerank_retreive("RAG是做什么的",db=vector_stores)
print(res)