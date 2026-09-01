import os

from dashscope.embeddings import text_embedding
from langchain_community import embeddings
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_experimental.text_splitter import SemanticChunker

from RAG知识库.load1 import DASHSCOPE_API_KEY
from RAG知识库.递归分块 import text
# os.environ["DASHSCOPE_API_KEY"] = DASHSCOPE_API_KEY
embedings=DashScopeEmbeddings(
    model="text-embedding-v4"
)
senmatic_split=SemanticChunker(
    embeddings=embedings,
    breakpoint_threshold_type="percentile",
    breakpoint_threshold_amount=80,
    sentence_split_regex=r"(?<=[。！？])\s*",
    min_chunk_size=30
)
chunks=senmatic_split.split_text("""
中国气象局气象分析师沈雨旸表示，台风登陆后路径折向西南方向的情况不多见，是因“沙德尔”深入内陆后，受北侧高压和冷空气的压制，所以后期路径会往南走。
今天（30日）早晨5时，其中心已到达广东省清远市境内，虽然“沙德尔”总体移动较快，强降雨在一个地方停留时间不长，但降水效率高、雨量较大，影响不可小觑。
“沙德尔”残涡影响持续
南方强降雨将持续至9月初
在“沙德尔”及辐合带影响下，8月底9月初南方强降雨频繁。
29日夜间到30日，江苏、安徽、江西、湖南至广西等地强降雨集中，其中湖南南部至广西北部、海南岛西部等局地有大暴雨。
31日，冷空气推进至华南，海南岛大部、湖南、江西、广东及福建沿海等地强降雨集中。同时，位于残涡北侧倒槽区的江苏、安徽等地也将有大到暴雨、局地大暴雨。
从小到大，泡面一直被贴上“不健康、全是防腐剂”的标签，成为大众认知里的“垃圾食品”。
多年来，防腐剂替泡面稳稳背了数年黑锅。但根据人民日报健康等权威科普辟谣：市面上绝大多数泡面面饼，
压根不需要添加防腐剂，就能实现长期保质。大家对泡面的固有偏见，其实都是一场流传已久的认知误区。
我爱吃苹果和香蕉，他们是最好吃的水果
""")
for i,chunk in enumerate(chunks):
    print(f"总共分成了{len(chunks)},其中第{i+1}块为：")
    print(f"字符数：{len(chunk)}")
    print(chunk)