import sys
import os
import psycopg2
from psycopg2 import Error
from config_data.config import USER, PASSWORD, HOST, PORT, DATABASE
sys.path.append(os.getcwd())


def create_all_tables():
    connection = psycopg2.connect(user=USER,
                                  password=PASSWORD,
                                  host=HOST,
                                  port=PORT,
                                  database=DATABASE)
    cursor = connection.cursor()

    create_city_table_query = '''CREATE TABLE cities
                              (ID BIGSERIAL ,
                              ID_CITY INTEGER PRIMARY KEY NOT NULL ,
                              CITY VARCHAR NOT NULL)
                               '''

    create_requests_table_query = '''CREATE TABLE requests
                                  (ID BIGSERIAL PRIMARY KEY NOT NULL,
                                  ID_CITY INTEGER NOT NULL ,
                                  JOB_TITLE VARCHAR NOT NULL,
                                  DATE_REQUEST DATE,
                                  FOREIGN KEY (ID_CITY) REFERENCES cities (ID_CITY))
                                   '''

    create_response_table_query = '''CREATE TABLE response
                                  (ID BIGSERIAL PRIMARY KEY NOT NULL,
                                  ID_REQUEST INTEGER NOT NULL,
                                  COMPANY_NAME VARCHAR,
                                  SITE VARCHAR NOT NULL,
                                  TELEPHONE VARCHAR NOT NULL,
                                  FOREIGN KEY (ID_REQUEST) REFERENCES requests (ID))
                                   '''

    try:
        cursor.execute(create_city_table_query)
        cursor.execute(create_requests_table_query)
        cursor.execute(create_response_table_query)
        connection.commit()
        print("Все таблицы созданы успешно")
    except (Exception, Error) as error:
        print("Ошибка создания таблиц:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


create_all_tables()
