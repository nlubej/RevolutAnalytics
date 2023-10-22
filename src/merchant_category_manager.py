import json
from src.merchant_gpt import get_merchant_category

class MerchantCategoryManager:
    def __init__(self):
        self.merchant_file_path = 'merchant_category.json'
        self.merchant_category = self.__load_merchant_data()

    def __load_merchant_data(self):
        try:
            with open(self.merchant_file_path, 'r') as json_file:
                return json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}  # Create an empty object if the file doesn't exist or is not valid JSON.

    def update_category(self, merchant, category):
        self.merchant_category[merchant] = category

    def determine_category(self, merchant):
        merhant_exists = True if merchant in self.merchant_category.keys() and self.merchant_category[merchant] != None else False

        if merhant_exists:
            return self.merchant_category[merchant]
        
        print(merchant, merhant_exists)

        category = get_merchant_category(merchant)
        self.update_category(merchant, category)

        return category
    
    def save_merchant_data(self):
        with open(self.merchant_file_path, 'w') as json_file:
            json.dump(self.merchant_category, json_file, ensure_ascii=False, indent=4)