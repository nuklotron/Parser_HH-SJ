import psycopg2


class DBManager:
    """
    Класс для работы с БД, создает саму БД, таблицы, выводит необхимые данные из БД
    Для работы необходимо изменить пароль в __init__
    """
    def __init__(self):
        self.host = "localhost"
        self.database = "cw5_employers_vacancies"
        self.user = "postgres"
        self.password = "12345"
        self.port = "5432"
        self.conn = None

    def create_database(self):
        """
        создание БД
        """
        self.conn = psycopg2.connect(host=self.host, database="postgres", user=self.user, password=self.password)
        self.conn.autocommit = True
        cur = self.conn.cursor()
        cur.execute("DROP DATABASE IF EXISTS cw5_employers_vacancies")
        cur.execute("""
                        CREATE DATABASE cw5_employers_vacancies
                            WITH
                            OWNER = postgres
                            ENCODING = 'UTF8'
                            CONNECTION LIMIT = -1
                            IS_TEMPLATE = False;
                        """)
        self.conn.commit()
        cur.close()

    def create_tables(self):
        """
        Создание таблиц
        """
        self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS vacancies, employers")
                cur.execute("""
                        CREATE TABLE vacancies
                        (
                            title varchar(100) NOT NULL,
                            description text,
                            salary_from int,
                            salary_to int,
                            city varchar(100),
                            url text,
                            employer varchar(100),
                            emp_id int
                        );
                        """)

                cur.execute("""CREATE TABLE employers
                                (
                                    emp_id int PRIMARY KEY,
                                    employer varchar(100) NOT NULL,
                                    vacancies_qty int
                                );
                            """)

                self.conn.commit()
        self.conn.close()

    def fill_table_vacancies(self, data):
        """
        заполнение таблицы с вакансиями из полученных данных
        """
        self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        for vacancy in data:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute("INSERT INTO vacancies (title, description, salary_from, salary_to, city, url, employer, emp_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                (vacancy["title"], vacancy["description"], vacancy["salary_from"], vacancy["salary_to"], vacancy["city"], vacancy["url"], vacancy["employer"], vacancy["emp_id"]))

                    self.conn.commit()
        self.conn.close()

    def fill_table_employers(self):
        """
        заполнение таблицы с работодателями из полученных данных
        """
        self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("INSERT INTO employers SELECT DISTINCT emp_id, employer, (SELECT COUNT(*) FROM vacancies) FROM vacancies")
                self.conn.commit()
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании
        """
        self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(emp_id) AS employers_qty, SUM(vacancies_qty) AS vacancies_qty FROM employers")
                rows = cur.fetchall()
                for row in rows:
                    print(f"Количество работодателей - {row[0]}")
                    print(f"Количество вакансий - {row[1]}")
        self.conn.close()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        :return:
        """
        self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT employer, description, salary_from, salary_to, url FROM vacancies")
                rows = cur.fetchall()
                for row in rows:
                    print(f"Работодатель - {row[0]}")
                    print(f"Описание вакансии - {row[1]}")
                    print(f"ЗП (среднее 'от/до') - {(row[2]+row[3])//2}")
                    print(f"Ссылка - {row[4]}\n")
        self.conn.close()

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям
        :return:
        """
        self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT AVG(salary_from + salary_to)::numeric(100,2) AS avg_salary FROM vacancies")
                rows = cur.fetchall()
                for row in rows:
                    print(f"Средняя зарплата по вакансиям - {row[0]} руб.")

        self.conn.close()

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        :return:
        """
        self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT employer, description, salary_from, salary_to, url FROM vacancies WHERE salary_from + salary_to / 2 > 58136")
                rows = cur.fetchall()

                for row in rows:
                    print(f"Работодатель - {row[0]}")
                    print(f"Описание вакансии - {row[1]}")
                    print(f"ЗП (среднее 'от/до') - {(row[2] + row[3]) // 2}")
                    print(f"Ссылка - {row[4]}\n")

        self.conn.close()
        pass

    def get_vacancies_with_keyword(self, keyword):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”
        :return:
        """
        self.conn = psycopg2.connect(host=self.host, database=self.database, user=self.user, password=self.password)
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(f"SELECT employer, description, salary_from, salary_to, url FROM vacancies WHERE title LIKE '%{keyword}%'")
                rows = cur.fetchall()
                for row in rows:
                    print(f"Работодатель - {row[0]}")
                    print(f"Описание вакансии - {row[1]}")
                    print(f"ЗП (среднее 'от/до') - {(row[2] + row[3]) // 2}")
                    print(f"Ссылка - {row[4]}\n")

        self.conn.close()
