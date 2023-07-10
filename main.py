from src.db_manager import DBManager
from src.hh_api import HHApi


def main():
    # # инициализируем класс БД
    db = DBManager()

    # # создаем БД и таблицы, закомментировать после создания БД и таблиц
    db.create_database()
    db.create_tables()

    # # получаем данные из API HH, закомментировать, если данные подгружать не нужно
    api = HHApi()

    api.get_request()
    data = api.get_parsed_data()

    # # заполняем таблицы БД из полученных данных, закомментировать после заполнения таблиц
    db.fill_table_vacancies(data)
    db.fill_table_employers()

    # # вывод необходимых данных, убрать комментарии после создания и заполнения БД
    # db.get_companies_and_vacancies_count()
    # db.get_all_vacancies()
    # db.get_avg_salary()
    # db.get_vacancies_with_higher_salary()
    # db.get_vacancies_with_keyword("стаж")


if __name__ == "__main__":
    main()
