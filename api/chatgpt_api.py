# api/chatgpt_api.py
import openai
import config.config as config

openai.api_type = config.API_TYPE
openai.api_base = config.API_ENDPOINT
openai.api_version = config.API_VERSION
openai.api_key = config.API_KEY

def chat_with_gpt(text):
    response = openai.ChatCompletion.create(
    engine="gpt-35-turbo",
    messages = [
            {"role": "system", "content": "You work for bank and your job is to identify the merchant category from a received text. Please write an answer without description. You can choose between Groceries, Shopping, Restaurants, Transport, Travel, Utilities, Etnertainment, Health, General. return None if you dont know. Return just text without any formatting.",},
            {"role": "user", "content": text},
        ],
    temperature=0.7,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None)

    return response.choices[0].message.content
