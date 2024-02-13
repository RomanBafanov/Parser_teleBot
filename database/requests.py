import sys
import os
import psycopg2
from psycopg2 import Error
from config_data.config import USER, PASSWORD, HOST, PORT, DATABASE
sys.path.append(os.getcwd())


def insert_requests_data(area, keyword, date):

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        select_query = """INSERT INTO requests(id_city, job_title, date_request) VALUES(%s, %s, %s)
                       """

        cursor.execute(select_query, (area, keyword, date))
        connection.commit()
        insert_query = f""" SELECT ID from requests ORDER BY ID DESC"""

        cursor.execute(insert_query)
        record = cursor.fetchall()
        connection.commit()
        id = record[0][0]

    except (Exception, Error) as error:
        print("Error while working with PostgreSQL:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Connection to PostgreSQL closed")
    return id


def search_requests_history():

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database=DATABASE)
        cursor = connection.cursor()
        select_query = """ SELECT cities.city, requests.job_title, requests.date_request
                            FROM cities, requests
                            WHERE cities.id_city = requests.id_city  """

        cursor.execute(select_query)
        result = cursor.fetchall()
        return result

    except (Exception, Error) as error:
        print("Error while working with PostgreSQL:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Connection to PostgreSQL closed")


def search_history():
    result = search_requests_history()
    return result
