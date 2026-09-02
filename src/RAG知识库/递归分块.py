from langchain_text_splitters import RecursiveCharacterTextSplitter


spliter=RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50,
    separators=["\n","。","！","?",",","\n\n"," ",""])
text="""## 1. 概述与背景
检索增强生成（Retrieval-Augmented Generation，简称 RAG）是一种结合了信息检索与文本生成的混合架构。它通过在生成回答前，先从外部知识库中检索相关文档，有效解决了大语言模型（LLM）的幻觉问题和知识时效性问题。RAG 的核心优势在于无需重新训练模型即可更新知识，同时保证了回答的可溯源性。
## 2. 核心处理流程
一个标准的 RAG 流程通常包含以下三个关键阶段：
1. **索引构建（Indexing）**：
   - 文档加载与清洗
   - **文本分块（Chunking）**：将长文档切分为语义完整的短文本
   - 向量化（Embedding）：使用 Embedding 模型将文本块转化为向量
    -存入向量数据库（如 Milvus, Pinecone, Chroma）
2. **检索（Retrieval）**：
   - 将用户查询（Query）向量化
   - 在向量数据库中进行相似度搜索（如余弦相似度）
   - 返回 Top-K 个最相关的上下文片段
3. **生成（Generation）**：
   - 将“用户问题”与“检索到的上下文”拼接成 Prompt
   - 输入 LLM 生成最终回答
## 3. 关键参数配置示例
在配置 RAG 系统时，以下参数至关重要：
| 参数名称 | 推荐值 | 说明 |
| :--- | :--- | :--- |
| `chunk_size` | 512 | 单个文本块的最大字符数，过大影响检索精度 |
| `chunk_overlap` | 50-100 | 块与块之间的重叠字符数，防止语义截断 |
| `top_k` | 3-5 | 检索返回的文档块数量 |
| `temperature` | 0.0-0.2 | 生成温度，RAG 场景建议低温度以保证事实性
我喜欢吃西瓜和苹果，我的名字叫张三，我的家在东北
"""
# chunks=spliter.split_text(text)
# for i,chunk in enumerate(chunks):
#     print(f"总共分成了{len(chunks)},其中第{i}块为：")
#     print(f"字符数：{len(chunk)}")
#     print(chunk)
