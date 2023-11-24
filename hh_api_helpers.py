import time
from itertools import count

import requests

import salary_helpers

HH_BASE_URL = "https://api.hh.ru"
HH_SEARCH_PERIOD_DAYS = 30


def get_langs_vacancies_stats(languages, hh_max_pages, hh_timeout):
    langs_stats = {}
    for lang in languages:
        lang_vacancies, lang_vacancies_count = get_lang_vacancies(
            lang,
            hh_max_pages,
            hh_timeout
        )
        vacancies_salaries = get_vacancies_average_salary(lang_vacancies)
        langs_stats[lang] = {
            "vacancies_found": lang_vacancies_count,
            "vacancies_processed": vacancies_salaries[0],
            "average_salary": vacancies_salaries[1],
        }
    return langs_stats


def get_lang_vacancies(lang="python", max_pages=1, timeout=1):
    for page in count():
        if max_pages and page >= max_pages:
            break
        params = {
            "text": f"программист {lang}",
            "period": HH_SEARCH_PERIOD_DAYS,
            'page': page
        }
        page_response = requests.get(f"{HH_BASE_URL}/vacancies", params=params)
        page_response.raise_for_status()
        page_payload = page_response.json()

        time.sleep(timeout)

        yield from (page_payload['items'], page_payload.get('found', 0))

        if page + 1 >= page_payload['pages']:
            break


def get_vacancies_average_salary(vacancies):
    count = 0
    total_salary = 0
    for vacancy in vacancies:
        vacancy_salary = vacancy["salary"]
        if not vacancy_salary:
            continue
        predicted_salary = salary_helpers.predict_rub_salary(
            currency=vacancy_salary["currency"],
            salary_from=vacancy_salary["from"],
            salary_to=vacancy_salary["to"],
        )
        if not predicted_salary:
            continue
        total_salary += predicted_salary
        count += 1
    avg_salary = int(total_salary / count) if count else 0
    return count, avg_salary
