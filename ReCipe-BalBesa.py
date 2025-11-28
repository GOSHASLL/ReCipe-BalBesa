from requests import get
import json
from jsonpath_ng.ext import parse


class Data_converter:

    def JSON_Read_Convert(self):
        with open("recipe_dict.json", encoding="UTF-8") as file:
            recipe_dict = json.load(file)
        jsonpath_titles = parse("$.results[*]..title").find(recipe_dict)
        titles = [match.value for match in jsonpath_titles]
        print(titles)
        jsonpath_time = parse("$.results[*]..readyInMinutes").find(recipe_dict)
        time = [match.value for match in jsonpath_time]
        print(time)
        titles2 = []
        for i in range(len(titles)):
            jsonpath_ingredients = parse(
                f"$.results[{i}].extendedIngredients[*].original"
            ).find(recipe_dict)
            ingredients = [match.value for match in jsonpath_ingredients]
            titles2.append(
                f'"{titles[i]}" : {time[i]} минут, {','.join(ingredients)}\n'
            )
        with open("recipes_dict.txt", "w", encoding="UTF-8") as file:
            file.writelines(titles2)


converter = Data_converter()
converter.JSON_Read_Convert()


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
            "number": self.number,
            "includeIngredients": self.includeIngredients,
            "maxReadyTime": self.maxReadyTime,
            "addRecipeInformation": True,
            "fillIngredients": True,
        }
        response = get(self.HTTPS, params=params)
        data = response.json()
        print(response)
        with open("recipe_dict.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)


request = API_Request(includeIngredients="tomato,cheese")
request.API_get()
