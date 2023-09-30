# tests/test_chatgpt_api.py
import unittest
from unittest.mock import patch
from api import chatgpt_api

class TestChatGPTAPI(unittest.TestCase):
    #@patch('api.chatgpt_api.requests.post')
    def test_chat_with_gpt(self):
        # Define a sample prompt
        prompt = "Translate the following English text to French: 'Hello, how are you?'"

        # Define a sample API response
        api_response = {
            "status_code": 200,
            "json": {
                "choices": [
                    {
                        "message": {
                            "content": "Bonjour, comment ça va ?",
                            "role": "assistant",
                            "index": 0
                        }
                    }
                ]
            }
        }

        # Configure the mock's return value to simulate an API response
        #mock_post.return_value = api_response

        print("response")

        # Call the ChatGPT API function
        response = chatgpt_api.chat_with_gpt(prompt)

        # Assert that the API was called with the correct data
        mock_post.assert_called_once_with(
            chatgpt_api.API_ENDPOINT,
            data='{"model": "gpt-3.5-turbo", "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Translate the following English text to French: \'Hello, how are you?\'"}]}',
            headers={
                'Authorization': f'Bearer {chatgpt_api.API_KEY}',
                'Content-Type': 'application/json'
            }
        )

        # Assert that the response matches the expected content
        self.assertEqual(response, "Bonjour, comment ça va ?")

if __name__ == '__main__':
    unittest.main()
