from itertools import count

import requests

SJ_BASE_URL = "https://api.superjob.ru/2.0"
SALARY_LOWER_BOUND_MULTIPLIER = 0.8
SALARY_UPPER_BOUND_MULTIPLIER = 1.2


def get_lang_vacancies(sj_secret_key, lang):
    for page in count():
        params = {
            "t": 4,
            'keywords[0][keys]': f"{lang}",
            'keywords[0][srws]': 1,
            'keywords[1][keys]': "разработчик программист developer",
            'keywords[1][skwc]': 'or',
            'keywords[1][srws]': 10,
            "count": 100,
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

        yield from vacancies_response.json()['objects']

        if not vacancies_response.json()['more']:
            break


def predict_rub_salary(vacancy):
    if vacancy["currency"] != "rub":
        return None
    if not vacancy["payment_from"]:
        return vacancy["payment_to"] * SALARY_LOWER_BOUND_MULTIPLIER
    if not vacancy["payment_to"]:
        return vacancy["payment_from"] * SALARY_UPPER_BOUND_MULTIPLIER
    return (vacancy["payment_to"] + vacancy["payment_from"]) / 2


def get_langs_vacancies_stats(sj_secret_key, languages):
    langs_stats = {}
    for lang in languages:
        lang_vacancies = get_lang_vacancies(sj_secret_key, lang)
        vacancies_salaries = get_vacancies_average_salary(lang_vacancies)
        langs_stats[lang] = {
            "vacancies_found": get_lang_vacancies_count(sj_secret_key, lang),
            "vacancies_processed": vacancies_salaries[0],
            "average_salary": vacancies_salaries[1],
        }
    return langs_stats


def get_lang_vacancies_count(sj_secret_key, lang):
    params = {
        "t": 4,
        'keywords[0][keys]': f"{lang}",
        'keywords[0][srws]': 1,
        'keywords[1][keys]': "разработчик программист developer",
        'keywords[1][skwc]': 'or',
        'keywords[1][srws]': 10,
    }
    headers = {
        "X-Api-App-Id": sj_secret_key,
    }
    vacancies_response = requests.get(
        f"{SJ_BASE_URL}/vacancies",
        params=params,
        headers=headers
    )
    return vacancies_response.json().get('total', 0)


def get_vacancies_average_salary(vacancies):
    count = 0
    total_salary = 0
    for vacancy in vacancies:
        if not predict_rub_salary(vacancy):
            continue
        total_salary += predict_rub_salary(vacancy)
        count += 1
    avg_salary = 0 if count == 0 else int(total_salary / count)
    return count, avg_salary
