from openai import OpenAI

client = OpenAI(
    api_key="sk-6hUzRJcA6jU7PB5UYGVIqsndQovhjtZgYHiOC2CKPxgnFHvz",         
    base_url="https://api.moonshot.cn/v1"     
)

resp = client.chat.completions.create(
    model="kimi-k2-instruct",                   
    messages=[{"role": "user", "content": "你好，世界！"}],
    temperature=0.7
)
print(resp.choices[0].message.content)
