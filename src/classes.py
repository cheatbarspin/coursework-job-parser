import json
import os
from abc import ABC, abstractmethod
from pprint import pprint

import requests


class Engine(ABC):
    @abstractmethod
    def get_request(self):
        """Метод для получения запроса от API"""
        pass

    @staticmethod
    def get_connector():
        """ Возвращает экземпляр класса Connector """
        json_saver = JSONSaver('Python1.json')
        return json_saver

    @staticmethod
    def get_convertation(salary_to, salary_from):
        """Метод для конвертации иностранной валюты в Рубли"""
        salary_min = 0
        salary_max = 0
        if salary_to:
            salary_min = int(salary_to) * 83
        if salary_from:
            salary_max = int(salary_from) * 83
        return salary_min, salary_max


class HeadHunterAPI(Engine):
    def get_request(self, keyword='Python'):
        """Метод для получения запроса по ключевому слову и записью в JSON"""
        # headers = {
        #     "User-Agent": "MyApp/1.0 (my-app-feedback@example.com)"
        # }
        for i in range(1, 11):
            params = {
                "user_agent": "Mozilla/4.0",
                "text": keyword,
                "page": i,
                "per_page": 50,
                "area": 113
            }
            response = requests.get("https://api.hh.ru/vacancies", params=params)
            count = 0
            for item in response.json()['items']:
                new_dict = {}
                new_dict['name'] = item['name']
                salary = item.get('salary')
                if salary:
                    if item['salary']['currency'] == "RUR":
                        new_dict['salary_min'] = item['salary']['from']
                        new_dict['salary_max'] = item['salary']['to']
                    else:
                        new_dict['salary'] = self.get_convertation(item['salary']['from'], item['salary']['to'])
                new_dict['employer'] = item['employer']['name']
                new_dict['link'] = item['alternate_url']
                print(new_dict)
                self.get_connector().add_vacancies(new_dict)
                count += 1
                print(count)
            return response

    # def get_vacancies(self, keyword, count=1000):
    #     pages = 1
    #     response = []
    #
    #     for page in range(pages):
    #         print(f"Парсинг страницы {page + 1}", end=": ")
    #         values = self.get_request(keyword, page)
    #         print(f"Найдено {len(values)} вакансий.")
    #         response.extend(values)
    #
    #     return response


class Vacancy:
    __slots__ = ('title', 'salary_min', 'salary_max', 'employer', 'link')

    def __init__(self, title, salary_min, salary_max, employer, link):
        self.title = title
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.employer = employer
        self.link = link


class JSONSaver:
    def __init__(self, filename):
        """Инициализатор класса JSONSaver"""
        self.__filename = filename
        if not os.path.exists(self.__filename):
            with open(self.__filename, 'w', encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)

    @property
    def filename(self):
        return self.__filename

    # @filename.setter
    # def filename(self, value):
    #     self.__filename = value

    def add_vacancies(self, data):
        """Метод для добавления вакансий"""
        if os.stat(self.__filename).st_size != 0:
            with open(self.__filename, 'r', encoding="utf-8") as fl:
                res = json.load(fl)
                res.append(data)
                with open(self.__filename, 'w', encoding="utf-8") as file:
                    json.dump(res, file, indent=4, ensure_ascii=False)


hh = HeadHunterAPI()
res = hh.get_request()
# json_saver = JSONSaver('Python2.json')
# json_saver.add_vacancies(res)
