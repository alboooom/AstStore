from flask import g
import psycopg2.pool
from psycopg2.extras import DictCursor

"""Модуль для работы с БД (PostgresQL)."""


class DataBase:

    def __init__(self):
        """Инициализация объекта для работы с БД."""
        self.connection_pool = None
        self.app = None

    def init_app(self, app):
        """
        Присвоение объекту ссылки на Flask приложение, создания пула
        подключений, настройка декоратора для автоматического закрытия
        соединения при выходе из контекстка приложения (см. Doc. FLASK).


        :param app: экземпляр Flask приложения.
        """
        self.app = app
        self.create_pool()

        @app.teardown_appcontext
        def teardown_db_conn(response_or_exception):
            conn = g.pop('db_conn', None)
            if conn is not None:
                self.connection_pool.putconn(conn)
                print('Соединение с БД закрыто')

    def create_pool(self):
        """Создания пула соединений."""
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                self.app.config['MIN_CONNECTIONS'],
                self.app.config['MAX_CONNECTIONS'],
                user=self.app.config['DB_USER'],
                password=self.app.config['USER_PASSWORD'],
                host=self.app.config['DB_HOST'],
                port=self.app.config['DB_PORT'],
                database=self.app.config['DB_NAME'])
            if self.connection_pool:
                print("Пул соединений успешно создан")

        except (Exception, psycopg2.DatabaseError) as error:
            print("ОШИБКА: Ошибка при подключении к БД", error)
        finally:
            if not self.connection_pool:
                self.connection_pool.closeall()
                print("Соединение с PostgreSQL закрыто")

    def get_conn(self):
        """
        Получить соединение из пула.

        :return: соединение из БД.
        """
        if 'db_conn' not in g:
            g.db_conn = self.connection_pool.getconn()
            print("Успешно получено соединение из пула")
        return g.db_conn

    def query_with_escape(self, query, data, sql_operator=None):
        """
        Выполнить SQL запрос. Несколько запросов в контексте одного
        приложения (вызов этого метода несколько раз в течении одного
        HTTP запроса) будут использовать одно соединение.

        :param query: строка SQL запроса.
        :param data: данные для вставки в SQL запрос.
        :param sql_operator: Тип запроса(select, update и т.д.)
        Определяет возвращаемое функцией значение
        :return: Результат запроса,
        обработанный методом prepare_answer (если нет ошибок). Иначе None.
        """

        connection = self.get_conn()
        if connection:
            try:
                cursor = connection.cursor(cursor_factory=DictCursor)
                cursor.execute(query, data)
                result = self.prepare_answer(cursor, sql_operator=sql_operator)
                connection.commit()
                cursor.close()
                return result
            except psycopg2.Error as error:
                print(error)
        else:
            print("ОШИБКА: Невозможно получить соединение")
            return None

    def query(self, query, sql_operator=None):
        """
        Выполнить SQL запрос. Несколько запросов в контексте одного
        приложения (вызов этого метода несколько раз в течении одного
        HTTP запроса) будут использовать одно соединение.

        :param query: строка SQL запроса.
        :param sql_operator: Тип запроса(select, update и т.д.)
        Определяет возвращаемое функцией значение
        :return: Результат запроса,
        обработанный методом prepare_answer (если нет ошибок). Иначе None.
        """

        connection = self.get_conn()
        if connection:
            try:
                cursor = connection.cursor(cursor_factory=DictCursor)
                cursor.execute(query)
                result = self.prepare_answer(cursor, sql_operator=sql_operator)
                connection.commit()
                cursor.close()
                return result
            except psycopg2.Error as error:
                print(error)
        else:
            print("ОШИБКА: Невозможно получить соединение")
            return None

    def query_per_one_pool_conn(self, query):
        """
        Выполнить SQL запрос, но на каждый запрос будет выделено одно
        соединение из пула.

        :param query: строка SQL запроса.
        :return: Записи из БД (DictionaryRow), если нет ошибок. Иначе None.
        """
        pool = self.connection_pool
        connection = pool.getconn()
        if connection:
            try:
                cursor = connection.cursor(cursor_factory=DictCursor)
                cursor.execute(query)
                records = cursor.fetchall()
                cursor.close()
                pool.putconn(connection)
                return records
            except psycopg2.Error as error:
                print(error)
        else:
            print("ОШИБКА: Невозможно получить соединение")
            return None

    def query_with_conn(self, query):
        """
        Выполнить SQL запрос, но на каждый запрос будет выделено одно
        соединение, созданное в этом же методе (т.е. не из пула).

        :param query: строка SQL запроса.
        :return: Записи из БД (DictionaryRow), если нет ошибок. Иначе None.
        """
        pass

    @staticmethod
    def prepare_answer(cursor, sql_operator=None):
        """
        Формирует структуру ответа взаисимости от типа SQL-запроса

        :param sql_operator: Строка. Тип SQL-запроса (select, update и т.д)
        :param cursor: Строка. Объект cursor библиотеки psycopg2
        :return: Результат SQL запроса
        """
        if sql_operator == 'select':
            result = {}
            rows = []
            columns = [desc[0] for desc in cursor.description]
            result["Column"] = columns
            for row in cursor.fetchall():
                row_data = tuple('' if i is None else i for i in row)
                rows.append(dict(zip(columns, row_data)))
            result["Data"] = rows
            result["Count"] = len(rows)
            return result

        elif sql_operator == 'select_id':
            # Return only value of first record
            data = cursor.fetchmany(1)
            if len(data) > 0:
                return data[0][0]
            return None

        elif sql_operator == 'update' or sql_operator == 'delete':
            return cursor.rowcount

        elif sql_operator == 'insert':
            return cursor.fetchone()[0]

        elif sql_operator == 'multiple_insert':
            return [i[0] for i in cursor.fetchall()]

        return None


db_driver = DataBase()
