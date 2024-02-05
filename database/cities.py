import os
import sys
import psycopg2
from psycopg2 import Error
from config_data.config import USER, PASSWORD, HOST, PORT
sys.path.append(os.getcwd())


def search_cities():
    connection = None
    cursor = None
    try:

        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database="parserhh_db")
        cursor = connection.cursor()
        cursor.execute(f'''SELECT id_city, city 
                            FROM cities''')
        record = cursor.fetchall()
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
    return record
