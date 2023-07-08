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
    def __init__(self, employer_id):
        self.employer_id = employer_id
        self.api_url = f"https://api.hh.ru/vacancies?employer_id={self.employer_id}"
        self.data = []
        self.vacancies = []

    def get_request(self):

        for page in range(0, 10):

            params = {
                "employer_id": self.employer_id,
                "page": page,
                "per_page": 100
            }

            header = {"User-Agent": "My_App_v1.0"}

            req = requests.get(self.api_url, headers=header, params=params)

            if req.status_code != 200:
                raise Exception(f"Ошибка в получении доступа к данным")

            self.data = json.loads(req.text)["items"]
            self.data.append(self.data)

            req.close()

        return self.data

    def get_parsed_data(self):
        """
        Приведение вакансий к общему виду.
        :return: список вакансий
        """
        for item in self.data:
            vacancy = Vacancy()
            try:
                vacancy.title = item["name"]
                vacancy.description = item["snippet"]["requirement"]
                vacancy.city = item["area"]["name"]
                vacancy.url = item["alternate_url"]

                if item["salary"]:
                    vacancy.salary_from = item["salary"]["from"] if item["salary"]["from"] else 0
                    vacancy.salary_to = item["salary"]["to"] if item["salary"]["to"] else 0
                vacancy.employer = item["employer"]["name"]
                vacancy.emp_id = item["employer"]["id"]

                if item["employer"]["id"] != 0:
                    self.vacancies.append(vacancy.get_json())

            except Exception as err:
                print("Ошибка в данных ['item'] - ", err)


            # vac = json.dumps(self.vacancies, indent=6, ensure_ascii=False)

        return self.vacancies
