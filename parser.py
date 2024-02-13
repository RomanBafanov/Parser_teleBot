import aiohttp
import asyncio
import re
from datetime import datetime, timedelta


async def get_employer_info(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            employer_info = await response.json()
            return {
                "Компания": employer_info["name"],
                "Сайт": employer_info.get("site_url", "")
            }
    except aiohttp.ClientError as error:
        print(f"Ошибка при запросе к {url}: {error}")
        return None


async def get_vacancies_hh(keyword, area):
    url = 'https://api.hh.ru/vacancies'
    vacancies_info = []
    period = 30
    per_page = 100
    today = datetime.now().date()
    period_start = today - timedelta(days=period)

    async with aiohttp.ClientSession() as session:
        page = 0
        while True:
            params = {
                'text': keyword,
                'area': area,
                'date_from': period_start.isoformat(),
                'per_page': per_page,
                'page': page
            }
            async with session.get(url, params=params) as response:
                response.raise_for_status()
                page_payload = await response.json()
                print(f"Processing page {page}, total pages: {page_payload['pages']}")

                tasks = []
                for vacancy in page_payload["items"]:
                    if "employer" in vacancy and "url" in vacancy["employer"]:
                        url_employer = vacancy["employer"]["url"]
                        tasks.append(get_employer_info(session, url_employer))

                results = await asyncio.gather(*tasks)
                vacancies_info.extend([info for info in results if info])

                if page < page_payload["pages"] - 1:
                    page += 1
                else:
                    break

    return vacancies_info


async def filter_and_create_dict(vacancies):
    filtered_companies = (company for company in vacancies if company.get('Сайт') != '')
    company_final = {}
    count_companies = 0
    async with aiohttp.ClientSession() as session:
        for company in filtered_companies:
            try:
                async with session.get(company['Сайт']) as response:
                    response.raise_for_status()
                    string = await response.text()
                    pattern = '"tel:(.*?)"'
                    match = re.search(pattern, string)

                    if match:
                        phone_number = match.group(1)

                        if phone_number and phone_number.strip():
                            company_final[company['Компания']] = {
                                'Сайт': company['Сайт'],
                                'Телефон': phone_number
                            }
                            count_companies += 1
                        else:
                            print(f"Не найден телефонный номер на сайте компании {company['Компания']}")

            except aiohttp.ClientError as error:
                print(f"Ошибка при запросе к сайту компании {company['Компания']}: {error}")

    print("Количество компаний:", count_companies)
    return company_final


async def get_companies(keyword, area):
    vacancies = await get_vacancies_hh(keyword, area)
    return await filter_and_create_dict(vacancies)
