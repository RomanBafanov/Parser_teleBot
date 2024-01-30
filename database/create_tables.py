import sys
import os
import psycopg2
from psycopg2 import Error
from config_data.config import USER, PASSWORD, HOST, PORT
sys.path.append(os.getcwd())


def city_database():
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database="parserhh_db")

        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE cities
                              (ID BIGSERIAL PRIMARY KEY NOT NULL,
                              ID_CITY INTEGER NOT NULL,
                              CITY VARCHAR NOT NULL)
                               '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица cities успешно создана в PostgreSQL")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL create_tables.cities", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


def requests():
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database="parserhh_db")

        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE requests
                                  (ID BIGSERIAL PRIMARY KEY NOT NULL,
                                  ID_CITY INTEGER NOT NULL,
                                  JOB_TITLE VARCHAR NOT NULL,
                                  DATE_REQUEST DATE,
                                  FOREIGN KEY (ID_CITY) REFERENCES cities (ID))
                                   '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица requests успешно создана в PostgreSQL")
        print("Связь между таблицами 'cities' и 'requests' успешно установлена")

        connection.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL create_tables.requests", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


def response():
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database="parserhh_db")

        cursor = connection.cursor()

        create_table_query = '''CREATE TABLE response
                                  (ID BIGSERIAL PRIMARY KEY NOT NULL,
                                  ID_REQUEST INTEGER NOT NULL,
                                  COMPANY_NAME VARCHAR,
                                  SITE VARCHAR NOT NULL,
                                  TELEPHONE VARCHAR NOT NULL,
                                  FOREIGN KEY (ID_REQUEST) REFERENCES requests (ID))
                                   '''

        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица requests успешно создана в PostgreSQL")

        cursor = connection.cursor()

        alter_orders_table_query = '''ALTER TABLE response
                ADD CONSTRAINT requests
                FOREIGN KEY (ID_REQUEST) REFERENCES requests (ID);'''

        cursor.execute(alter_orders_table_query)
        print("Связь между таблицами 'requests' и 'response' успешно установлена")

        connection.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL create_tables.response", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


city_database()
requests()
response()
