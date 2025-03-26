# 实现真正的AI问答 --- by：天青色等烟雨_1ijunha0
from openai import OpenAI

client = OpenAI(
    api_key="sk-mzsxdllbdabrmybzgmlermighzrhbvqzqevxsfttcvsxepnt",
    base_url="https://api.siliconflow.cn/v1"
)

# 发送流式输出的请求
question = input("问题：")
messages = [
    {"role": "system", "content": "你是一个AI助手"},
    {"role": "user", "content": question}
]
response = client.chat.completions.create(
    model="Pro/deepseek-ai/DeepSeek-R1",
    messages=messages,
    stream=True,  # 流式输出：False/True
    # max_tokens=16384,   # 回答的最大长度（包含思维链输出）,输出大于max_token的情况下,会被截断,deepseek R1系列的max_token最大可设置为16K(16384)
    temperature=0.7,  # 温度参数,平衡创造性与可靠性,控制随机性
    top_p=0.95,  # 核采样,动态选择候选词集,从累积概率超过 p 的最小词集中采样,通常与 temperature 结合使用，平衡多样性和质量
    frequency_penalty=0.5,  # 频率惩罚,减少重复词,降低已生成词的重复概率
)

# 存储原始内容，用于后续处理(如上下文拼接连续问答)
content_bak = ""
reasoning_content_bak = ""
# 初始化标志位，用于跟踪是否已添加前缀
reasoning_content_started = False
content_started = False


# 输出函数
def res_run(res=response, reasoning_flag=reasoning_content_started, content_flag=content_started):
    # 声明全局变量
    global content_bak
    global reasoning_content_bak
    # 逐步接收并处理响应
    for chunk in res:
        # print(chunk.choices[0].delta)   # 获取当前块的增量数据
        if not chunk.choices:
            continue

        # 处理思维链内容（reasoning_content）
        if chunk.choices[0].delta.reasoning_content:
            if not reasoning_flag:
                print("推理：")  # 首次添加推理前缀
                reasoning_flag = True
            # 替换双换行并流式输出
            reasoning_content = chunk.choices[0].delta.reasoning_content.replace('\n\n', '\n')
            print(reasoning_content, end='', flush=True)
            # 拼接原始内容存储
            reasoning_content_bak += reasoning_content

        # 处理最终内容（content）
        if chunk.choices[0].delta.content:
            if not content_flag:
                print("回答：", end='')  # 首次添加回答前缀
                content_flag = True
            # 替换双换行并流式输出
            content = chunk.choices[0].delta.content.replace('\n\n', '\n')
            print(content, end='', flush=True)
            # 拼接原始内容存储
            content_bak += content


res_run()    # 运行输出

# Round 2、3、...
while True:
    print('\n', '---' * 20, sep='')
    question = input("问题：")
    if question == '':
        break
    messages.append({"role": "assistant", "content": content_bak})  # assistant	模型生成的历史回复，为模型提供示例，说明它应该如何回应当前请求
    messages.append({'role': 'user', 'content': question})
    response = client.chat.completions.create(
        model="Pro/deepseek-ai/DeepSeek-R1",
        messages=messages,
        stream=True
    )
    res_run(res=response, reasoning_flag=False, content_flag=False)
