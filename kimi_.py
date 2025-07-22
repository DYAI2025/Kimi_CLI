from openai import OpenAI
 
client = OpenAI(
    api_key="sk-6hUzRJcA6jU7PB5UYGVIqsndQovhjtZgYHiOC2CKPxgnFHvz", # <-- Replace MOONSHOT_API_KEY with the API Key you obtained from the Kimi Open Platform
    base_url="https://api.moonshot.ai/v1", # <-- Replace the base_url from https://api.openai.com/v1 to https://api.moonshot.ai/v1
)