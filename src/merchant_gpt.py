from api import chatgpt_api

def get_merchant_category(merchant):
        result = None

        try:
            response = chatgpt_api.chat_with_gpt(merchant)
            result = None if response == 'None' else response
        except Exception as e:
            print('Error', e)
        finally:
            return result