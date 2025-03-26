from openai import OpenAI

client = OpenAI(
    api_key="sk-mzsxdllbdabrmybzgmlermighzrhbvqzqevxsfttcvsxepnt",
    base_url="https://api.siliconflow.cn/v1"
)

# 发送非流式输出的请求
question = input("问题：")
messages = [
    {"role": "system", "content": "你是一个AI助手"},
    {"role": "user", "content": question}
]
response = client.chat.completions.create(
    model="Pro/deepseek-ai/DeepSeek-R1",
    messages=messages,
    stream=False,   # (非)流式输出：False/True
    # max_tokens=16384,   # 回答的最大长度（包含思维链输出）,输出大于max_token的情况下,会被截断,deepseek R1系列的max_token最大可设置为16K(16384)
    temperature=0.7,    # 温度参数,平衡创造性与可靠性,控制随机性
    top_p=0.95,  # 核采样,动态选择候选词集,从累积概率超过 p 的最小词集中采样,通常与 temperature 结合使用，平衡多样性和质量
    # top_k=50, # 限制候选词数量,限制模型在每一步生成时只从概率最高的 k 个词中选择
    frequency_penalty=0.5,  # 频率惩罚,减少重复词,降低已生成词的重复概率
)
# V3模型
# print(response)
# print(response.choices[0].message.content)

# R1模型
# 返回参数：content、reasoning_content
# print(response)
# print('---'*10)
reasoning_content = response.choices[0].message.reasoning_content.replace('\n\n', '\n')  # reasoning_content：思维链内容
content = response.choices[0].message.content.replace('\n\n', '\n')  # content：最终回答内容
print("推理：", reasoning_content, sep='\n')
print("回答：", content, sep='\n')

# Round 2、3、...
while True:
    print('---' * 20)
    question = input("问题：")
    if question == '':
        break
    messages.append({"role": "assistant", "content": content})  # assistant	模型生成的历史回复，为模型提供示例，说明它应该如何回应当前请求
    # messages.append({'role': 'user', 'content': "还有补充吗？"})
    messages.append({'role': 'user', 'content': question})
    response = client.chat.completions.create(
        model="Pro/deepseek-ai/DeepSeek-R1",
        messages=messages,
        stream=False
    )
    reasoning_content = response.choices[0].message.reasoning_content.replace('\n\n', '\n')
    content = response.choices[0].message.content.replace('\n\n', '\n')
    print("推理：", reasoning_content, sep='\n')
    print("回答：", content, sep='\n')
