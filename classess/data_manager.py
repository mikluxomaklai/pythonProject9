import json
#from pprint import pprint as pp
from classess.exceptions import DataSourseBrokenException


class DataManager:

    def __init__(self, path):
        #путь к  файлу
        self.path = path

    def _load_data(self):
        """ Загружает данные из файла """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):

            raise DataSourseBrokenException("Файл поврежден")

        return data

    def _save_data(self, data):
        """ Перезаписывает переданные данные """
        with open(self.path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

    def get_all(self):
        """ Отдает полный список данных """
        data = self._load_data()
        return data

    def search(self, substring):
        """ Отдает посты, содержащие substring """

        posts = self._load_data()
        substring = substring.lower()

        matching_posts = [post for post in posts if substring in post["content"].lower()]

        return matching_posts

    def add(self, post):
        """ Добавдяет в хранилище постов конкретный пост"""

        if type(post) != dict:
            raise TypeError("Dict expected for adding post")

        posts = self._load_data()
        posts.append(post)
        self._save_data(posts)
