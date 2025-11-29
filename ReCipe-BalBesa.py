from requests import get
from jsonpath_ng.ext import parse
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QWidget,
    QPushButton,
)
import sys
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
                f'"{titles[i]}" : {time[i]} минут, {','.join(ingredients)}\n\n'
            )
        with open("recipes_dict.txt", "w", encoding="UTF-8") as file:
            file.writelines(titles2)


class MainWindow(QMainWindow, API_Request, Data_converter):
    def __init__(self):
        super().__init__(includeIngredients="")

        self.setWindowTitle("ReCipe BalBesa")

        self.label = QLabel()

        self.button = QPushButton("Поиск")
        self.button.clicked.connect(self.return_search)
        self.button2 = QPushButton("Очистить")
        self.button2.clicked.connect(self.clear_search)

        self.input = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def return_search(self):
        global includeIngredients
        includeIngredients = self.input.text()
        request = API_Request(includeIngredients)
        request.API_get()
        converter = Data_converter()
        converter.JSON_Read_Convert()
        with open("recipes_dict.txt", "r", encoding="UTF-8") as file_out:
            lines = file_out.readlines()
        self.label.setText(f"{''.join(lines)}")

    def clear_search(self):
        self.label.clear()
        self.input.clear()
        with open("recipe_dict.json", "w") as file:
            pass
        with open("recipes_dict.txt", "w") as file2:
            pass


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
