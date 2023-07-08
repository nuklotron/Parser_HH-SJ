class Vacancy:
    """
    Класс приводит получаемые данные к общему виду для последующей записи
    """
    def __init__(self, title="нет названия", salary_from=0, salary_to=0, descrip="нет описания", city="нет города", url="нет ссылки", employer="работодатель", emp_id=0):
        self.title = title
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.description = descrip
        self.city = city
        self.url = url
        self.employer = employer
        self.emp_id = emp_id

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.title}', {self.salary_from}-{self.salary_to})"

    def __str__(self):
        return f"Вакансия:{self.title}\nЗП: {self.salary_from}-{self.salary_to}\nГород:{self.city}\nURL:{self.url}"

    def get_json(self):
        return {
            "title": self.title,
            "description": self.description,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "city": self.city,
            "url": self.url,
            "employer": self.employer,
            "emp_id": self.emp_id
            }
