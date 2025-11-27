from requests import get
import json


class API_Request:

    def __init__(
        self,
        includeIngredients,
        maxReadyTime=60,
        number=5,
        HTTPS="https://api.spoonacular.com/recipes/complexSearch",
        apiKey="5ae743794a224759999e7e85d2e890ea",
    ):
        self.HTTPS = HTTPS
        self.includeIngredients = includeIngredients
        self.maxReadyTime = maxReadyTime
        self.number = number
        self.apiKey = apiKey

    def API_get(self):
        params = {
            "apiKey": self.apiKey,
            "includeIngredients": self.includeIngredients,
            "maxReadyTime": self.maxReadyTime,
            "number": self.number,
        }
        response = get(self.HTTPS, params=params)
        data = response.json()
        print(response)
        with open("recipe_dict.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
