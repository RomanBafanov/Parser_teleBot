from datetime import datetime, timedelta
import requests
import re
from multiprocessing import Pool
from requests_cache import install_cache

install_cache('hh_cache')


def get_employer_info(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        employer_info = response.json()
    except requests.RequestException as error:
        print(f"Ошибка при запросе к {url}: {error}")
        return None

    return {
        "Компания": employer_info["name"],
        "Сайт": employer_info.get("site_url", "")
    }


def get_vacancies_hh(keyword, area):
    url = 'https://api.hh.ru/vacancies'
    vacancies_info = []
    period = 30
    per_page = 100
    today = datetime.now().date()
    period_start = today - timedelta(days=period)

    page = 0
    while True:
        params = {
            'text': keyword,
            'area': area,
            'date_from': period_start.isoformat(),
            'per_page': per_page,
            'page': page,
            'only_with_company': True
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        page_payload = response.json()
        print(f"Processing page {page}, total pages: {page_payload['pages']}")

        with Pool() as pool:
            vacancies_info.extend(pool.map(get_employer_info,
                                           [vacancy["employer"]["url"] for vacancy in page_payload["items"]
                                            if "employer" in vacancy and "url" in vacancy["employer"]]))

        if page < page_payload["pages"] - 1:
            page += 1
        else:
            break

    return vacancies_info


def filter_and_create_dict(vacancies):
    filtered_companies = (company for company in vacancies if company.get('Сайт') != '')
    company_final = {}
    count_companies = 0

    for company in filtered_companies:
        try:
            response = requests.get(company['Сайт'])
            response.raise_for_status()

            string = response.text
            pattern = '"tel:(.*?)"'
            match = re.search(pattern, string)

            if match:
                phone_number = match.group(1)

                # Проверка на null и пустую строку
                if phone_number and phone_number.strip():
                    company_final[company['Компания']] = {
                        'Сайт': company['Сайт'],
                        'Телефон': phone_number
                    }
                    count_companies += 1
                else:
                    # Обработка null или пустой строки
                    print(f"Не найден телефонный номер на сайте компании {company['Компания']}")

        except requests.RequestException as error:
            # Обработка ошибок запросов
            print(f"Ошибка при запросе к сайту компании {company['Компания']}: {error}")

    print("Количество компаний:", count_companies)
    return company_final


def get_companies(keyword, area):
    vacancies = get_vacancies_hh(keyword, area)
    return filter_and_create_dict(vacancies)
