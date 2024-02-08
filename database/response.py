import sys
import os
import logging
import psycopg2
from psycopg2 import Error
from config_data.config import USER, PASSWORD, HOST, PORT
# from openpyxl import Workbook
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


def search_response_history(area, keyword):
    print(f"Значение переменной area: {area}")
    print(f"Значение переменной keyword: {keyword}")
    # logging.info(f"Вызов функции search_response_history с аргументами: keyword={keyword}, area={area}")
    # area = 60
    # keyword = 'Повар'
    # print(keyword, area)
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user=USER,
                                      password=PASSWORD,
                                      host=HOST,
                                      port=PORT,
                                      database="parserhh_db")
        logging.debug("Выполнен запрос к базе данных")
        cursor = connection.cursor()
        select_query = f"""
        SELECT company_name, site, telephone
        FROM response, requests
        WHERE response.id_request = requests.id
        AND requests.id_city = {area}
        AND requests.job_title = '{keyword}'
        """

        cursor.execute(select_query, (area, keyword))
        result = cursor.fetchall()
        return result  # Вернуть результаты запроса

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


# keyword = 'Слесарь'
# area = 61
# result = search_response_history(keyword, area)
#
#
#
# wb = Workbook()
#
# sheet = wb.active
#
# sheet.cell(row=1, column=1).value = "Компания"
# sheet.cell(row=1, column=2).value = "Сайт"
# sheet.cell(row=1, column=3).value = "Телефон"
#
# last_row = sheet.max_row + 1  # Определение номера строки для начала заполнения данных
# for row_index, row in enumerate(result, start=last_row):
#     company, website, phone_number = row
#     sheet.cell(row=row_index, column=1).value = company
#     sheet.cell(row=row_index, column=2).value = website
#     sheet.cell(row=row_index, column=3).value = phone_number
#
# # После заполнения данных настраиваем ширину столбцов и сохраняем файл
# for column in sheet.columns:
#     max_length = 0
#     for cell in column:
#         try:  # Необходимо для избежания ошибок при обработке пустых ячеек
#             if len(str(cell.value)) > max_length:
#                 max_length = len(str(cell.value))
#         except:
#             pass
#     adjusted_width = (max_length + 2)
#     sheet.column_dimensions[column[0].column_letter].width = adjusted_width
#
# wb.save("history.xlsx")
    # absolute_path = os.path.abspath("history.xlsx")
    # document = FSInputFile(absolute_path)
    # await bot.send_document(chat_id=callback.from_user.id, document=document)