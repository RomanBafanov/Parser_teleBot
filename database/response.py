import sys
import os
import psycopg2
from psycopg2 import Error
from config_data.config import USER, PASSWORD, HOST, PORT
sys.path.append(os.getcwd())


def insert_response_data(id_request, company_name, site, telephone):

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database="parserhh_db")
        cursor = connection.cursor()

        insert_query = """
            INSERT INTO response (ID_REQUEST, COMPANY_NAME, SITE, TELEPHONE)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (id_request, company_name, site or None, telephone or None))
        connection.commit()

    except (Exception, Error) as error:
        print("Error while working with PostgreSQL:", error)
        raise

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Connection to PostgreSQL closed")


def search_response_history(city_code, title_job):

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database="parserhh_db")
        cursor = connection.cursor()
        select_query = f"""
        SELECT company_name, site, telephone
        FROM response, requests
        WHERE response.id_request = requests.id
        AND requests.id_city = {city_code}
        AND requests.job_title = '{title_job}'
        """

        cursor.execute(select_query, (city_code, title_job))
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


def search_response_history1(city_code, title_job):
    result = search_response_history(city_code, title_job)
    return result
