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
        # Close database resources
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Connection to PostgreSQL closed")


def search_response_history(keyword, area):
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
        AND requests.id_city = {area}
        AND requests.job_title = {keyword}
        """

        cursor.execute(select_query)
        results = cursor.fetchall()
        print(results)
        return results  # Вернуть результаты запроса

    except (Exception, Error) as error:
        print("Error while working with PostgreSQL:", error)
        raise

    finally:
        # Close database resources
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Connection to PostgreSQL closed")
