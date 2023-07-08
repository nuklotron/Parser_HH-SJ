from src.db_manager import *
from src.hh_api import *


def main():
    # инициализируем класс БД
    db = DBManager()

    # создаем БД и таблицы
    db.create_database()
    db.create_tables()

    # получаем данные из API HH
    employers = [3529, 1740, 15478, 4219, 39305, 1186, 4023, 7172, 3127, 84585]

    for emp in employers:
        api = HHApi(emp)

        api.get_request()
        data = api.get_parsed_data()

        # заполняем таблицы БД из полученных данных
        db.fill_table_vacancies(data)
        db.fill_table_employers()

    # вывод необходимых данных
    # db.get_companies_and_vacancies_count()
    # db.get_all_vacancies()
    # db.get_avg_salary()
    # db.get_vacancies_with_higher_salary()
    # db.get_vacancies_with_keyword("стаж")


if __name__ == "__main__":
    main()
