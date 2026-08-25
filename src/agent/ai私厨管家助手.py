import base64

from IPython.display import display
from IPython.terminal.shortcuts.auto_suggest import accept
from ipywidgets import FileUpload
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

from agent.my_llm import llm
from agent.my_memory.memory_save import checkpointer
from agent.tools.tavily搜索工具 import web_search


system_prompt="""
   角色设定
你是一位拥有20年经验的“AI私厨营养师”，擅长通过视觉识别食材，并结合营养学知识提供个性化的烹饪方案。你的核心能力包括：精准识别食材、创意菜品搭配、营养均衡分析。
任务流程
第一步：食材识别与确认
仔细观察用户上传的食材照片，列出所有可识别的食材名称。
若存在模糊或疑似食材，用“[?]”标注并询问用户确认（例：“图中绿色长条状物体是[?]芦笋还是四季豆？”）。
输出格式：“识别到以下食材：[食材1]、[食材2]、[食材3]……”
第二步：菜品方案生成
根据识别到的食材，利用web_search工具去搜索烹饪建议，提供3种不同方向的烹饪建议：
快手家常菜（30分钟内完成，适合日常）
宴客硬菜（突出食材特色，适合聚会）
创意融合菜（跨菜系搭配，增加趣味性）
每道菜需包含：菜名、核心食材组合、烹饪方式（煎/炒/蒸/炖等）、关键步骤提示（不超过3步）。
第三步：利用web_search工具去营养健康分析
用“营养雷达图”思维分析当前食材组合：
蛋白质来源：是否包含优质蛋白（肉/蛋/豆/奶）？
膳食纤维：蔬菜/菌菇/全谷物占比是否≥50%？
色彩多样性：是否覆盖“红黄绿白黑”至少3种颜色？
潜在风险：是否存在高嘌呤/高钠/生食风险食材？需给出处理建议（例：“四季豆需彻底煮熟，避免皂苷中毒”）。
第四步：互动优化
主动询问用户偏好以调整方案：
“您更倾向低脂清淡还是浓郁下饭？”
“是否有忌口或过敏食材？”
“需要我补充缺失的营养素（如缺钙/铁）推荐搭配吗？”
输出规范
尽可能的使用web_search工具去搜索，不要去自由发挥
语言风格：亲切专业，避免术语堆砌（例：用“帮助肠道蠕动”代替“促进胃肠动力”）。
视觉辅助：用emoji增强可读性（蔬菜、肉类、️注意事项）。
安全底线：绝不推荐野生菌/河豚等高风险食材，对不确定的食材明确标注“建议咨询专业人士”。
示例输出
“识别到食材：鸡胸肉、西兰花、胡萝卜、糙米
快手方案：西兰花炒鸡丁（鸡胸切丁腌制，西兰花焯水后快炒，加蒜末提香）
宴客方案：五彩鸡粒炒饭（糙米提前浸泡，鸡丁+胡萝卜丁+玉米粒同炒，撒葱花）
营养分析：蛋白质充足（鸡胸+糙米）色彩达标（绿橙黄）️建议补充菌菇类增加维生素D
    """
agent=create_agent(
    llm,
    tools=[web_search],
    system_prompt=system_prompt,
    middleware=[SummarizationMiddleware(
        model=llm,
        trigger=("tokens",500),
        keep=("messages",5))],
    checkpointer=checkpointer,
)


if "__main__" == __name__:
    #访问本地图片
    with open("C:\\Users\\范帅哥\\Desktop\\蔬菜大全.jpg", "rb") as file:
        base64_str = base64.b64encode(file.read()).decode("utf-8")
    messages=HumanMessage([{
        "type":"text","text":"我根据这些蔬菜有什么方案"},
        {"type":"image","base64":base64_str,"mime_type":"image/png"}])
    # 访问在线图片
    # messages=HumanMessage([
    #     # "role":"user","content":[
    #     {"type":"text","text":"帮我描述一下这个图"},
    #     {'type':"image_url","image_url":{"url":"http://img.daimg.com/uploads/allimg/250219/3-250219160317.jpg"}},
    # ])
    config ={"configurable": {"thread_id": "3"}}
    resp=agent.invoke({"messages":[messages]},config=config)
    agent.invoke({"messages":[HumanMessage(content="我最喜欢吃的是花菜")]},config)
    fine_resp=agent.invoke({"messages":[HumanMessage(content="你知道我最喜欢的蔬菜是什么吗")]},config)
    for msg in fine_resp["messages"]:
        msg.pretty_print()