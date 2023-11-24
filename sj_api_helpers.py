from itertools import count

import requests

import salary_helpers

SJ_BASE_URL = "https://api.superjob.ru/2.0"
MOSCOW_ID = 4
SEARCH_IN_TITLE = 1
SEARCH_EVERYWHERE = 10
MAX_VACANCIES_PER_REQUEST = 100


def get_lang_vacancies(sj_secret_key, lang):
    for page in count():
        params = {
            "t": MOSCOW_ID,
            'keywords[0][keys]': f"{lang}",
            'keywords[0][srws]': SEARCH_IN_TITLE,
            'keywords[1][keys]': "разработчик программист developer",
            'keywords[1][skwc]': 'or',
            'keywords[1][srws]': SEARCH_EVERYWHERE,
            "count": MAX_VACANCIES_PER_REQUEST,
            "page": page,
        }
        headers = {
            "X-Api-App-Id": sj_secret_key,
        }
        vacancies_response = requests.get(
            f"{SJ_BASE_URL}/vacancies",
            params=params,
            headers=headers
        )

        yield from (
            vacancies_response.json()['objects'],
            vacancies_response.json().get('total', 0),
        )

        if not vacancies_response.json()['more']:
            break


def get_langs_vacancies_stats(sj_secret_key, languages):
    langs_stats = {}
    for lang in languages:
        lang_vacancies, lang_vacancies_count = get_lang_vacancies(
            sj_secret_key,
            lang
        )
        vacancies_salaries = get_vacancies_average_salary(lang_vacancies)
        vacancies_processed, average_salary = vacancies_salaries
        langs_stats[lang] = {
            "vacancies_found": lang_vacancies_count,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary,
        }
    return langs_stats


def get_vacancies_average_salary(vacancies):
    count = 0
    total_salary = 0
    for vacancy in vacancies:
        predicted_salary = salary_helpers.predict_rub_salary(
            currency=vacancy["currency"],
            salary_from=vacancy["payment_from"],
            salary_to=vacancy["payment_to"],
        )
        if not predicted_salary:
            continue
        total_salary += predicted_salary
        count += 1
    avg_salary = int(total_salary / count) if count else 0
    return count, avg_salary
