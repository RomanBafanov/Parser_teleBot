import sys
import os
import psycopg2
from psycopg2 import Error
from config_data.config import USER, PASSWORD, HOST, PORT
sys.path.append(os.getcwd())


def create_requests(area, keyword, date):
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database="parserhh_db")
        cursor = connection.cursor()
        insert_query = """INSERT INTO requests(id_city, job_title, date_request) VALUES(%s, %s, %s)
                       """

        cursor.execute(insert_query, (area, keyword, date))
        connection.commit()

    except (Exception, Error) as error:
        print("Error while working with PostgreSQL:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Connection to PostgreSQL closed")
