from agent.my_llm import llm
reason=[]
for chunk in llm.stream("hello world"):
    print(type(chunk))
    print(chunk.content_blocks)
    reason_step=[r for r in chunk.content_blocks if r["type"]=="reasoning"]
    print(reason_step if reason_step else chunk.text)
