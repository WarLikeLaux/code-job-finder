from itertools import count

import requests

SJ_BASE_URL = "https://api.superjob.ru/2.0"


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
        r = requests.get(
            f"{SJ_BASE_URL}/vacancies",
            params=params,
            headers=headers
        )

        yield from r.json()['objects']

        if not r.json()['more']:
            break


def predict_rub_salary(vacancy):
    if vacancy["currency"] != "rub":
        return None
    if not vacancy["payment_from"]:
        return vacancy["payment_to"] * 0.8
    if not vacancy["payment_to"]:
        return vacancy["payment_from"] * 1.2
    return (vacancy["payment_to"] + vacancy["payment_from"]) / 2


def get_langs_vacancies_info(sj_secret_key, languages):
    langs_info = {}
    for lang in languages:
        lang_vacancies = get_lang_vacancies(sj_secret_key, lang)
        vacancies_salaries = get_vacancies_average_salary(lang_vacancies)
        langs_info[lang] = {
            "vacancies_found": get_lang_vacancies_count(sj_secret_key, lang),
            "vacancies_processed": vacancies_salaries.get('count', 0),
            "average_salary": vacancies_salaries.get('avg_salary', 0),
        }
    return langs_info


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
    r = requests.get(
        f"{SJ_BASE_URL}/vacancies",
        params=params,
        headers=headers
    )
    return r.json().get('total', 0)


def get_vacancies_average_salary(vacancies):
    count = 0
    salary = 0
    for vacancy in vacancies:
        if not predict_rub_salary(vacancy):
            continue
        salary += predict_rub_salary(vacancy)
        count += 1
    avg_salary = 0 if count == 0 else int(salary / count)
    return {
        "count": count,
        "avg_salary": avg_salary
    }
