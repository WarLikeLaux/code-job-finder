import time
from itertools import count

import requests

HH_BASE_URL = "https://api.hh.ru"
HH_SEARCH_PERIOD_DAYS = 30
SALARY_LOWER_BOUND_MULTIPLIER = 0.8
SALARY_UPPER_BOUND_MULTIPLIER = 1.2


def predict_rub_salary(vacancy):
    if vacancy["salary"]["currency"] != "RUR":
        return None
    if not vacancy["salary"]["from"]:
        return vacancy["salary"]["to"] * SALARY_LOWER_BOUND_MULTIPLIER
    if not vacancy["salary"]["to"]:
        return vacancy["salary"]["from"] * SALARY_UPPER_BOUND_MULTIPLIER
    return (vacancy["salary"]["to"] + vacancy["salary"]["from"]) / 2


def get_langs_vacancies_stats(languages, hh_max_pages, hh_timeout):
    langs_stats = {}
    for lang in languages:
        lang_vacancies = get_lang_vacancies(lang, hh_max_pages, hh_timeout)
        vacancies_salaries = get_vacancies_average_salary(lang_vacancies)
        langs_stats[lang] = {
            "vacancies_found": get_lang_vacancies_count(lang),
            "vacancies_processed": vacancies_salaries[0],
            "average_salary": vacancies_salaries[1],
        }
    return langs_stats


def get_lang_vacancies_count(lang):
    params = {
        "text": f"Программист {lang}",
        "only_with_salary": "true",
        "period": HH_SEARCH_PERIOD_DAYS
    }
    vacancies_response = requests.get(
        f"{HH_BASE_URL}/vacancies",
        params=params
    )
    return vacancies_response.json().get('found', 0)


def get_lang_vacancies(lang="python", max_pages=1, timeout=1):
    for page in count():
        if max_pages and page >= max_pages:
            break
        params = {
            "text": f"программист {lang}",
            "only_with_salary": "true",
            "period": HH_SEARCH_PERIOD_DAYS,
            'page': page
        }
        page_response = requests.get(f"{HH_BASE_URL}/vacancies", params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()

        time.sleep(timeout)

        yield from page_payload['items']

        if page + 1 >= page_payload['pages']:
            break


def get_vacancies_average_salary(vacancies):
    count = 0
    total_salary = 0
    for vacancy in vacancies:
        predicted_salary = predict_rub_salary(vacancy)
        if not predicted_salary:
            continue
        total_salary += predicted_salary
        count += 1
    avg_salary = int(total_salary / count) if count else 0
    return count, avg_salary
