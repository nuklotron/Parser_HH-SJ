import requests
import json
from abc import ABC, abstractmethod
from src.vacancy import Vacancy


class InitApi(ABC):
    """
    Абстрактный класс для методов класса
    """
    @abstractmethod
    def get_request(self):
        pass

    @abstractmethod
    def get_parsed_data(self):
        pass


class HHApi(InitApi):
    """
    Класс подключается к API HH и получает вакансии по ID работодателя
    sber - 3529
    yandex - 1740
    vk - 15478
    tele2 - 4219
    gazprom - 39305
    heineken - 1186
    raiff - 4023
    lenta - 7172
    megafon - 3127
    avito - 84585
    """
    def __init__(self):
        self.employer_id = [3529, 1740, 15478, 4219, 39305, 1186, 4023, 7172, 3127, 84585]
        self.data = []
        self.vacancies = []

    def get_request(self):
        """
        Подключение к API HH по ID работодателя, запись сырых данных в список self.data
        :return: self.data
        """
        for emp in self.employer_id:

            api_url = f"https://api.hh.ru/vacancies?employer_id={emp}"

            params = {
                "employer_id": emp,
                "per_page": 100
            }

            header = {"User-Agent": "My_App_v1.0"}

            req = requests.get(api_url, headers=header, params=params)

            if req.status_code != 200:
                raise Exception(f"Ошибка в получении доступа к данным")

            data_json = json.loads(req.text)["items"]
            self.data.append(data_json)

            req.close()

        return self.data

    def get_parsed_data(self):
        """
        Приведение вакансий к общему виду.
        :return: self.vacancies
        """
        for item in self.data:
            vacancy = Vacancy()
            try:
                for i in range(0, 100):
                    vacancy.title = item[i]["name"]
                    vacancy.description = item[i]["snippet"]["requirement"]
                    vacancy.city = item[i]["area"]["name"]
                    vacancy.url = item[i]["alternate_url"]

                    if item[i]["salary"]:
                        vacancy.salary_from = item[i]["salary"]["from"] if item[i]["salary"]["from"] else 0
                        vacancy.salary_to = item[i]["salary"]["to"] if item[i]["salary"]["to"] else 0
                    vacancy.employer = item[i]["employer"]["name"]
                    vacancy.emp_id = item[i]["employer"]["id"]

                    self.vacancies.append(vacancy.get_json())

            except Exception as err:
                print("Ошибка в данных ['item'] - ", err)

        return self.vacancies
