import time
from itertools import count

import requests

HH_BASE_URL = "https://api.hh.ru"


def get_langs_vacancies(languages):
    langs_vacancies = {}
    for language in languages:
        params = {
            "text": f"Программист {language}",
            "period": 30,
        }
        r = requests.get(f"{HH_BASE_URL}/vacancies", params=params)
        count = r.json().get('found', 0)
        langs_vacancies[language] = count
    return langs_vacancies


def predict_rub_salary(vacancy):
    if vacancy["salary"]["currency"] != "RUR":
        return None
    if not vacancy["salary"]["from"]:
        return vacancy["salary"]["to"] * 0.8
    if not vacancy["salary"]["to"]:
        return vacancy["salary"]["from"] * 1.2
    return (vacancy["salary"]["to"] + vacancy["salary"]["from"]) / 2


def get_langs_vacancies_info(languages):
    langs_info = {}
    for lang in languages:
        lang_vacancies = get_lang_vacancies(lang)
        vacancies_salaries = get_vacancies_average_salary(lang_vacancies)
        langs_info[lang] = {
            "vacancies_found": get_lang_vacancies_count(lang),
            "vacancies_processed": vacancies_salaries.get('count', 0),
            "average_salary": vacancies_salaries.get('avg_salary', 0),
        }
    return langs_info


def get_lang_vacancies_count(lang):
    params = {
        "text": f"Программист {lang}",
        "only_with_salary": "true",
        "period": 30
    }
    r = requests.get(f"{HH_BASE_URL}/vacancies", params=params)
    return r.json().get('found', 0)


def get_lang_vacancies(lang="python"):
    for page in count():
        params = {
            "text": f"программист {lang}",
            "only_with_salary": "true",
            "period": 30,
            'page': page
        }
        page_response = requests.get(f"{HH_BASE_URL}/vacancies", params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()

        time.sleep(1)

        yield from page_payload['items']

        if page > 0:
            break
        if page + 1 >= page_payload['pages']:
            break


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
