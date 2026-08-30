from langchain_text_splitters import MarkdownHeaderTextSplitter

from RAG知识库.递归分块 import text

md_spliter=MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#","一级标题"),
        ("##","二级标题"),
        ("###","三级标题")
    ]
)
splits=md_spliter.split_text(text)
for idx,doc in enumerate(splits):
    print(f"第{idx+1}个章节块")
    print(doc.page_content)
    print(doc.metadata)
    print("-"*50)