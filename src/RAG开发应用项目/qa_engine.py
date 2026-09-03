from http import HTTPStatus

import dashscope

from RAG开发应用项目.config import GENERATE_MODEL
from RAG开发应用项目.retriever import full_retriever


def build_prompt(query,docs):
    """强约束prompy :可追溯，不编造，不越界"""
    context=""
    for i,doc in enumerate(docs):
        meta=doc.metadata
        source=f"来源：{meta.get("archive_name","未知")},日期：{meta.get("record_date","未知")},第{meta.get("page",0)+1}页"
        context+=f"""[资料{i+1}]
        {doc.page_content}\n{source}\n---\n"""
    prompt = f"""
    角色：你是一个健康档案的问答助手，严格遵守一系列规则
    规则：1.只能根据下面的参考资料进行回答，资料中没有的内容，直接回答“未查询到相关健康档案”，严禁瞎编乱造。
    2.涉及到档案内容一定要标注来源，格式：[来源：档案名称 日期 页码]
    3.绝对不能提供诊疗建议，用药指导，病情诊断等内容
    4.回答简洁准确，可适当拓展。
    参考资料：
    {context if docs else "无相关资料"}
    用户的问题：{query}
    """
    return prompt
def health_qa(query,db,chunks):
    docs=full_retriever(query,db,chunks)
    prompt=build_prompt(query,docs)
    resp=dashscope.Generation.call(
        model=GENERATE_MODEL,
        prompt=prompt,
    )
    if resp.status_code !=HTTPStatus.OK or resp.output is None:
        return "查询失败，请稍后再试"
    answer=resp.output.text
    answer+="\n\n! 免责声明：本回答仅基于健康档案客观信息，不构成任何医疗建议，如有不适及时就医。"
    return answer

