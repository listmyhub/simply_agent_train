from email import message

from agent.my_llm import llm

# response=llm.chat.completions.create(
#     model="glm-5.3",
#     messages=[{"role":"user","content":"hello"}]
# )
# print(response.choices.message)
print(llm.invoke("hello"))