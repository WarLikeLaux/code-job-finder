import os

from dotenv import load_dotenv
from terminaltables import AsciiTable

import hh_api_helpers
import sj_api_helpers

LANGUAGES = [
    "Python",
    "JavaScript",
    "Java",
    "PHP",
    "C++",
    "C#",
    "TypeScript",
    "Kotlin",
    "Go",
    "Swift",
]


def main():
    load_dotenv()
    hh_max_pages = int(os.environ["HH_MAX_PAGES"])
    hh_timeout = int(os.environ["HH_TIMEOUT"])
    hh_vacancies_stats = hh_api_helpers.get_langs_vacancies_stats(
        LANGUAGES,
        hh_max_pages,
        hh_timeout
    )
    hh_vacancies_table = [
        [
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата',
        ]
    ]
    for lang, stats in hh_vacancies_stats.items():
        row = [
            lang,
            stats['vacancies_found'],
            stats['vacancies_processed'],
            stats['average_salary']
        ]
        hh_vacancies_table.append(row)
    hh_vacancies_table = AsciiTable(
        hh_vacancies_table,
        title="HeadHunter Moscow"
    )
    print(hh_vacancies_table.table)

    sj_secret_key = os.environ["SJ_SECRET_KEY"]
    sj_vacancies_stats = sj_api_helpers.get_langs_vacancies_stats(
        sj_secret_key,
        LANGUAGES
    )
    sj_vacancies_table = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата",
        ]
    ]
    for lang, stats in sj_vacancies_stats.items():
        row = [
            lang,
            stats["vacancies_found"],
            stats["vacancies_processed"],
            stats["average_salary"],
        ]
        sj_vacancies_table.append(row)
    sj_vacancies_table = AsciiTable(
        sj_vacancies_table,
        title="SuperJob Moscow"
    )
    print(sj_vacancies_table.table)


if __name__ == "__main__":
    main()
